import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange
pygame.init()

# diretorios
diretorio_principal = os.path.dirname(__file__)
diretorio_sprites = os.path.join(diretorio_principal, "sprites")
diretorio_musicas = os.path.join(diretorio_principal, "musicas")

# variaveis gerais
largura_tela = 990
meio_largura_tela = largura_tela // 2
altura_tela = 555
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Legends Of The Jungle")
icon = pygame.image.load(os.path.join(diretorio_sprites, "icon-game.png")).convert_alpha()
pygame.display.set_icon(icon)
relogio = pygame.time.Clock()
gameOver = False
pause = False
vida = 6000
pontos = 0  
musica_vitoria_tocada = False 

#baixando sprites
sprite_button = pygame.image.load(os.path.join(diretorio_sprites, "button3.png")).convert_alpha()
sprite_birds = pygame.image.load(os.path.join(diretorio_sprites, "birds.32x32.png")).convert_alpha()
sprite_chao = pygame.image.load(os.path.join(diretorio_sprites, "grass_main_128x128.png")).convert_alpha()
sprite_player_parado = pygame.image.load(os.path.join(diretorio_sprites, "Idle.png")).convert_alpha()
sprite_player_andando = pygame.image.load(os.path.join(diretorio_sprites, "Walk.png")).convert_alpha()
sprite_player_jump = pygame.image.load(os.path.join(diretorio_sprites, "Jump.png")).convert_alpha()
sprite_player_attack = pygame.image.load(os.path.join(diretorio_sprites, "Attack_3_1.png")).convert_alpha()
sprite_player_dead = pygame.image.load(os.path.join(diretorio_sprites, "Dead.png")).convert_alpha()
sprite_medusa_andando = pygame.image.load(os.path.join(diretorio_sprites, "medusa_Walk1.png")).convert_alpha()
sprite_medusa_atacando = pygame.image.load(os.path.join(diretorio_sprites, "medusa_Attack_1.png")).convert_alpha()
sprite_medusa_morrendo = pygame.image.load(os.path.join(diretorio_sprites, "medusa_Dead.png")).convert_alpha()
sprite_lobisomem_andando = pygame.image.load(os.path.join(diretorio_sprites, "lobisomem_walk.png")).convert_alpha()
sprite_lobisomem_atacando = pygame.image.load(os.path.join(diretorio_sprites, "lobisomen_Attack_1.png")).convert_alpha()
sprite_lobisomem_morrendo = pygame.image.load(os.path.join(diretorio_sprites, "lobisomem_Dead.png")).convert_alpha()


#classes
class Birds(pygame.sprite.Sprite):
    def __init__(Self):
        super().__init__()
        Self.sprite = []
        for i in range(5):
                img = sprite_birds.subsurface((i * 32, 0), (32,32))
                img = pygame.transform.scale(img, (32 * 1.5, 32 * 1.5))
                Self.sprite.append(img)
        Self.index_lista = 0
        Self.image = Self.sprite[Self.index_lista]
        Self.rect = Self.image.get_rect()
        Self.rect.x = largura_tela + randrange(20, 450, 50)
        Self.rect.y = randrange(50, 250, 50)

    def update(Self):
        Self.index_lista += 0.09
        if Self.index_lista >= len(Self.sprite):
            Self.index_lista = 0
        Self.image = Self.sprite[int(Self.index_lista)]
        Self.image = pygame.transform.scale(Self.image, (32  * 1.5, 32 * 1.5))
        if Self.rect.topright[0] < 0: 
            Self.rect.x = largura_tela + randrange(20, 450, 50)
            Self.rect.y = randrange(50, 250, 50)
        Self.rect.x -= 4          

class Chao(pygame.sprite.Sprite):
    def __init__(Self, pos_x):
        super().__init__()
        Self.image = sprite_chao
        Self.rect = Self.image.get_rect()
        Self.rect.y = altura_tela - 128
        Self.rect.x = pos_x * 128
        Self.playerAndando = False

