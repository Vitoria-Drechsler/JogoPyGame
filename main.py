import pygame
import random
import pyttsx3
from recursos.funcoes import inicializarBancoDeDados, limpar_tela, escreverDados, maior_pontuador
from recursos.trabalho import moverNuvem

limpar_tela()
inicializarBancoDeDados()
nome_maior, maior_pontos, dataJogada, horaJogada = maior_pontuador()
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
fundoStart = pygame.image.load("bases/inicio.png")
fundoBoasvindas = pygame.image.load("bases/boasvindas.png")
fundoFim = pygame.image.load("bases/fim.png")

cesta = pygame.image.load("bases/cesta.png")
cesta = pygame.transform.scale(cesta, (145,150)) 
cherry = pygame.image.load("bases/cai.png")
cherry = pygame.transform.scale(cherry, (100,100))

nuvem = pygame.image.load('bases/nuvem.png')
nuvem = pygame.transform.scale(nuvem, (180,180))

cherrySound = pygame.mixer.Sound("bases/backgroundGame.wav.mp3")
explosaoSound = pygame.mixer.Sound("bases/gameover.wav.mp3")
pygame.mixer.music.load("bases/backgroundGame.wav.mp3")
fonteMenu = pygame.font.SysFont("comicsans",18)
fonteRecorde = pygame.font.SysFont('cambria',28)

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
    posicaoXNuvem = 150
    
    pontos = 0
    pygame.mixer.Sound.play(cherrySound)
    pygame.mixer.music.play(-1)
    dificuldade = 20
    pause = False
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pause = not pause
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

        posicaoXPersona = posicaoXPersona + movimentoXPersona

        raioSol += direcaoSol
        if raioSol > 50:
            direcaoSol = -1
        if raioSol < 30:
            direcaoSol = 1  
        
        posicaoXNuvem = moverNuvem (posicaoXNuvem)

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

        tela.blit(nuvem, (posicaoXNuvem,50))

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
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    quit()

        tela.blit(fundoFim, (0,0))

        textoRecorde = fonteRecorde.render(
            f"Recorde: {nome_maior} - {maior_pontos} pontos",
            True,
            (0,0,0)
        )       

        tela.blit(textoRecorde,(325,320))

        pygame.display.update()
        relogio.tick(60)

def boasVindas():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint (evento.pos):
                    larguraButtonStart = 210
                    alturaButtonStart = 45
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    jogar()
        tela.fill(branco)
        tela.blit(fundoBoasvindas,(0,0))

        textoNome = fonteRecorde.render(
            f" {nome}",
            True,
            preto
        )
        tela.blit(textoNome, (400,200))

        textoRecorde = fonteMenu.render(
            f"{nome_maior} - {maior_pontos} pontos",
            True,
            preto
        )
        tela.blit(textoRecorde, (190, 535))

        textoData = fonteMenu.render(
            f"{dataJogada}",
            True,
            preto
        )
        tela.blit(textoData, (470,535))
        textoHora = fonteMenu.render(
            f"{horaJogada}",
            True,
            preto
        )
        tela.blit(textoHora, (700,535))

        startButton = pygame.Rect(
            390,
            630,
            220,
            50
        )


        pygame.display.update()
        relogio.tick(60)

def start():
    falou = False
    larguraButtonStart = 150
    alturaButtonStart  = 40
    startButton = pygame.Rect(20,35,190,50)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    boasVindas()
                
            
        tela.fill(branco)
        tela.blit(fundoStart, (0,0))

        texto = fonteMenu.render(f"The Best - {nome_maior} - {maior_pontos} - { dataJogada} ", True, branco)
        tela.blit(texto, (690,15))

        pygame.display.update()
        relogio.tick(60)

        if not falou:
            motor = pyttsx3.init()
            motor.say("Bem vindo ao jogo Caça Cerejas")
            motor.runAndWait()
            falou = True

falouInicio = False

start()