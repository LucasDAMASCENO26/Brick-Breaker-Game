import pygame

# inicializar
pygame.init()

tamanho_tela = (800, 800)
tela = pygame.display.set_mode(tamanho_tela)
pygame.display.set_caption("Brick Breaker")

tamanho_bola = 15
bola = pygame.Rect(100, 500, tamanho_bola, tamanho_bola)
tamanho_jogador = 100
jogador = pygame.Rect(0, 750, tamanho_jogador, 15)

qtde_blocos_linha = 8
qtde_linhas_blocos = 10
qtde_total_blocos = (qtde_blocos_linha * qtde_linhas_blocos)

def criar_blocos(qtde_blocos_linha, qtde_linhas_blocos):
    altura_tela = tamanho_tela[1]
    largura_tela = tamanho_tela[0]
    distancia_entre_blocos = 5
    largura_bloco = largura_tela / qtde_blocos_linha - distancia_entre_blocos
    altura_bloco = 15
    distancia_entre_linhas = altura_bloco + 10

    blocos = []
    # criar os blocos
    for j in range(qtde_linhas_blocos):
        for i in range(qtde_blocos_linha):
            # criar o bloco
            bloco = pygame.Rect(i * (largura_bloco + distancia_entre_blocos), j * distancia_entre_linhas, largura_bloco, altura_bloco)
            # adicionar o bloco na lista de blocos 
            blocos.append(bloco)

    return blocos


cores = {
    "branca": (255, 255, 255),
    "preta": (0, 0, 0),
    "amarela": (255, 255, 0),
    "azul": (0, 0, 255),
    "vermelho": (255, 0, 0),
    "verde": (0, 255, 0),
    "laranja": (255, 165, 0),
    "roxo": (128, 0, 128)
}
fim_jogo = False
pontuacao = 0
movimento_bola = [5, -5]  # Ajuste a velocidade da bola
jogo_ativo = False
vitoria = False

# criar as funções do jogo

# desenhar as coisas na tela 
def desenhar_inicio_jogo():
    tela.fill(cores["preta"])
    fonte = pygame.font.Font(None, 74)
    texto = fonte.render("Brick Breaker", 1, cores["verde"])
    texto_rect = texto.get_rect(center=(tamanho_tela[0] / 2, tamanho_tela[1] / 2 - 50))
    tela.blit(texto, texto_rect)

    fonte_menor = pygame.font.Font(None, 36)
    texto_menor = fonte_menor.render("Pressione ENTER para começar", 1, cores["azul"])
    texto_menor_rect = texto_menor.get_rect(center=(tamanho_tela[0] / 2, tamanho_tela[1] / 2 + 50))
    tela.blit(texto_menor, texto_menor_rect)

    texto_autor = fonte_menor.render("Criado por Lucas Santos", 1, cores["vermelho"])
    texto_autor_rect = texto_autor.get_rect(center=(tamanho_tela[0] / 2, tamanho_tela[1] - 50))
    tela.blit(texto_autor, texto_autor_rect)

def desenhar_fim_jogo(pontos):
    tela.fill(cores["preta"])
    fonte = pygame.font.Font(None, 74)
    texto = fonte.render("Game Over", 1, cores["vermelho"])
    texto_rect = texto.get_rect(center=(tamanho_tela[0] / 2, tamanho_tela[1] / 2 - 50))
    tela.blit(texto, texto_rect)

    fonte_menor = pygame.font.Font(None, 36)
    texto_pontos = fonte_menor.render(f"Pontuação: {pontos}", 1, cores["amarela"])
    texto_pontos_rect = texto_pontos.get_rect(center=(tamanho_tela[0] / 2, tamanho_tela[1] / 2))
    tela.blit(texto_pontos, texto_pontos_rect)

    texto_menor = fonte_menor.render("Pressione ENTER para tentar novamente", 1, cores["azul"])
    texto_menor_rect = texto_menor.get_rect(center=(tamanho_tela[0] / 2, tamanho_tela[1] / 2 + 50))
    tela.blit(texto_menor, texto_menor_rect)