class Player(pygame.sprite.Sprite): 
    def __init__(Self, pos_x):
        super().__init__()
        Self.sprite = []
        # [0] até [5]
        for i in range(6):
            img_idle = sprite_player_parado.subsurface((i * 128, 0), (128, 128)).convert_alpha()
            Self.sprite.append(img_idle)
        # [6] até [13]
        for i in range(8):
            img_walk = sprite_player_andando.subsurface((i * 128, 0), (128, 128)).convert_alpha()
            Self.sprite.append(img_walk)
        # [14] até [25]
        for i in range(11, -1, -1):
            img_jump = sprite_player_jump.subsurface((i * 128, 0), (128, 128)).convert_alpha()
            Self.sprite.append(img_jump)
        # [26] até [37]
        for i in range(4):
            img_attack1 = sprite_player_attack.subsurface((i * 128, 0), (128, 128)).convert_alpha()
            Self.sprite.append(img_attack1)
        for i in range(3):
            img_attack2 = sprite_player_attack.subsurface((i * 128, 128), (128, 128)).convert_alpha()
            Self.sprite.append(img_attack2)
        for i in range(5):
            img_attack3 = sprite_player_attack.subsurface((i * 128, 256), (128, 128)).convert_alpha()
            Self.sprite.append(img_attack3)
        #[38] até [41]
        for i in range(4):
            img_dead = sprite_player_dead.subsurface((i * 128, 0), (128, 128)).convert_alpha()
            Self.sprite.append(img_dead)

        Self.index_lista = 0
        Self.image = Self.sprite[Self.index_lista]
        Self.rect = Self.image.get_rect()
        Self.mask = pygame.mask.from_surface(Self.image)
        Self.rect.x = pos_x
        Self.rect.y = altura_tela - 256
        Self.parado = True
        Self.andando = False
        Self.pulando= False
        Self.atacando = False
        Self.morrendo = False
        Self._vely = 0
        Self.gravidade = 0.4
        #mecanica de vida
        Self.vida = 100
        Self.ultimo_dano = 0
        Self.invulneravel = 0
        Self.tempo_invulneravel = 0
        Self.cooldowm_dano = 1000
        #mecanica ataque
        Self.cooldown_ataque = False  
        Self.tempo_ultimo_ataque = 0 
        Self.duracao_cooldown = 5000

    def morreu(Self):
        Self.andando = False
        Self.pulando = False
        Self.parado = False
        if not Self.morrendo:
            Self.morrendo = True

    def andar(Self):
        Self.andando = True
        Self.parado = False
        Self.morrendo = False
        Self.atacando = False

    def atacar(Self):
        tempo_atual = pygame.time.get_ticks()
        if not Self.cooldown_ataque:
            Self.andando = False
            Self.parado = False
            Self.atacando = True
            Self.morrendo = False
            Self.tempo_ultimo_ataque = tempo_atual  
            Self.cooldown_ataque = True  

    def pular(Self):
        Self.parado = False
        Self.atacando = False
        Self.andando = False
        Self.morrendo = False
        if not Self.pulando:
           Self.pulando = True
           Self.vel_y = -10
        Self.index_lista = 14

    def update(Self):
        tempo_atual = pygame.time.get_ticks()        
        if Self.cooldown_ataque and tempo_atual - Self.tempo_ultimo_ataque > Self.duracao_cooldown:
            Self.cooldown_ataque = False

        if Self.morrendo == True:
            if Self.index_lista >  41 or Self.index_lista < 38:
                Self.index_lista = 38
            Self.index_lista += 0.01
            Self.image = Self.sprite[int(Self.index_lista)]
            Self.mask = pygame.mask.from_surface(Self.image)
            if Self.index_lista > 41:
                Self.morrendo = False
        
        if Self.atacando == True and not Self.andando:
            if Self.index_lista > 37 or Self.index_lista < 26:
                Self.index_lista = 26
            Self.index_lista += 0.18  
            Self.image = Self.sprite[int(Self.index_lista)]
            Self.mask = pygame.mask.from_surface(Self.image)

            if Self.index_lista >= 37:
                Self.atacando = False
                Self.parado = True
        
        if Self.parado == True:
            if Self.index_lista > 5:
                Self.index_lista = 0
            Self.index_lista += 0.25
            Self.image = Self.sprite[int(Self.index_lista)]
            Self.mask = pygame.mask.from_surface(Self.image)
            
        if Self.andando == True and not Self.pulando:
            if Self.index_lista > 13 or Self.index_lista < 6:
                Self.index_lista = 6
            Self.index_lista += 0.15
            Self.image = Self.sprite[int(Self.index_lista)]
            Self.mask = pygame.mask.from_surface(Self.image)
            if pygame.key.get_pressed()[K_a]:
                if Self.rect.center[0] > 12:
                    Self.rect.x -= 2
            else:
                Self.parado = True
                Self.andando = False
                pass
            if pygame.key.get_pressed()[K_d]:
                if Self.rect.x < largura_tela:
                    Self.rect.x += 2
                if Self.rect.topright[0] >= largura_tela + 128:
                    Self.rect.x = 0 - 128
            else:
                Self.parado = True
                Self.andando = False
                pass

        if Self.pulando:
            Self.index_lista += 0.25
            if Self.index_lista > 25 or Self.index_lista < 14:
                Self.index_lista = 14
            Self.image = Self.sprite[int(Self.index_lista)]
            Self.mask = pygame.mask.from_surface(Self.image)
            Self.vel_y += Self.gravidade  # Aplica gravidade
            Self.rect.y += Self.vel_y  # Atualiza a posição vertical

            # Verifica se o jogador atingiu o chão
            if Self.rect.y >= altura_tela - 256:
                Self.rect.y = altura_tela - 256
                Self.pulando = False
                Self.vel_y = 0
                Self.parado = True
            
            if pygame.key.get_pressed()[K_a]:
                if Self.rect.center[0] > 12:
                    Self.rect.x -= 3
            if pygame.key.get_pressed()[K_d]:
                if Self.rect.x < largura_tela:
                    Self.rect.x += 3
                if Self.rect.topright[0] >= largura_tela + 128:
                    Self.rect.x = 0 - 128

