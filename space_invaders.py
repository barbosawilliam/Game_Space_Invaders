"""
  AO PREENCHER ESSE CABEÇALHO COM O MEU NOME E O MEU NÚMERO USP, 
  DECLARO QUE SOU O ÚNICO AUTOR E RESPONSÁVEL POR ESSE PROGRAMA. 
  TODAS AS PARTES ORIGINAIS DESSE EXERCÍCIO PROGRAMA (EP) FORAM 
  DESENVOLVIDAS E IMPLEMENTADAS POR MIM SEGUINDO AS INSTRUÇÕES
  DESSE EP E QUE PORTANTO NÃO CONSTITUEM DESONESTIDADE ACADÊMICA
  OU PLÁGIO.  
  DECLARO TAMBÉM QUE SOU RESPONSÁVEL POR TODAS AS CÓPIAS
  DESSE PROGRAMA E QUE EU NÃO DISTRIBUI OU FACILITEI A
  SUA DISTRIBUIÇÃO. ESTOU CIENTE QUE OS CASOS DE PLÁGIO E
  DESONESTIDADE ACADÊMICA SERÃO TRATADOS SEGUNDO OS CRITÉRIOS
  DIVULGADOS NA PÁGINA DA DISCIPLINA.
  ENTENDO QUE EPS SEM ASSINATURA NÃO SERÃO CORRIGIDOS E,
  AINDA ASSIM, PODERÃO SER PUNIDOS POR DESONESTIDADE ACADÊMICA.

  Nome : WILLIAM SIMÕES BARBOSA
  NUSP : 9837646
  Turma: 07
  Prof.: Alan Mitchell Durham

  Referências: Com exceção das rotinas fornecidas no enunciado
  e em sala de aula, caso você tenha utilizado alguma refência,
  liste-as abaixo para que o seu programa não seja considerado
  plágio ou irregular.
  
  Exemplo:
  - O algoritmo Quicksort foi baseado em
  http://wiki.python.org.br/QuickSort

  """

# !!!!! NÃO APAGUE NEM ALTERE NENHUM import !!!!!!
import random

# !!!!! PARA TESTAR O JOGO, USE VALORES MENORES, COMO 10 E 5, MAS
# VOLTE PARA O ORIGINAL ANTES DE ENTREGAR !!!!
COLUNA_MAXIMA     = 56
LINHA_MAXIMA      = 19

# !!!!! NÃO APAGUE NEM ALTERE NENHUMA CONSTANTE !!!!!
# CONSTANTES DE IMPRESSÃO NA TELA
CANHAO            = 'A'
NAVE              = 'V'
LASER_CANHAO      = '^'
LASER_NAVE        = '.'
EXPLOSAO          = '*'

# !!!!! NÃO APAGUE NEM ALTERE NENHUMA CONSTANTE !!!!!
# CONSTANTES DE AÇÕES DE MOVIMENTAÇÃO DOS OBJETOS NO JOGO
ATIRA             = 3  # para tecla 'l' quando movimentar o canhão
ESQUERDA          = -1 # para tecla 'e' quando movimentar o canhão
DIREITA           = 1  # para tecla 'd' quando movimentar o canhão
BAIXO             = -2

# !!!!! NÃO APAGUE NEM ALTERE NENHUMA CONSTANTE !!!!!
# CONSTANTES DE RESULTADO DO JOGO
VENCEU            = True
PERDEU            = False

# !!!!! NÃO APAGUE NEM ALTERE NENHUMA CONSTANTE !!!!!
# CONSTANTES DOS PONTOS RELACIONADOS A LASERS OU NAVES DESTRUÍDAS
PONTOS_ACERTOU_LASER     = 1
PONTOS_ACERTOU_NAVE      = 3

# !!!!! NÃO APAGUE NEM ALTERE NENHUMA CONSTANTE !!!!!
# OUTRAS CONSTANTES: SEMENTE DO GERADOR DE NÚMEROS ALEATÓRIOS E
# VALORES USADOS NA FUNÇÃO QUE MOVIMENTA AS NAVES
SEMENTE           = 0
ATINGIU_ESQUERDA  = -1
ATINGIU_DIREITA   = 1
ATINGIU_EMBAIXO   = -2

