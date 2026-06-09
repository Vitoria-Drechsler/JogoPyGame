import pygame
import random
from recursos.funcoes import inicializarBancoDeDados, limpar_tela, escreverDados, maior_pontuador

limpar_tela()
inicializarBancoDeDados()
nome_maior, maior_pontos, dataJogada = maior_pontuador()
pygame.init()

while True:
    nome = input("Informe o Nome do Competidor:")
    if len(nome) > 0: 
        break
    else:
        print("Nome Inválido!")
        
tamanho = (1000,700)
pygame.display.set_caption("Caça Cerejas")
icone  = pygame.image.load("bases/cereja.png")
pygame.display.set_icon(icone)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
branco = (255, 255, 255)
preto = (0, 0, 0)

fundo = pygame.image.load("bases/fundo.jpg")
fundoStart = pygame.image.load("bases/backgroundStart.jpg")
fundoDead = pygame.image.load("bases/backgroundDead.jpg")

cesta = pygame.image.load("bases/cesta.png")
cesta = pygame.transform.scale(cesta, (145,150)) 
cherry = pygame.image.load("bases/cai.png")
cherry = pygame.transform.scale(cherry, (100,100))

cherrySound = pygame.mixer.Sound("bases/backgroundGame.wav.mp3")
explosaoSound = pygame.mixer.Sound("bases/gameover.wav.mp3")
pygame.mixer.music.load("bases/backgroundGame.wav.mp3")
fonteMenu = pygame.font.SysFont("comicsans",18)

def jogar():
    fundoMov1 = 0
    fundoMov2 = 1070
    posicaoXPersona = 450
    posicaoYPersona = 450
    raioSol = 30
    direcaoSol = 1
    movimentoXPersona  = 0
    velocidadeMovPersona = 5
    posicaoXCherry = random.randint(0,900)
    posicaoYCherry = -100
    velocidadeCherry = 2
    
    pontos = 0
    pygame.mixer.Sound.play(cherrySound)
    pygame.mixer.music.play(-1)
    dificuldade = 20
    pause = False
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
                movimentoXPersona = 0

            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pause = not pause
                print('Pause =' , pause)

            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimentoXPersona = velocidadeMovPersona
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimentoXPersona = -velocidadeMovPersona

            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXPersona = 0

        raioSol += direcaoSol
        if raioSol > 50:
            direcaoSol = -1
        if raioSol < 30:
            direcaoSol = 1  
        
        posicaoXPersona = posicaoXPersona + movimentoXPersona


        if not pause:
            posicaoYCherry = posicaoYCherry + velocidadeCherry
                   
        if posicaoXPersona < 0 :
            posicaoXPersona = 0
        elif posicaoXPersona > 858:
            posicaoXPersona = 858
            
    
                            
        tela.fill(branco)
        tela.blit(fundo, (fundoMov1,0) )
        tela.blit(fundo, (fundoMov2,0) )

        pygame.draw.circle(
            tela,
            (255,255,0),
            (900,80),
            raioSol
        )

        fundoMov1 -= 1
        fundoMov2 -= 1
        if fundoMov1 <= -1129:
            fundoMov1 = 1129
        elif fundoMov2 <= -1129:
            fundoMov2 = 1129
        
        
        tela.blit(cesta, (posicaoXPersona,posicaoYPersona))
        tela.blit(cherry, (posicaoXCherry, posicaoYCherry))

        if pause:

            textoPause = fonteMenu.render(
                'PAUSE',
                True,
                (255,255,255)
            )
            tela.blit(textoPause,(500,350))
            
            textoPauseGame = fonteMenu.render(
                'Press Space to Pause Game',
                True,
                (255,255,255)
            )
            tela.blit(textoPauseGame, (20,560))

        
        texto = fonteMenu.render("Pontos: "+str(pontos), True, branco)
        tela.blit(texto, (850,15))
            
        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona+116))
        pixelsCherryX = list(range(posicaoXCherry, posicaoXCherry + 125))
    
        
        if posicaoYCherry >= 450:

            if len(list(set(pixelsCherryX).intersection(set(pixelsPersonaX)))) > dificuldade:

                pontos = pontos + 1

                posicaoXCherry = random.randint(0,900)
                posicaoYCherry = -100

                velocidadeCherry = velocidadeCherry + 1

            else:

                escreverDados(nome, pontos)
                dead()
        
        
        pygame.display.update()
        relogio.tick(60)

def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
            
        tela.fill(branco)
        tela.blit(fundoDead, (0,0))
        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))


        pygame.display.update()
        relogio.tick(60)



def start():
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
            
        tela.fill(branco)
        tela.blit(fundoStart, (0,0))
        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))
        texto = fonteMenu.render(f"The Best - {nome_maior} - {maior_pontos} - { dataJogada} ", True, branco)
        tela.blit(texto, (480,15))
        

        pygame.display.update()
        relogio.tick(60)
           
start()