class Monstros(pygame.sprite.Sprite):
    def __init__(Self, tipo):
        super().__init__()
        Self.tipo = tipo
        if Self.tipo == "medusa":
            Self.sprite = []
            #[0] até [12]
            for i in range(13):
                img_walk = sprite_medusa_andando.subsurface((i * 128, 0),(128, 128)).convert_alpha()
                Self.sprite.append(img_walk)
            #[13] até [28]
            for i in range(16):
                img_attack = sprite_medusa_atacando.subsurface((i * 128, 0), (128, 128)).convert_alpha()
                Self.sprite.append(img_attack)
            #[29] até [31]
            for i in range(2, -1, -1):
                img_dead = sprite_medusa_morrendo.subsurface((i * 128, 0),(128, 128)).convert_alpha()
                Self.sprite.append(img_dead)
        elif Self.tipo == "lobisomem":
            Self.sprite = []
            #[0] até [10]
            for i in range(11):
                img_walk = sprite_lobisomem_andando.subsurface((i * 128, 0),(128, 128)).convert_alpha()
                Self.sprite.append(img_walk)
            #[11] até [16]
            for i in range(5, -1, -1):
                img_attack = sprite_lobisomem_atacando.subsurface((i * 128, 0), (128, 128)).convert_alpha()
                Self.sprite.append(img_attack)
            #[17] até [18]
            for i in range(1, -1, -1):
                img_dead = sprite_lobisomem_morrendo.subsurface((i * 128, 0),(128, 128)).convert_alpha()
                Self.sprite.append(img_dead)

        Self.index_lista = 0
        Self.image = Self.sprite[Self.index_lista]
        Self.rect = Self.image.get_rect()
        Self.mask = pygame.mask.from_surface(Self.image)
        if Self.tipo == "lobisomem":
            Self.rect.x = largura_tela + randrange(100, 900, 100)
        elif Self.tipo == "medusa":
            Self.rect.x = largura_tela + randrange(200, 1000, 300)
        Self.rect.y = altura_tela - 256
        Self.atacando = False
        Self.andando = True
        Self.morrendo = False
        Self.morto = False  # Adicionado para controlar se o monstro já foi pontuado

    def morreu(Self):
        Self.atacando = False
        Self.andando = False
        if not Self.morrendo:
            Self.morrendo = True
            Self.morto = False  # Inicializa como False

    def update(Self):
        if Self.morrendo:
            Self.index_lista += 0.25
            if Self.index_lista > len(Self.sprite) - 1 or Self.index_lista < len(Self.sprite) - 3:
                Self.index_lista = len(Self.sprite) - 3
            Self.image = Self.sprite[int(Self.index_lista)]
            Self.mask = pygame.mask.from_surface(Self.image)
            if Self.index_lista >= len(Self.sprite) - 1:
                Self.rect.x = largura_tela + randrange(100, 800, 200)
                Self.morrendo = False
                Self.andando = True 
                Self.index_lista = 0  
                
        if Self.andando:
            Self.index_lista += 0.25
            if Self.index_lista > 12:
                Self.index_lista = 0
            Self.image = Self.sprite[int(Self.index_lista)]
            Self.mask = pygame.mask.from_surface(Self.image)
            if Self.rect.topright[0] < 0: 
                Self.rect.x = largura_tela + randrange(150, 900, 150)
            Self.rect.x -= 3.5
        