# !!!!! NÃO MODIFIQUE NADA NO main() !!!!!
# FUNÇÃO PRINCIPAL QUE SÓ LÊ A QUANTIDADE DE INIMIGOS DO TECLADO,
# PASSA O CONTROLE PARA A FUNÇÃO REAL DO JOGO E RECEBE COMO RETORNO A
# PONTUAÇÃO DO JOGADOR PARA IMPRIMIR NA TELA COM O RESULTADO DO JOGO
def main():
    random.seed(SEMENTE)
    
    quantidadeNaves = int(input("Digite o numero de naves (inteiro maior que 1 e menor que %d): " %(COLUNA_MAXIMA-3)))
    
    resultado = joga(quantidadeNaves)
    
    if resultado[0] == VENCEU:
        print(">>> CONGRATULATIONS! Você venceu!")
    else:
        print(">>> GAME OVER! Você perdeu!")
    
    print(">>> Pontuação:",resultado[1]) 

# DEMAIS FUNÇÕES NECESSÁRIAS PARA O JOGO
# !!!!! SEU TRABALHO COMEÇA AQUI. COMPLETE TODAS AS FUNÇÕES !!!!!
# !!!!! MAS NÃO MODIFIQUE A ASSINATURA DE NENHUMA DELAS E NEM O QUE JÁ ESTÁ FEITO !!!!!

# Passo 0: função para imprimir a matriz do jogo. Ela precisa ser
# modificada para imprimir os '|' nas laterais direita e esquerda
def imprimeMatriz(matriz):
    ''' (matriz) -> None
        
          Imprime a matriz do jogo. Cada posição da matriz é um caracter e deve
          ser impresso exatamente com o valor dele.'''
    
    for linha in matriz:
        print("|", end = "")
        for posicao in linha:
            print(posicao, end="")
        print("|", end = "")
        print("")

