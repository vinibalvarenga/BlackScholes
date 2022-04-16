import numpy as np
from statistics import NormalDist
import math
import matplotlib.pyplot as plt

def calculaU(N, M, sigma, K, L, T, vetorizado):
    #parametros gerais
    deltaX = 2*L/N
    deltaTau = T/M
    temp = deltaTau/(deltaX**2) * (sigma**2)/2
    i = j = 0
    
    if( not vetorizado ):
        #cria matriz u nula com N+1 linhas e M+1 colunas
        u = np.zeros((N+1)*(M+1))
        u.shape = (N+1, M+1)
        # Condições de contorno:
        while(j != M+1):
            taui = j*deltaTau
            u[N][j] = K * np.exp(L+(taui/2)*(sigma**2))
            j = j + 1
        while(i != N):
            xi = i*deltaX-L
            u[i][0] = K * max(np.exp(xi)-1,0)
            i = i + 1
        # Calcula os outros termos da matriz u
        i = 1
        j = 1  
        while (j != M+1):         
            i = 1
            while (i != N):
                u[i][j] = u[i][j-1] + temp * (u[i-1][j-1] - 2 * u[i][j-1] + u[i+1][j-1])
                i = i + 1
            j = j + 1
        
        return u
    # nesse caso temos que:
    # u(j+1) = uj +  deltaTau/(deltaX**2) * (sigma**2)/2 *uj *A
    # A = [ [1  0  0 0 0 0 0 ... 0]
    #       [-2 1  0 ...         0]       
    #       [1 -2  1 ...         0]
    #       [0  1 -2 ...         0]
    #       [0  0  1  ...     1  0] 
    #        ...
    else:

        uAnterior = np.zeros((N+1))

        i = 1
        while(i != N):
            xi = i*deltaX - L
            uAnterior[i] = K * max(math.exp(xi)-1, 0)
            i = i + 1
        uAnterior[N] = K * math.exp(L) 

        u = np.array([np.copy(uAnterior)])

        j=0
        while(j != M+1):
            uinter1 = np.zeros((N+1))
            uinter1[1:N+1] = uAnterior[0:N]
            uinter2 = np.zeros((N+1))
            uinter2[1:N] = uAnterior[2:N+1]

            uNovo = uAnterior + temp * (uinter1 - 2 * uAnterior + uinter2)
            u = np.append(u, np.array([np.copy(uNovo)]), axis = 0)

            uAnterior = uNovo
            
            j = j + 1

        return u.T
        
            
######################################
#  u(j+1)i notação vetorizada
# j               0      1  ...   M-1
#          u0     u1     u2       uM
# | i=0  |u00,   u10,       ..., u(M)0
# |      |u01
# |      |
# |      |
# |      |u(0)N, u1N,       ..., uM(N) 

# Função para comparar os métodos vetorizados e não vetorizados
# Ela se vale da fórmula usada no EP para fazer os calculos

def calculaUDistNormal(N, M, T, L, K, sigma): 
    #calcula constantes
    deltax = 2*L/N
    deltatau = T/M
    #cria matriz
    u = np.zeros((N+1)*(M+1))
    u.shape = (N+1, M+1)
    
    i  = 0
    # condição de contorno
    while(i!= N+1):
        xi = i*deltax - L
        u[i][0] = K *  max(np.exp(xi)-1,0)
        i = i + 1

    # Caso geral
    i = 0
    while(i!=N+1):
        xi = i*deltax - L
        j = 1
        while(j!=M+1):
            tauj = j*deltatau
            d1 = (xi + sigma*sigma*tauj)/(sigma*math.sqrt(tauj))
            d2 = xi/(sigma*math.sqrt(tauj))

            u[i][j] = K * math.exp(xi+sigma*sigma*tauj/2)*(NormalDist().cdf(d1)) - K * NormalDist().cdf(d2)

            j = j +1
        i = i + 1 

    return u


def calculaV1(u, M, N, T, r):
    V = np.zeros((N+1)*(M+1))
    V.shape = (N+1, M+1)
    deltatau = T/M

    i = j = 0
    while(i != N+1):
        j = 0
        while(j != M+1):
            tauj = j*deltatau
            V[i][j] = u[i][j] * math.exp(-r*tauj)
            j = j + 1
        i = i + 1 
    return V

