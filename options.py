from metodo import *
import time as time
import matplotlib.pyplot as plt



entrada  = printaMenu()
while(entrada!='0'):

    vetorizado = True
    variaT = [0, 0.25, 0.5, 0.75, 1]

    if(entrada=='1'):
        #============================================ 4.1 ========================================
        #Cenario ficticio 1
        N = 10000
        L = 10
        K = 1
        T = 1
        sigma = 0.01
        r = 0.01

        M = calculaM(T, N, sigma, L)
        #============================================== 4.1.1 =====================================

        
        u = calculaU(N, M, sigma, K, L, T, vetorizado)
        S = 1
        t = 0

        premio = calculaV2(calculaV1(u, M, N, T, r), M, N, T, t, L, r, sigma, K, S)

        print(f"A precificacao da opcao de compra de R$ 1000 do ativo para o tempo presente é de {premio*1000}.")

        #=========================================  4.1.2 ==========================================
        Smin = 0.5
        Smax = 1.5

        #parte 1
        t = 0.5
        cenarioFicticio4P1(Smin, Smax, u, M, N, T, r, t, L, sigma, K, premio, 'Cenário 1.2')

        # parte 2
        cenarioFicticio4P2(Smin, Smax, variaT, u, M, N, T, r, L, sigma, K, 'Cenário 1.2')

        #============================================ 4.1.3 ========================================
        sigma = 0.02
        L = 100 #alterado para agilizar o processo
        M = calculaM(T, N, sigma, L)

        u = calculaU(N, M, sigma, K, L, T, vetorizado)

        #com t = 0
        premio = calculaV2(calculaV1(u, M, N, T, r), M, N, T, 0, L, r, sigma, K, S)

        #parte 1
        t = 0.5
        cenarioFicticio4P1(Smin, Smax, u, M, N, T, r, t, L, sigma, K, premio, 'Cenário 1.3')

        # parte 2
        cenarioFicticio4P2(Smin, Smax, variaT, u, M, N, T, r, L, sigma, K, 'Cenário 1.3')

        #============================================ 4.1.4 ========================================
        sigma = 0.1
        r = 0.1
        M = calculaM(T, N, sigma, L)

        u = calculaU(N, M, sigma, K, L, T, vetorizado)

        premio = calculaV2(calculaV1(u, M, N, T, r), M, N, T, 0, L, r, sigma, K, S)
        print(f"A precificacao da opcao de compra de R$ 1000 do ativo para o tempo presente é de {premio*1000}.")

        #parte 1
        t = 0.5
        cenarioFicticio4P1(Smin, Smax, u, M, N, T, r, t, L, sigma, K, premio, 'Cenário 1.4')

        # parte 2
        cenarioFicticio4P2(Smin, Smax, variaT, u, M, N, T, r, L, sigma, K, 'Cenário 1.4')
        
    elif(entrada=='2'):

        #============================================ 4.2 ========================================

        # 1 US = 5,1605 reais em 01/02/2022

        L = 100
        N = 10000
        sigma = 0.1692
        r = 0.1075
        S = 5.6376
        T = 3/12
        K = 5.7
        M = calculaM(T, N, sigma, L)


        u = calculaU(N, M, sigma, K, L, T, vetorizado)
        
        premio = calculaV2(calculaV1(u, M, N, T, r), M, N, T, 0, L, r, sigma, K, S)
        print("O premio da opcao seria: ", end='')
        print(premio)

        cotacaoAtual = 5.1605
        print("O valor da cotacao do dolar no dia 01/02/2022 foi de US$"+str(cotacaoAtual)+".")

        lucro = max(cotacaoAtual - K, 0) - premio

        print("O prejuizo/lucro de cada dolar comprado foi de "+str(lucro)+".")
        print("O prejuizo/lucro total foi de "+str(lucro*100000)+".")

        Smin = 5.2
        Smax = 6.2
        t = 1/12

        pontos = 10
        valores_S = defineValoresS(Smin, Smax, pontos)

        prejuLucro = list()

        i = 0
        while(i!=pontos):
            inter = calculaV2(calculaV1(u, M, N, T, r), M, N, T, t, L, r, sigma, K, valores_S[i])
            prejuLucro.append(inter-premio)
            print("Valor do prejuizo/lucro: "+str(inter-premio)+" Valor de S: "+str(valores_S[i]))
            i = i + 1

        plotaGrafico(valores_S, prejuLucro, 'S (R$)', 'Lucro/prejuízo (R$)', 'Cenário 2: Análise do lucro/prejuízo por opção para diferentes valores de S')
            

    elif(entrada=='3'):
        print("A acao escolida foi do comglomerado AMBEV, seu preco no dia 15/04/2022 é de 14.70 reais por acão. Neste caso, decidimos comprar o valor de 1 milhão de reais para daqui 6 meses.")
        print("A taxa de juros foi baseada na taxa SELIC, por volta de 12.25%. A volatilidade foi calculada a partir da fórmula dada no enunciado, na qual a volatilidade anual é a volatilidade diaria vezes a raiz dos dias uteis no ano, ou seja, a volatilidade anual é de aproximadamente de 15.87%.")
        print("O valor do preco de exercicio da opcao é de 15 por escolha nossa.")

        sigma = 0.1225
        r = 0.1587
        S = 14.70
        K = 15

        N = 10000
        L = 100
        T = 0.5
        M = calculaM(T, N, sigma, L)

        u = calculaU(N, M, sigma, K, L, T, vetorizado)

        premio = calculaV2(calculaV1(u, M, N, T, r), M, N, T, 0, L, r, sigma, K, S) 

        print("O valor do premio é de ", end='')
        print(premio)

        Smin = 14.5
        Smax = 17

        t = 0.5
        cenarioFicticio4P1(Smin, Smax, u, M, N, T, r, t, L, sigma, K, premio, 'Cenário 3')

        Smin = 12
        Smax = 18
        cenarioFicticio4P2(Smin, Smax, variaT, u, M, N, T, r, L, sigma, K, 'Cenário 3')

    elif(entrada=='4'):

        N = 10000
        M = 26
        sigma = 0.01
        K = 1
        L = 10
        T = 1
        vetorizado = False
        # mostra diferenca de tempo entre versao vetorizada e nao-vetorizada da matriz u
        time1 = time.time()
        calculaU(N, M, sigma, K, L, T, vetorizado)
        time2 = time.time()

        vetorizado = True
        time3 = time.time()
        calculaU(N, M, sigma, K, L, T, vetorizado)
        time4 = time.time()

        print("O tempo gasto para a versão não vetorizada foi de: ", time2-time1)
        print("O tempo gasto para a versão vetorizada foi de: ", time4-time3)

    entrada = printaMenu()