# Passo 1: função que cria todos os elementos na matriz do jogo (Deve
# ser chamada só no início do jogo)
def criaElementos(quantidadeNaves, matriz):
    ''' int, (matriz) -> None
    
          Recebe um inteiro com a quantidade de naves a serem criadas
          e a matriz de caracteres vazia para colocar os elementos no início do
          jogo: o canhão do jogador na linha de baixo e na coluna do meio e as
          naves na parte superior. As naves devem sempre ficar em pares (um em
          cima do outro) e separados pelos outros pares por uma coluna vazia.
          Por exemplo, se a quantidade de naves for 4, a parte superior da
          matriz tem que ficar assim:
          
          V V
          V V
          
          Se for 6 tem que ficar assim:
          
          V V V
          V V V

          Se for 5 tem que ficar assim:

          V V V
          V V  
          '''
    matriz[LINHA_MAXIMA][COLUNA_MAXIMA//2] = CANHAO
    navesAdicionadas = 0
    j = 0
    while ((quantidadeNaves - navesAdicionadas) >= 2):
        for i in range(2): 
            matriz[i][j] = NAVE
            navesAdicionadas += 1
        j += 2
    i = 0
    if (navesAdicionadas < quantidadeNaves):
        matriz[i][j] = NAVE

# Passo 2: primeira função para mover algum elemento que emite lasers.
# Nesse caso para mover o canhão do jogador.
def moveCanhao(direcao, matriz):
    ''' int, (matriz) -> bool
 
          Recebe um inteiro com a direção (valores definidos em ESQUERDA e
          DIREITA) para mover o canhão do jogador (caracter definido em CANHAO)
          e a matriz de caracteres do jogo, para mover o canhão nessa direção.
          Ao mover tem que observar se atingiu algum laser de alguma nave (caso
          no qual tem que imprimir um EXPLOSAO no lugar). Nesse caso precisará
          informar que o canhão foi atingido pois a função retorna esse valor.
          
          Retorna:
                   
          True se canhão do jogador foi atingido (False se não)
                   
          Obs.: o movimento do canhão é ciclíco quando ele se move além dos
          limites laterais da matriz do jogo.'''
    houveColisao = False
    for i in range(COLUNA_MAXIMA+1): #procurando a coluna que está o canhão na rodada em questão
        if (matriz[LINHA_MAXIMA][i] == CANHAO):
            posicaoCanhao = i #canhão está nessa coluna)

    #verificando se haverá movimento cíclico com esse movimento
    if (posicaoCanhao == COLUNA_MAXIMA and direcao == DIREITA): #se tá na última coluna e usuário digitou 'd'
        if (matriz[LINHA_MAXIMA][0] == NAVE or matriz[LINHA_MAXIMA][0] == LASER_NAVE): #verificando se há nave ou laser na posição [19][0]
            houveColisao = True 
            matriz[LINHA_MAXIMA][0] = EXPLOSAO
            matriz[LINHA_MAXIMA][posicaoCanhao] = ' '
        else: #se não tiver colisão, imprimir nova posição do CANHAO
            matriz[LINHA_MAXIMA][0] = CANHAO #move o CANHAO de acordo com a direção
            matriz[LINHA_MAXIMA][posicaoCanhao] = ' ' #apaga a antiga posição do canhão
    elif (posicaoCanhao == 0 and direcao == ESQUERDA): #se tá na primeira coluna e usuário digitou 'e'
        if (matriz[LINHA_MAXIMA][COLUNA_MAXIMA] == NAVE or matriz[LINHA_MAXIMA][COLUNA_MAXIMA] == LASER_NAVE): #verificando se há nave ou laser
            houveColisao = True 
            matriz[LINHA_MAXIMA][COLUNA_MAXIMA] = EXPLOSAO
            matriz[LINHA_MAXIMA][posicaoCanhao] = ' '
        else: #se não tiver colisão, imprimir nova posição do CANHAO
            matriz[LINHA_MAXIMA][COLUNA_MAXIMA] = CANHAO
            matriz[LINHA_MAXIMA][posicaoCanhao] = ' '
    else: #se não está nos extremos, só mover normalmente
        if (matriz[LINHA_MAXIMA][posicaoCanhao + direcao] == NAVE or matriz[LINHA_MAXIMA][posicaoCanhao + direcao] == LASER_NAVE):
            houveColisao = True
            matriz[LINHA_MAXIMA][posicaoCanhao + direcao] = EXPLOSAO
            matriz[LINHA_MAXIMA][posicaoCanhao] = ' '
        else:
            matriz[LINHA_MAXIMA][posicaoCanhao + direcao] = CANHAO #move o CANHAO de acordo com a direção
            matriz[LINHA_MAXIMA][posicaoCanhao] = ' ' #apaga a antiga posição do canhão

    return houveColisao

# Passo 2: segunda função para mover algum elemento que emite lasers.
# Nesse caso para mover as naves.
def moveNaves(direcao, matriz):
    ''' int, (matriz) -> [bool, int, int]
 
          Recebe um inteiro com a direcao (valores definidos em ESQUERDA,
          DIREITA e BAIXO) para mover as naves (caracter definido em NAVE) e a
          matriz de caracteres do jogo, para mover as naves nessa direção. Ao
          mover tem que observar se chegou em algum extremo da matriz, se
          atingiu o canhão do jogador e se atingiu algum laser do jogador. No
          primeiro e no segundo caso precisa informar que isso aconteceu e no
          terceiro caso precisa atualizar a quantidade de naves atingidas
          porque a função retorna esses valores numa lista. No segundo caso tem
          que colocar o caracter definido em EXPLOSAO e no terceiro caso a nave
          tem que sumir da matriz.
                   
          Retorna:
          
          [True se canhão do jogador foi atingido (False se não), limite atingido, quantidade de naves atingidas]
           
          Onde limite atingido tem os seguintes significados:
          
          - valor definido em ATINGIU_DIREITA se alguma nave após o movimento chegou em COLUNA_MAXIMA
          - valor definido em ATINGIU_ESQUERDA se alguma nave após o movimento chegou na coluna 0
          - valor definido em ATINGIU_EMBAIXO se alguma nave após o movimento chegou na linha LINHA_MAXIMA
          - 0 caso nenhuma das alternativas anteriores tenha acontecido
          
          Obs.: mesmo que a primeira nave verificada atinja o canhão ou atinja
          a linha mais baixa da matriz, tem que varrer a matriz **inteira** para
          atualizar a quantidade de naves atingidas antes de retornar'''
  
    canhaoDestruido = False #bool pra ver se alguma nave atingiu o canhão
    limiteMatriz = 0 #ainda não atingiu nenhum limite da matriz
    quantidadeNavesDestruidasLasers = 0 #quantidade de naves destruídas por lasers após movimentação de todas as naves
    atingiuUltimaLinha = False

    
    if (direcao == DIREITA): #pensando primeiro no movimento para a direita
    #primeiro vou encontrar a posição da nave da coluna mais à esquerda, depois devo andar de duas em duas pra dar certo

        i = 0
        colunaPrimeira = 100 #valor arbitrário maior que 56 para resolver um problema de mínimo
        while (i < LINHA_MAXIMA): #(0, 19)
            j = 0
            while (j < COLUNA_MAXIMA): #(0, 56)
                if (matriz[i][j] == NAVE):
                    posicaoPrimeiro = j
                    if (posicaoPrimeiro < colunaPrimeira):
                        colunaPrimeira = posicaoPrimeiro
                j += 1
            i += 1

        for i in range(LINHA_MAXIMA): #laços para encontrar todas as naves da matriz e move-las de acordo com a 'direcao'
            for j in range(colunaPrimeira, COLUNA_MAXIMA, 2): #pensando só em mover para a direita olho até a posicao 55, pois na 56 eu moveria pra baixo
              
                if (matriz[i][j] == NAVE): #se tem uma NAVE nessa posição, move-la de acordo com a 'direcao' (no caso, direita)
                    #verificar se na posição para onde a nave vai tem algum laser do canhao
                    if (matriz[i][j+direcao] == LASER_CANHAO): #se tem um LASER_CANHAO para onde a NAVE vai, então apagar os dois
                        matriz[i][j] = ' ' #apagar a antiga posição da NAVE
                        matriz[i][j+direcao] = ' ' #LASER_CANHAO acertou uma nave, contar os pontos
                        quantidadeNavesDestruidasLasers += 1
                    else: #caso não possua LASER_CANHAO na posição que a NAVE vai, então mover a NAVE
                        matriz[i][j+direcao] = NAVE #mover a NAVE
                        matriz[i][j] = ' ' #apagar a antiga posição da NAVE 
                        #agora tenho que verificar se essa nova posição da NAVE corresponde ao limite direito da matriz
                        if ((j + direcao) == COLUNA_MAXIMA):
                            limiteMatriz = ATINGIU_DIREITA

    elif (direcao == ESQUERDA): #movimento para a ESQUERDA
        #encontrar o primeiro elemento da esquerda pra direita pra ir incrementando de 2 em 2
        i = 0
        colunaPrimeira = -50 #valor arbitrário menor que 0
        while (i < LINHA_MAXIMA): # (0, 19)
            j = COLUNA_MAXIMA # (56, 1)
            while (j > 0):
                if (matriz[i][j] == NAVE):
                    posicaoPrimeiro = j
                    if (posicaoPrimeiro > colunaPrimeira):
                        colunaPrimeira = posicaoPrimeiro
                j -= 1
            i += 1

        for i in range(LINHA_MAXIMA): # (0, 18) não preciso olhar para a última linha, pois nela o jogo já acabou
            for j in range(colunaPrimeira, 0, -2): # (j, 1) olho para todas as colunas, nunca deve haver NAVE na posição 0, pois iria pra baixo

                if (matriz[i][j] == NAVE): #se encontrar uma NAVE na posição em questão
                    #verificar se vai ter um LASER_CANHAO na posição que a NAVE vai
                    if (matriz[i][j + direcao] == LASER_CANHAO): #se tiver um LASER_CANHAO, então apagar ambos e computar pontos
                        matriz[i][j + direcao] = ' ' #tudo apagado onde antes tinha um laser, e falta computar pontos
                        quantidadeNavesDestruidasLasers += 1
                        matriz[i][j] = ' ' #posição antiga da NAVE é apagada
                    else: #se o caminho para a ESQUERDA estiver limpo, então mover a NAVE
                        matriz[i][j + direcao] = NAVE #colocou a NAVE para a ESQUERDA, pois direcao é -1
                        matriz[i][j] = ' ' #apagou a antiga posição da NAVE
                        #verificar agora se essa nova posição da NAVE corresponde ao limite esquerdo da matriz
                        if ((j + direcao) == 0):
                            limiteMatriz = ATINGIU_ESQUERDA

    #dá pra fazer essa de duas formas, descendo de um em um, indo de baixo pra cima, ou descendo a primeira linha 2, indo de cima pra baixo
    #utilizando a primeira opção
    elif (direcao == BAIXO): #mover todas as naves para baixo tenho que começar pela linha de baixo
        for i in range(LINHA_MAXIMA-1, -1, -1): #vai do (18 ao 0, voltando de 1 em 1) pra ir de trás pra frente
            for j in range(0, COLUNA_MAXIMA+1): #vai da primeira coluna até a última

                if (matriz[i][j] == NAVE): #se encontrar alguma NAVE 

                    #ver se a posição que ela iria tem algum LASER_CANHAO ou o próprio CANHAO (ie, a posição logo abaixo)
                    if (matriz[i + 1][j] == LASER_CANHAO): #se encontrou LASER_CANHAO, apagar ambos e computar os pontos
                        matriz[i + 1][j] = ' '
                        quantidadeNavesDestruidasLasers += 1
                        matriz[i][j] = ' '
                    elif (matriz[i + 1][j] == CANHAO): #se encontrou um canhão, então apagar ambos e imprimir uma EXPLOSAO
                        canhaoDestruido = True #CANHAO foi destruído
                        matriz[i + 1][j] = EXPLOSAO #EXPLOSAO foi impressa
                        matriz[i][j] = ' ' #apaguei a antiga posição da NAVE
                        limiteMatriz = ATINGIU_EMBAIXO #se atingiu o canhão significa que atingiu a linha 19, que é o limite inferior
                    else: #ie, se não encontrar LASER_CANHAO ou CANHAO
                        matriz[i + 1][j] = NAVE
                        matriz[i][j] = ' '

                    #agora verificar se atingiu o limite inferior
                    if ((i + 1) == LINHA_MAXIMA):
                        atingiuUltimaLinha = True

            if (atingiuUltimaLinha):
                limiteMatriz = ATINGIU_EMBAIXO
                #procurando o canhão para imprimir uma explosão, caso nenhuma nave tenha batido nele
                for k in range(COLUNA_MAXIMA+1): #tenho que rodar a última linha inteira para achá-lo
                    if (matriz[LINHA_MAXIMA][k] == CANHAO): #quando encontrar o canhão, imprima uma EXPLOSAO
                        matriz[LINHA_MAXIMA][k] = EXPLOSAO

    lista = [canhaoDestruido, limiteMatriz, quantidadeNavesDestruidasLasers] #completar a lista que deve ser retornada
    return lista

# Passo 3: primeira função para emitir lasers. Nesse caso, para emitir
# um novo laser pelo canhão do jogador.
def emiteLaserCanhao(matriz):
    ''' (matriz) -> [int, int]
 
          Recebe a matriz do jogo e emite um novo laser atirado pelo jogador
          (caracter definido em LASER_CANHAO) uma posição acima da posição onde
          o canhão se encontra.  Ao emitir o laser já tem que observar: se
          atingiu alguma nave e se atingiu algum laser de alguma nave. Em todos
          esses casos o laser recém-emitido já tem que sumir da matriz (ele nem
          chega a ser impresso nesse caso) e tem que atualizar a quantidade de
          naves atingidas e de lasers atingidos pois a função retorna esses
          dois valores numa lista.
 
          Retorna:
 
          [quantidade de naves atingidas, quantidade de lasers atingidos]'''
    quantidadeNavesAtingidas = 0
    quantidadeLasersAtingidos = 0

    for j in range(COLUNA_MAXIMA + 1): #para achar o canhão e emitir um laser preciso varrer a última linha da matriz
        if (matriz[LINHA_MAXIMA][j] == CANHAO): #se encontrou o CANHAO, então atirar para cima
            if (matriz[LINHA_MAXIMA-1][j] == LASER_NAVE): #se na posição de cima do canhão há um laser, então apagá-lo e incrementar pontos
                matriz[LINHA_MAXIMA-1][j] = ' '
                quantidadeLasersAtingidos += 1
            elif (matriz[LINHA_MAXIMA-1][j] == NAVE): #se na posição de cima do canhão há uma nave, então apagá-la e incrementar pontos
                matriz[LINHA_MAXIMA-1][j] = ' '
                quantidadeNavesAtingidas += 1
            else: #se não há nem nave nem laser, então colocar o laser na posição de cima
                matriz[LINHA_MAXIMA-1][j] = LASER_CANHAO

    lista = [quantidadeNavesAtingidas, quantidadeLasersAtingidos]
    return lista

# Passo 3: segunda função para emitir lasers. Nesse caso para emitir
# novos lasers pelas naves.
def emiteLasersNaves(matriz):
    ''' (matriz) -> [bool, int]
 
          Recebe a matriz do jogo e emite lasers pelas naves (caracter definido
          em LASER_NAVE) uma posição abaixo da posição da nave que emitiu o
          laser. Ao emitir o laser já tem que observar: se atingiu o canhão do
          jogador (caso no qual tem que imprimir um EXPLOSAO no lugar) e se
          atingiu algum laser do jogador. Em todos esses casos, o laser
          recém-emitido já tem que sumir da matriz (ele nem chega a ser impresso
          nesse caso). No primeiro caso tem que informar que o canhão do jogador
          foi atingido e no segundo caso tem que atualizar a quantidade de
          lasers atingidos pois a função retorna esses dois valores numa lista.
 
          Para definir se uma nave deve ou não emitir laser, sorteie um
          número aleatório entre 0 e 1 (use a função random.randint para isso),
          inclusive. Se o resultado for 0, não emita o laser para aquela nave.
          Se o resultado for 1, emita. Essa verificação só deve ser feita para
          aquelas naves que não possuem nenhuma outra imediatamente abaixo e
          sempre na ordem da esquerda para a direita da matriz.
                
          Retorna:
          
          [True se canhão do jogador foi atingido (False se não), quantidade de lasers atingidos]
          
          Obs.1: mesmo que o primeiro laser emitido atinja o canhão, tem que
          varrer a matriz **inteira** para atualizar a quantidade de lasers
          atingidos antes de retornar'''
    canhaoDestruido = False
    quantidadeLasersAtingidos = 0
    #laço para encontrar todas as naves capazes de atirar, ie, as que não possuem nave imediatamente abaixo
    for i in range(LINHA_MAXIMA, -1, -1): #naves da última linha não atiram, pois na última linha o jogo já acabou
        for j in range(COLUNA_MAXIMA + 1): #preciso analisar até a última coluna
          
            if (matriz[i][j] == NAVE): #se encontrar uma NAVE, verificar se tem uma nave abaixo
                if (matriz[i+1][j] != NAVE): #se não tiver NAVE abaixo, então chamar função aleatória.
                    if (random.randint(0, 1) == 1): #se o número aleatório for igual a 1, então atirar!!
                        if (matriz[i+1][j] == LASER_CANHAO): #se há um laser do canhão, apagar e contar os pontos
                            matriz[i+1][j] = ' ' #apaguei tudo que tinha na posição
                            quantidadeLasersAtingidos += 1 #contar quantos lasers foram destruídos
                        elif (matriz[i+1][j] == CANHAO): #se o canhão está na linha debaixo, então imprimir uma EXPLOSÃO e mudar variável booleana
                            matriz[i+1][j] = EXPLOSAO
                            canhaoDestruido = True
                        else: #se não há nem laser nem canhão, então coloca o laser
                            matriz[i+1][j] = LASER_NAVE

    lista = [canhaoDestruido, quantidadeLasersAtingidos]
    return lista

# Passo 4: primeira função para mover lasers. Nesse caso, para mover
# os lasers do jogador.
def moveLasersCanhao(matriz):
    ''' (matriz) -> [int, int]
 
          Recebe a matriz do jogo e move todos os lasers atirados pelo jogador
          (caracter definido em LASER_CANHAO) uma posição para cima na matriz.
          Ao mover tem que observar: se saiu do limite da matriz, se atingiu
          alguma nave e se atingiu algum laser de alguma nave. Em todos esses 3
          casos o laser movido tem que sumir da matriz. Nos dois primeiros
          casos tem que atualizar a quantidade de naves atingidas e de lasers
          atingidos pois a função retorna esses dois valores numa lista.
 
          Retorna:
 
          [quantidade de naves atingidas, quantidade de lasers atingidos]'''
    quantidadeNavesDestruidasLasers = 0
    quantidadeLasersDestruidos = 0

    for i in range(LINHA_MAXIMA):
        for j in range(COLUNA_MAXIMA+1):

            if (matriz[i][j] == LASER_CANHAO): #se encontrou um laser do canhão, ver se ele sai do limite da matriz ao mover pra cima
            #ver também se ele atinge algum laser de alguma nave, ou se atinge alguma nave, atualizar os dois pontos
                if (matriz[i-1][j] == NAVE): #se encontrou alguma nave, apagar ambos e atualizar pontos
                    matriz[i][j] = ' ' #apaga a posição do laser_canhao
                    matriz[i-1][j] = ' ' #apaga a posição da NAVE
                    quantidadeNavesDestruidasLasers += 1

                elif (matriz[i-1][j] == LASER_NAVE): #se encontrou algum laser_nave, apagar ambos e atualizar pontos
                    matriz[i][j] = ' '
                    matriz[i-1][j] = ' '
                    quantidadeLasersDestruidos += 1

                elif (i-1 < 0): #se o laser_canhao sair da matriz, apagá-lo
                    matriz[i][j] = ' '

                else:
                    matriz[i][j] = ' '
                    matriz[i-1][j] = LASER_CANHAO

    lista = [quantidadeNavesDestruidasLasers, quantidadeLasersDestruidos]
    return lista

# Passo 4: segunda função para mover lasers. Nesse caso, para
# mover os lasers das naves.
def moveLasersNaves(matriz):
    ''' (matriz) -> [bool, int]
 
          Recebe a matriz do jogo e move todos os lasers atirados pelas naves
          (caracter definido em LASER_NAVE) uma posição para baixo na matriz.
          Ao mover tem que observar: se saiu do limite da matriz, se atingiu o
          canhão do jogador (caso no qual tem que imprimir um EXPLOSAO no lugar)
          e se atingiu algum laser do jogador. Em todos esses 3 casos, o laser
          movido tem que sumir da matriz. No segundo caso tem que informar que o
          canhão do jogador foi atingido e no terceiro caso tem que atualizar a
          quantidade de lasers atingidos pois a função retorna esses dois
          valores numa lista.
                
          Retorna:
          
          [True se canhão do jogador foi atingido (False se não), quantidade de lasers atingidos]
          
          Obs.: mesmo que o primeiro laser verificado atinja o canhão, tem que
          varrer a matriz **inteira** para atualizar a quantidade de lasers
          atingidos antes de retornar'''
    canhaoAtingido = False
    quantidadeLasersDestruidos = 0

    #farei laços que percorrerão a matriz inteira, atualizando cada um dos lasers atirados pelas naves
    #a função moveLasersCanhao() não precisava ir até a linha 19, pois os lasers estavam da 18 pra cima
    #aqui os lasers estão da 1 pra baixo, mas por maior clareza, vou varrer desde a linha 0
    for i in range(LINHA_MAXIMA, 0, -1): #laço que roda da linha 0 até a linha 19, para apagar lasers que estão na última linha
        for j in range(COLUNA_MAXIMA+1): #laço que roda da coluna 0 até a coluna 56, para mover todos os possíveis lasers para baixo
            if (matriz[i][j] == LASER_NAVE): #se encontrar um laser da nave, verificar a posição abaixo (sai da matriz, bate em algo?)

                if (i + 1 > 19): #se sair do limite da matriz, apagá-lo
                    matriz[i][j] = ' '
                elif (matriz[i+1][j] == CANHAO): #se o canhão estiver na linha logo abaixo, então imprimir uma explosão e mudar a booleana
                    canhaoAtingido = True
                    matriz[i+1][j] = EXPLOSAO
                    matriz[i][j] = ' '

                elif (matriz[i+1][j] == LASER_CANHAO): #se encontrar um laser do canhão, apagar ambos e contabilizar pontos
                    quantidadeLasersDestruidos += 1
                    matriz[i][j] = ' '
                    matriz[i+1][j] = ' '


                elif(matriz[i+1][j] == ' '): #se não ocorreu nada disso, se o caminho está livre, então mover o laser
                    matriz[i+1][j] = LASER_NAVE
                    matriz[i][j] = ' '

    lista = [canhaoAtingido, quantidadeLasersDestruidos]
    return lista

# Passo 5: a função que de fato implementa o jogo segundo as regras do
# enunciado. Ela vai chamar toda as funções implementadas nos passos
# anteriores.
def joga(quantidadeNaves):
    ''' int -> [bool, int]
    
          Recebe um inteiro que representa a quantidade de naves, implementa de
          fato o jogo de acordo com as regras do enunciado e retorna uma lista
          com o resultado do jogo:
          
          [resultado, pontuacao]
          
          resultado é uma variável booleana que vale True se o jogador venceu ou
          False se o jogador perdeu.
    
          Para o jogador vencer:
          - O jogador precisa destruir todas as naves
          
          Para o jogador perder:
          - O jogador precisa ser atingido pelo tiro de alguma nave
          - Ou alguma nave precisa alcançar a linha LINHA_MAXIMA da matriz do jogo
          - Ou o jogador precisa ser atingido por alguma nave
    
          pontuacao é uma variável inteira que armazena a quantidade de pontos
          que o jogador fez. A pontuação é definida da seguinte forma:
    
          +PONTOS_ACERTOU_LASER pontos se o jogador consegue acertar 1 tiro em alguma nave
          +PONTOS_ACERTOU_NAVE  pontos se o jogador consegue acertar 1 tiro em algum tiro de alguma nave
    
          A ordem das ações no jogo é:
          - tiros anteriores do jogador se movem
          - imprime o estado do jogo na tela
          - usuário informa se quer atirar ou se mover e a ação escolhida é realizada
          - tiros anteriores das naves se movem
          - naves atiram (de acordo com o sorteio de números aleatórios)
          - naves se movem (de acordo com a rodada - se move apenas nas pares: direita, baixo, esquerda, baixo, direita, etc...
       
          Dentro de cada função de movimentação e de emissão de lasers é
          necessário verificar se houve colisões para aumentar a pontuação, para
          terminar o jogo ou para limpar a tela removendo os elementos que
          sumiram por terem passado do limite da tela (tiros que subiram demais
          e tiros que desceram demais)
    
          Sempre que o jogo terminar, deve imprimir o status final da
          matriz do jogo'''
    
    # Criação da matriz que manterá o estado do jogo.
    matriz = []
    for i in range(LINHA_MAXIMA+1):
        matriz.append([' ']*(COLUNA_MAXIMA+1))
    
    criaElementos(quantidadeNaves, matriz) #cria os elementos da matriz, imprime todas as naves e o canhão

    # Loop do jogo
    resultado     = VENCEU
    fimDeJogo     = False
    pontos        = 0
    rodada        = 1
    direcaoNaves  = DIREITA

    direcaoAnterior = DIREITA
    limiteMatriz = 0
    quantidadeNavesDestruidasLasers = 0
    quantidadeLasersDestruidos = 0
    
    while not fimDeJogo:
        # complete o loop seguindo a ordem das ações explicada no
        # enunciado e no docstring desta função acima.

        listaMoveLasersCanhao = moveLasersCanhao(matriz) #Tiros anteriores do jogador se movem
        quantidadeNavesDestruidasLasers += listaMoveLasersCanhao[0]
        quantidadeLasersDestruidos += listaMoveLasersCanhao[1]
        if (quantidadeNavesDestruidasLasers == quantidadeNaves):
            fimDeJogo = True
            resultado = VENCEU

        if (not fimDeJogo):    
            imprimeMatriz(matriz) #Imprime o estado de jogo na tela

            acaoCanhao = input("’e’ para esquerda, ’d’ para direita e ’l’ para emitir laser: ") #Usuário escolhe o que quer fazer.
            if (acaoCanhao == 'e'): #se quer mover pra esquerda, go on.
                canhaoAtingido = moveCanhao(ESQUERDA, matriz) #retorna um bool se o canhão foi ou não atingido após esse movimento
                if (canhaoAtingido): #se o canhão foi destruído ao se mover para o lado, então canhaoAtingido = True
                    fimDeJogo = True #jogo deve acabar no final desse laço
                    resultado = PERDEU
            elif (acaoCanhao == 'd'):
                canhaoAtingido = moveCanhao(DIREITA, matriz)
                if (canhaoAtingido):
                    fimDeJogo = True
                    resultado = PERDEU
            elif (acaoCanhao == 'l'): #se quiser a opção 'l' = atirar
                listaTiroCanhao = emiteLaserCanhao(matriz)
                quantidadeNavesDestruidasLasers += listaTiroCanhao[0]
                quantidadeLasersDestruidos += listaTiroCanhao[1]
                if (quantidadeNavesDestruidasLasers == quantidadeNaves):
                    fimDeJogo = True
                    resultado = VENCEU
        
        if (not fimDeJogo):
            listaMoveLasersNaves = moveLasersNaves(matriz) #Tiros anteriores das naves se movem.
            canhaoAtingido = listaMoveLasersNaves[0]
            if (canhaoAtingido):
                fimDeJogo = True
                resultado = PERDEU
            quantidadeLasersDestruidos += listaMoveLasersNaves[1]

        if (not fimDeJogo):
            listaTiroNave = emiteLasersNaves(matriz) #Naves atiram (de acordo com o sorteio de números aleatórios).
            canhaoAtingido = listaTiroNave[0]
            if (canhaoAtingido):
                fimDeJogo = True
                resultado = PERDEU
            quantidadeLasersDestruidos += listaTiroNave[1]
        
        if (not fimDeJogo):
            if (rodada % 2 == 0): #Naves se movem (de acordo com a rodada-se movem somente nas pares).
                lista = moveNaves(direcaoNaves, matriz) #na primeira vez diracaoNaves = DIREITA
                canhaoAtingido = lista[0]
                if (canhaoAtingido):
                    fimDeJogo = True
                    resultado = PERDEU
                limiteMatriz = lista[1] #decidir agora a direção da nave com base no limite da matriz
                if (limiteMatriz == ATINGIU_EMBAIXO): #se após mover as naves chegaram na última linha, então acabou.
                    fimDeJogo = True
                    resultado = PERDEU
                if (limiteMatriz == ATINGIU_DIREITA or limiteMatriz == ATINGIU_ESQUERDA):#se ela atingiu algum extremo, move-la pra baixo
                    direcaoAnterior = direcaoNaves #salvar a direção que ela estava indo
                    direcaoNaves = BAIXO #nova direção das NAVES
                elif (direcaoNaves == BAIXO and limiteMatriz == 0): 
                    if (direcaoAnterior == DIREITA):
                        direcaoNaves = ESQUERDA
                    else:
                        direcaoNaves = DIREITA
                quantidadeNavesDestruidasLasers += lista[2]

        if (quantidadeNavesDestruidasLasers == quantidadeNaves): #se todas as naves foram destruídas, então usuário ganhou.
            fimDeJogo = True
            resultado = VENCEU

        pontos = PONTOS_ACERTOU_LASER*quantidadeLasersDestruidos + PONTOS_ACERTOU_NAVE*quantidadeNavesDestruidasLasers
        rodada+=1

    imprimeMatriz(matriz) #última impressão da matriz, pra mostrar onde o canhão foi destruído
    return [resultado, pontos]

main()