#funções para o jogo
def iniciar_gameplay():
    global menu, musica_game, gameOver, pontos, musica_vitoria_tocada
    jogador.morrendo = False
    jogador.parado = True
    jogador.rect.x = 100
    jogador.rect.y = altura_tela - 256
    jogador.vida = 100
    for inimigo in todos_inimigos:
        inimigo.rect.x = largura_tela + randrange(100, 800, 200)
        inimigo.morrendo = False
        inimigo.morto = False
    
    menu = False
    gameOver = False
    pontos = 0  # Reseta a pontuação
    musica_vitoria_tocada = False  # Reseta a música de vitória
    musica_game = pygame.mixer.music.load(os.path.join(diretorio_musicas, "jungle.mp3"))
    musica_game = pygame.mixer.music.play(-1)

def morreu():
    global musica_gameOver
    musica_gameOver = pygame.mixer.music.load(os.path.join(diretorio_musicas, "Once-Upon-a-Time.mp3"))
    musica_gameOver = pygame.mixer.music.play(-1)

def mostra_vida(tela, vida):
    fonte_vida = pygame.font.SysFont("pixeledregular", 20, True, False) 
    texto_vida = fonte_vida.render(f'Vida: {vida}', False, (255, 0, 0))
    tela.blit(texto_vida, (10,10))

def mostra_cooldown(tela, tempo):
    fonte_cooldown = pygame.font.SysFont("pixeledregular", 20, True, False)
    if tempo > 0:
        texto_cooldown = fonte_cooldown.render(f"Ataque: {tempo // 1000}", False, (255, 0, 0))
    else:
        texto_cooldown = fonte_cooldown.render("Ataque carregado.", False, (0, 255, 0))
    tela.blit(texto_cooldown, (10, 50))

