import pygame
import sys
import random
import os
import time

# Centralizar a janela do jogo
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Inicialização do Pygame
pygame.init()

# Inicialização dos sons
pygame.mixer.init()
nomnom = pygame.mixer.Sound("game/sons/nomnom.mp3")
nomnom.set_volume(0.8)

youwin = pygame.mixer.Sound("game/sons/win.mp3")
youwin.set_volume(1)

music = pygame.mixer.Sound("game/sons/music.mp3")
music.play()

yay = pygame.mixer.Sound("game/sons/yay.mp3")
yay.set_volume(3)

# Configuração da tela
tela = pygame.display.set_mode((1152, 648))
pygame.display.set_caption('Pinkie Game')

# Cor e fundo
BACKGROUND = pygame.image.load('game/imagens/torrao-de-acucar.png')
WINNER = pygame.image.load('game/imagens/winner.jpg')
BRANCO = (255, 255, 255)  # 
PRETO = (0, 0, 0)
KIDS = pygame.image.load('game/imagens/yay.png')

# Posição do jogador
x, y = 640, 360

# Velocidade
velocidade = 5

# Carregar imagens do jogador
jogador_imagem_d = pygame.image.load('game/imagens/pinkie.png')
jogador_imagem_e = pygame.image.load('game/imagens/pinkie2.png')
jogador_imagem = jogador_imagem_d

jogador_rect = jogador_imagem.get_rect()

# Carregar imagens dos objetos (cupcakes)
objetos_imagens = []
objetos_rects = []
for i in range(5):
    imagem = pygame.image.load('game/imagens/cupcake.png')
    rect = imagem.get_rect()
    rect.x = random.randint(0, 1151 - rect.width)
    rect.y = random.randint(0, 647 - rect.height)
    objetos_imagens.append(imagem)
    objetos_rects.append(rect)

# Configuração do relógio
clock = pygame.time.Clock()

# Fonte para o texto de vitória
fonte = pygame.font.Font(None, 74)
texto_completo = fonte.render("Parabéns! Você venceu!", True, BRANCO)
texto_rect = texto_completo.get_rect(center=(576, 320))  # Ajustado para centralizar melhor

# Função para verificar colisão
def colidiu(rect1, rect2):
    return rect1.colliderect(rect2)

# Controlar cooldown do som
ultimo_som_tocado = 0
cooldown_som = 300  

# Tutorial
fonte = pygame.font.Font(None, 50)
texto1 = "Para se mover: use WASD ou as setas direcionais."

textoup = fonte.render("Para se mover:", True, PRETO)
textoup_rect = textoup.get_rect()
textoup_rect.bottomright = (1152 - 10, 648 - 40) 

textodown = fonte.render("use WASD ou as setas direcionais.", True, PRETO)
textodown_rect = textodown.get_rect()
textodown_rect.bottomright = (1152 - 10, 648 - 10) 

tutorial_ativo = True  # Variável para controlar a exibição do tutorial

# Exibir o tutorial enquanto tutorial_ativo for True
if tutorial_ativo:
    tela.blit(BACKGROUND, (0, 0))  # Desenha o fundo
    tela.blit(textoup, textoup_rect)  # Desenha a primeira linha do tutorial
    tela.blit(textodown, textodown_rect)  # Desenha a segunda linha do tutorial
    pygame.display.flip()  # Atualiza a tela
    # Verificar se o tempo do tutorial acabou

# Loop principal do jogo
def iniciar_jogo():
    global x, y, jogador_imagem, jogador_rect, objetos_imagens, objetos_rects, ultimo_som_tocado

    game = True

    while game:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                game = False

        # Movimentação do jogador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            x -= velocidade
            jogador_imagem = jogador_imagem_e
            tutorial_ativo = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x += velocidade
            tutorial_ativo = False
            jogador_imagem = jogador_imagem_d
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            y -= velocidade
            tutorial_ativo = False
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            y += velocidade
            tutorial_ativo = False

        # Evita que o jogador saia da tela
        x = max(0, min(1152 - jogador_rect.width, x))
        y = max(0, min(648 - jogador_rect.height, y))
        jogador_rect.topleft = (x, y)

        # Fundo
        tela.blit(BACKGROUND, (0, 0))

        # Desenhar os objetos (cupcakes)
        tempo_atual = pygame.time.get_ticks()
        for i in range(len(objetos_rects) - 1, -1, -1):
            tela.blit(objetos_imagens[i], objetos_rects[i])
            if colidiu(jogador_rect, objetos_rects[i]):
                if tempo_atual - ultimo_som_tocado > cooldown_som:
                    nomnom.play()
                    ultimo_som_tocado = tempo_atual
                del objetos_imagens[i]
                del objetos_rects[i]

        # Desenhar jogador
        tela.blit(jogador_imagem, jogador_rect.topleft)

        pygame.display.flip()
        clock.tick(60)

        # Verificar vitória
        if not objetos_rects:
            music.stop()
            tempo_inicio = pygame.time.get_ticks()  # Marca o tempo inicial
            tela.blit(WINNER, (0, 0))
            youwin.play()
            tela.blit(texto_completo, texto_rect)
            pygame.display.flip()

            # Espera 1 segundo sem travar o jogo
            while pygame.time.get_ticks() - tempo_inicio < 2000:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            tempo_inicio = pygame.time.get_ticks()  # Reinicia o tempo

            tela.blit(KIDS, (400, 100))
            yay.play()
            pygame.display.flip()

            # Espera 2 segundos sem travar o jogo
            while pygame.time.get_ticks() - tempo_inicio < 2000:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            # Espera mais 6 segundos antes de fechar
            tempo_inicio = pygame.time.get_ticks()
            while pygame.time.get_ticks() - tempo_inicio < 4000:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            pygame.quit()
            sys.exit()

# Iniciar o jogo
iniciar_jogo()