def desenhar_vitoria(pontos):
    tela.fill(cores["preta"])
    fonte = pygame.font.Font(None, 74)
    texto = fonte.render("Você Venceu!", 1, cores["branca"])
    texto_rect = texto.get_rect(center=(tamanho_tela[0] / 2, tamanho_tela[1] / 2 - 50))
    tela.blit(texto, texto_rect)

    fonte_menor = pygame.font.Font(None, 36)
    texto_pontos = fonte_menor.render(f"Pontuação: {pontos}", 1, cores["branca"])
    texto_pontos_rect = texto_pontos.get_rect(center=(tamanho_tela[0] / 2, tamanho_tela[1] / 2))
    tela.blit(texto_pontos, texto_pontos_rect)

    texto_menor = fonte_menor.render("Pressione ENTER para tentar novamente", 1, cores["branca"])
    texto_menor_rect = texto_menor.get_rect(center=(tamanho_tela[0] / 2, tamanho_tela[1] / 2 + 50))
    tela.blit(texto_menor, texto_menor_rect)

def desenhar_jogo():
    tela.fill(cores["preta"])
    pygame.draw.rect(tela, cores["azul"], jogador)
    pygame.draw.rect(tela, cores["branca"], bola)
    desenhar_blocos(blocos)

def desenhar_blocos(blocos):
    for bloco in blocos:
        pygame.draw.rect(tela, cores["verde"], bloco)

# criar as funçoes do jogo
def movimentar_jogador(teclas_pressionadas):
    if teclas_pressionadas[pygame.K_RIGHT]:
        if (jogador.x + tamanho_jogador) < tamanho_tela[0]:
            jogador.x = jogador.x + 10
    if teclas_pressionadas[pygame.K_LEFT]:
        if jogador.x > 0:
            jogador.x = jogador.x - 10

def movimentar_bola(bola):
    movimento = movimento_bola
    bola.x = bola.x + movimento[0]
    bola.y = bola.y + movimento[1]

    if bola.x <= 0:
        movimento[0] = - movimento[0]
    if bola.y <= 0:
        movimento[1] = - movimento[1]
    if bola.x + tamanho_bola >= tamanho_tela[0]:
        movimento[0] = - movimento[0]
    if bola.y + tamanho_bola >= tamanho_tela[1]:
        movimento[1] = - movimento[1]
        return None

    if jogador.collidepoint(bola.x, bola.y):
        movimento[1] = - movimento[1]
    for bloco in blocos:
        if bloco.collidepoint(bola.x, bola.y):
            blocos.remove(bloco)
            movimento[1] = - movimento[1]
    return movimento

def atualizar_pontuacao():
    fonte = pygame.font.Font(None, 30)
    texto = fonte.render(f"Pontuação: {qtde_total_blocos - len(blocos)}", 1, cores["amarela"])
    tela.blit(texto, (0, 780))

def reiniciar_jogo():
    global bola, jogador, blocos, movimento_bola, jogo_ativo, vitoria, pontuacao
    bola = pygame.Rect(100, 500, tamanho_bola, tamanho_bola)
    jogador = pygame.Rect(0, 750, tamanho_jogador, 15)
    blocos = criar_blocos(qtde_blocos_linha, qtde_linhas_blocos)
    movimento_bola = [5, -5]  # Ajuste a velocidade da bola
    jogo_ativo = True
    vitoria = False
    pontuacao = 0

blocos = criar_blocos(qtde_blocos_linha, qtde_linhas_blocos)

# loop principal do jogo
while True:
    teclas_pressionadas = pygame.key.get_pressed()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
            if not jogo_ativo:
                reiniciar_jogo()

    if not jogo_ativo:
        if vitoria:
            desenhar_vitoria(qtde_total_blocos - len(blocos))
        elif fim_jogo:
            desenhar_fim_jogo(qtde_total_blocos - len(blocos))
        else:
            desenhar_inicio_jogo()
    else:
        movimentar_jogador(teclas_pressionadas)
        movimento_bola = movimentar_bola(bola)
        if not movimento_bola:
            fim_jogo = True
            jogo_ativo = False

        if len(blocos) == 0:
            vitoria = True
            jogo_ativo = False

        desenhar_jogo()
        atualizar_pontuacao()

    # Atualizar a tela
    pygame.display.update()

    # Controlar a taxa de atualização do jogo
    pygame.time.Clock().tick(60)