def tela_vitoria(tela):
    global musica_vitoria_tocada
    if not musica_vitoria_tocada:
        pygame.mixer.music.load(os.path.join(diretorio_musicas, "vitoria.mp3"))  # Carrega a música de vitória
        pygame.mixer.music.play(-1)  # Toca a música em loop
        musica_vitoria_tocada = True

    tela.fill((0, 0, 0))  # Preenche a tela com preto

    # Texto de vitória
    fonte_vitoria = pygame.font.SysFont('pixeledregular', 50, True, False)
    mensagem_vitoria = fonte_vitoria.render("VITÓRIA!", False, (0, 255, 0))
    tela.blit(mensagem_vitoria, (meio_largura_tela - mensagem_vitoria.get_width() // 2, altura_tela // 2 - 150))
    # Texto para reiniciar o jogo
    fonte_reiniciar = pygame.font.SysFont('pixeledregular', 25, True, False)
    mensagem_reiniciar = fonte_reiniciar.render("Aperte 'r' para jogar novamente", False, (255, 255, 255))
    tela.blit(mensagem_reiniciar, (meio_largura_tela - mensagem_reiniciar.get_width() // 2, altura_tela // 2 + 50))

    pygame.display.flip()

# config. imagem de fundo do menu
fundo_menu = pygame.image.load(os.path.join(diretorio_sprites, "fundo-menu.jpg")).convert()
fundo_menu = pygame.transform.scale(fundo_menu, (largura_tela, altura_tela))
menu = True

#config. imagem de fundo durante game
fundo_game = pygame.image.load(os.path.join(diretorio_sprites, "fundo_game.png")).convert()
fundo_game = pygame.transform.scale(fundo_game, (largura_tela, altura_tela))

#texto menu
mensagem = "Pressione 'z' para começar"
fonte_menu = pygame.font.SysFont('pixeledregular', 17, True, False)
start_formatado = fonte_menu.render(mensagem, False, (160, 42, 45))

#musica menu
pygame.mixer.music.set_volume(0.4)
musica_menu = pygame.mixer.music.load(os.path.join(diretorio_musicas, "overworld-day.mp3"))
musica_menu = pygame.mixer.music.play(-1)

#Objetos
todas_as_sprites = pygame.sprite.Group()
for i in range(3):
    bird = Birds()
    todas_as_sprites.add(bird)

for i in range((largura_tela*2) // 128):
    chao = Chao(i)
    todas_as_sprites.add(chao)

jogador = Player(100)
todas_as_sprites.add(jogador)
todos_inimigos = pygame.sprite.Group()
for i in range(3):
    medusa = Monstros("medusa")
    todas_as_sprites.add(medusa)
    todos_inimigos.add(medusa)
for i in range(2):
    lobisomem = Monstros("lobisomem")
    todas_as_sprites.add(lobisomem)
    todos_inimigos.add(lobisomem)

#Loop principal
rodando = True
while rodando:
    #Tela menu
    while menu:
        tela.blit(fundo_menu, (0,0))
        tela.blit(icon, (meio_largura_tela - icon.get_width() // 2, 20))
        tela.blit(sprite_button, (meio_largura_tela - sprite_button.get_width() // 2, 340))
        tela.blit(start_formatado, (meio_largura_tela - (start_formatado.get_width() - 10) // 2, 375))
        for event in pygame.event.get():
            if event.type == QUIT:
                rodando = False
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_z:
                    iniciar_gameplay()
        pygame.display.flip()
    
    # configura fps, fundo durante jogatina e mostra a vida do jogador
    relogio.tick(45)
    tela.blit(fundo_game, (0, 0))
    mostra_vida(tela, jogador.vida)
    
    # Exibe a pontuação
    fonte_pontos = pygame.font.SysFont("pixeledregular", 20, True, False)
    texto_pontos = fonte_pontos.render(f'Pontos: {pontos}', False, (255, 255, 255))
    tela.blit(texto_pontos, (largura_tela - texto_pontos.get_width() - 30, 10))
    
    # configura o cooldown do ataque
    tempo_atual = pygame.time.get_ticks()
    tempo_restante = max(0, jogador.duracao_cooldown - (tempo_atual - jogador.tempo_ultimo_ataque))
    mostra_cooldown(tela, tempo_restante)
    
    # analise de ocorrencia de evento do loop principal
    for event in pygame.event.get():
        if event.type == QUIT:
            rodando = False
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_f:
                jogador.atacar()
            if event.key == K_SPACE:
                jogador.pular()
            if event.key == K_p:
                pause = True

    # verifica movimentação
    if pygame.key.get_pressed()[K_a]:
        jogador.andar()
    if pygame.key.get_pressed()[K_d]:
        jogador.andar()

    # verifica se o jogador está invulneravel e contabiliza o tempo 
    if jogador.invulneravel:
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - jogador.tempo_invulneravel > jogador.cooldowm_dano:
            jogador.invulneravel = False

    #atualiza o metodo update de todas as sprites
    todas_as_sprites.update()

    #determina a colisao
    colisoes = pygame.sprite.spritecollide(jogador, todos_inimigos, False, pygame.sprite.collide_mask)
    if colisoes:
        if jogador.atacando == True: 
            for inimigo in colisoes:
                if not inimigo.morrendo:
                    inimigo.morreu()  # Coloca o monstro no estado de "morrendo"
                elif inimigo.morrendo and not inimigo.morto:  # Verifica se o monstro está morrendo e ainda não foi pontuado
                    pontos += 1  # Incrementa a pontuação
                    inimigo.morto = True  # Marca o monstro como morto e pontuado
            todas_as_sprites.update()
        else:
            tempo_atual = pygame.time.get_ticks()
            if not jogador.invulneravel:
               jogador.vida -= 10
               jogador.invulneravel = True
               jogador.tempo_invulneravel = tempo_atual
               if jogador.vida <= 0:
                   morreu()
                   jogador.morreu()
                   gameOver = True

    # Verifica se o jogador venceu // tela de vitória
    while pontos >= 15:
        tela_vitoria(tela)
        for event in pygame.event.get():
            if event.type == QUIT:
                rodando = False
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    iniciar_gameplay()
    else:
        todas_as_sprites.draw(tela)
        pygame.display.flip()

    #Caso o jogador aperte 'p'
    while pause:
        #texto pause
        fonte_pause = pygame.font.SysFont("pixeledregular", 25, True, False)
        mensagem_pause = fonte_pause.render("PAUSE", False, (255, 0, 0))
        tela.blit(mensagem_pause, (meio_largura_tela - mensagem_pause.get_width() // 2, altura_tela // 2 - 150))

        #texto tirar pause
        fonte_guia_pause = pygame.font.SysFont('pixeledregular', 25, True, False)
        mensagem_voltar_pause = fonte_guia_pause.render("Aperte 'p' para voltar", False, (255, 0, 0))
        tela.blit(mensagem_voltar_pause, (meio_largura_tela - mensagem_voltar_pause.get_width() // 2, altura_tela // 2))
        for event in pygame.event.get():
            if event.type == QUIT:
                rodando = False
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_p:
                    pause = False
        
        pygame.display.flip()

    #Tela de gameOver
    while gameOver:
        tela.fill((0, 0, 0))  # Preenche a tela com preto
        jogador.update() 
        tela.blit(jogador.image, jogador.rect)
        # Texto Game Over
        fonte_game_over = pygame.font.SysFont('pixeledregular', 50, True, False)
        mensagem_game_over = fonte_game_over.render("GAME OVER", False, (255, 0, 0))
        tela.blit(mensagem_game_over, (meio_largura_tela - mensagem_game_over.get_width() // 2, altura_tela // 2 - 150))

        # Texto para reiniciar o jogo
        fonte_reiniciar = pygame.font.SysFont('pixeledregular', 25, True, False)
        mensagem_reiniciar = fonte_reiniciar.render("Aperte 'r' para recomeçar", False, (255, 255, 255))
        tela.blit(mensagem_reiniciar, (meio_largura_tela - mensagem_reiniciar.get_width() // 2, altura_tela // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                rodando = False
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    iniciar_gameplay()
                    gameOver = False
