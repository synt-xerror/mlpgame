import pygame
import sys

# Inicializando o Pygame
pygame.init()

# Definindo o tamanho da tela e cores
LARGURA, ALTURA = 800, 600
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)

# Configuração da tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pinkie Game - Menu")

# Função para exibir texto na tela
def exibir_texto(texto, tamanho, cor, x, y):
    fonte = pygame.font.Font(None, tamanho)
    texto_renderizado = fonte.render(texto, True, cor)
    tela.blit(texto_renderizado, (x, y))

# Função para a tela de loading
def tela_loading():
    # Definir o tempo de loading (em milissegundos)
    tempo_loading = pygame.time.get_ticks() + 500  # Exibe por 1 segundos
    while pygame.time.get_ticks() < tempo_loading:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Preencher a tela com cor preta
        tela.fill(PRETO)

        # Exibir a mensagem de loading
        exibir_texto("Carregando...", 60, BRANCO, LARGURA // 2 - 150, ALTURA // 2 - 50)

        pygame.display.update()

music = pygame.mixer.Sound("game/sons/menu.mp3")
music.play()

# Função para o menu
def menu():
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Preencher a tela de branco
        tela.fill(BRANCO)

        # Exibindo opções de menu
        exibir_texto("Pinkie Game", 60, PRETO, LARGURA // 2 - 150, ALTURA // 4 - 50)
        
        # Botão "Iniciar Jogo"
        botao_iniciar = pygame.Rect(LARGURA // 2 - 100, ALTURA // 2 - 50, 200, 50)
        pygame.draw.rect(tela, VERDE, botao_iniciar)
        exibir_texto("Iniciar Jogo", 40, BRANCO, LARGURA // 2 - 90, ALTURA // 2 - 40)
        
        # Botão "Sair"
        botao_sair = pygame.Rect(LARGURA // 2 - 100, ALTURA // 2 + 50, 200, 50)
        pygame.draw.rect(tela, VERMELHO, botao_sair)
        exibir_texto("Sair", 40, BRANCO, LARGURA // 2 - 25, ALTURA // 2 + 60)

        # Verificando o clique do mouse
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if botao_iniciar.collidepoint(evento.pos):
                music.stop()
                tela_loading()  # Exibe a tela de loading antes de iniciar o jogo
                import jogo  # Supondo que o módulo jogo tenha uma função 'iniciar_jogo'
                jogo.iniciar_jogo()
                rodando = False
            
            if botao_sair.collidepoint(evento.pos):
                pygame.quit()
                sys.exit()

        pygame.display.update()

# Executando o menu
menu()