def calculaV2(V, M, N, T, t, L, r, sigma, K, S):

    deltax = 2*L/N

    #calculamos x(S,t)
    x = math.log(S/K) + (r - (sigma**2 )/2)* (T-t)

    i = 0
    while(i != N+1):
        xi_1 = (i+1)*deltax - L
        xi = i*deltax - L
        # calculamos i tal que xi< x < xi_i
        if (x >= xi and x <= xi_1):
            # calculamos o j que minimiza o erro de tau
            j = calculaj(t, M, T)
            return ((xi_1 - x)*V[i][j] - (xi - x)*V[i+1][j])/(xi_1-xi)
        i = i + 1

def calculaj(t, M, T):
    deltaTau = T/M
    tau = T - t

    j = 0
    tauj = j*deltaTau
    erroMin = math.fabs(tau - tauj)
    jmin = 0 

    while (j != M+1):
        tauj = j*deltaTau
        erro = math.fabs(tau - tauj)
        if(erro < erroMin):
            jmin = j
            erroMin = erro
        j = j + 1

    return jmin


def defineValoresS(Smin, Smax, pontos):

    listaPontos = list()
    #defina qual vai ser a distancia entre os pontos
    distancia = (Smax - Smin)/(pontos-1)

    i=0
    while (i != pontos):
        listaPontos.append(Smin+i*distancia)
        i = i + 1

    return listaPontos


def calculaM(T, N, sigma, L):
    return math.floor( (T*N*N*sigma*sigma)/(4*L*L) ) + 1


def printaMenu():
    print("-----------------------MENU--------------------------\n\n Selecione o que deseja rodar:")
    print(" 0) Para sair")
    print(" 1) Cenario fictício com K=R$1, sigma = 0.01, T = 1 ano")
    print(" 2) Cenário de câmbio com sigma = 0.1692, r = 0.1075, S = R$5.6376, K = R$5.7, T = 3/12")
    print(" 3) Cenário real com dados reais fornecidos")
    print(" 4) Comparacão entre versão vetorizada e não vetorizada\n")
    return input(" Entrada: ")

def plotaGrafico(valores_S, prejuLucro, xlabel, ylabel, titulo):
    plt.plot(valores_S, prejuLucro, color='k')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(titulo)

    plt.show()

#funcoes auxiliares para fazer as questoes pedidas
#P1 equivale a parte 1, onde colocamos o prejuizo/lucro em relacao aos valores de S
def cenarioFicticio4P1(Smin, Smax, u, M, N, T, r, t, L, sigma, K, premio, numeroQuestao):
    pontos = 20
    valores_S = defineValoresS(Smin, Smax, pontos)

    prejuLucro = list()

    i = 0
    while(i!=pontos):
        inter = calculaV2(calculaV1(u, M, N, T, r), M, N, T, t, L, r, sigma, K, valores_S[i])
        prejuLucro.append(inter-premio)
        i = i + 1

    plotaGrafico(valores_S, prejuLucro, 'S (R$)', 'Lucro/prejuízo (R$)', numeroQuestao+': Análise do lucro/prejuízo por opção para diferentes valores de S')

#P2 equivale a parte 2, onde colocamos o V em relacao ao S para diferentes t
def cenarioFicticio4P2(Smin, Smax, variaT, u, M, N, T, r, L, sigma, K, numeroQuestao):
    pontos = 10
    valores_S = defineValoresS(Smin, Smax, pontos)

    for t in variaT:
        precoOpcao = list()

        i = 0
        while(i!=pontos):
            inter = calculaV2(calculaV1(u, M, N, T, r), M, N, T, t, L, r, sigma, K, valores_S[i])
            precoOpcao.append(inter)
            i = i + 1

        plt.plot(valores_S, precoOpcao)

    plt.xlabel('S (R$)')
    plt.ylabel('Preço da opção (R$)')
    plt.title(numeroQuestao + ': Preço da opção em relação a S para vários valores de tempo')
    plt.show()