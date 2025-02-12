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

# variaveis tela
largura_tela = 990
meio_largura_tela = largura_tela // 2
altura_tela = 555
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Legends Of The Jungle")
icon = pygame.image.load(os.path.join(diretorio_sprites, "icon-game.png")).convert_alpha()
pygame.display.set_icon(icon)


#baixando sprites
sprite_birds = pygame.image.load(os.path.join(diretorio_sprites, "birds.32x32.png")).convert_alpha()
sprite_chao = pygame.image.load(os.path.join(diretorio_sprites, "grass_main_128x128.png")).convert_alpha()
sprite_player_parado = pygame.image.load(os.path.join(diretorio_sprites, "Idle.png")).convert_alpha()
sprite_player_andando = pygame.image.load(os.path.join(diretorio_sprites, "Walk.png")).convert_alpha()
sprite_player_jump = pygame.image.load(os.path.join(diretorio_sprites, "Jump.png")).convert_alpha()
sprite_player_attack = pygame.image.load(os.path.join(diretorio_sprites, "Attack_3_1.png")).convert_alpha()
sprite_medusa_andando = pygame.image.load(os.path.join(diretorio_sprites, "medusa_Walk.png")).convert_alpha()
sprite_medusa_atacando = pygame.image.load(os.path.join(diretorio_sprites, "medusa_Attack_1.png")).convert_alpha()



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
            Self.rect.y = randrange(50, 250, 30) 
        Self.rect.x -= 4 

class Chao(pygame.sprite.Sprite):
    def __init__(Self, pos_x):
        super().__init__()
        Self.image = sprite_chao
        Self.rect = Self.image.get_rect()
        Self.rect.y = altura_tela - 128
        Self.rect.x = pos_x * 128
        Self.playerAndando = False
    '''def update(Self):
        if Self.rect.topright[0] < 0:
            Self.rect.x = largura_tela
        Self.rect.x -= 4'''

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
        for i in range(12):
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
        Self._vely = 0
        Self.gravidade = 0.4




    def andar(Self):
        Self.andando = True
        Self.parado = False

    def atacar(Self):
        Self.andando = False
        Self.parado = False
        Self.atacando = True

    def pular(Self):
        Self.parado = False
        Self.atacando = False
        Self.andando = False
        if not Self.pulando:
           Self.pulando = True
           Self.vel_y = -10


    def update(Self):
        if Self.atacando == True:
            if pygame.key.get_pressed()[K_f]:
                if Self.index_lista > 37 or Self.index_lista < 26:
                    Self.index_lista = 26
                Self.index_lista += 0.18
                Self.image = Self.sprite[int(Self.index_lista)]
                Self.mask = pygame.mask.from_surface(Self.image)
            else:
                Self.parado = True
                Self.atacando = False
                pass
        
        if Self.parado == True:
            if Self.index_lista > 5:
                Self.index_lista = 0
            Self.index_lista += 0.25
            Self.image = Self.sprite[int(Self.index_lista)]
            Self.mask = pygame.mask.from_surface(Self.image)
            
        if Self.andando == True:
            if Self.index_lista > 13 or Self.index_lista < 6:
                Self.index_lista = 6
            Self.index_lista += 0.15
            Self.image = Self.sprite[int(Self.index_lista)]
            Self.mask = pygame.mask.from_surface(Self.image)
            if pygame.key.get_pressed()[K_a]:
                if Self.rect.center[0] > 12:
                    Self.rect.x -= 3
            else:
                Self.parado = True
                Self.andando = False
                pass
            if pygame.key.get_pressed()[K_d]:
                if Self.rect.x < largura_tela:
                    Self.rect.x += 2.5
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

class Monstros(pygame.sprite.Sprite): 
    def __init__(Self):
        super().__init__()
        Self.sprite_medusa = []
        #[0] até [12]
        for i in range(13):
            img_walk = sprite_medusa_andando.subsurface((i * 128, 0),(128, 128)).convert_alpha()
            Self.sprite_medusa.append(img_walk)
        #[13] até [28]
        for i in range(16):
            img_attack = sprite_medusa_atacando.subsurface((i * 128, 0), (128, 128)).convert_alpha()
            Self.sprite_medusa.append(img_attack)
        
        Self.index_lista = 0
        Self.image = Self.sprite_medusa[Self.index_lista]
        Self.rect = Self.image.get_rect()
        Self.mask = pygame.mask.from_surface(Self.image)
        Self.rect.x = largura_tela + randrange(100, 800, 200)
        Self.rect.y = altura_tela - 256
        Self.atacando = False
        Self.andando = True
    
    def update(Self):
        if Self.andando:
            Self.index_lista += 0.25
            if Self.index_lista > 12:
                Self.index_lista = 0
            Self.image = Self.sprite_medusa[int(Self.index_lista)]
            if Self.rect.topright[0] < 0: 
                Self.rect.x = largura_tela + randrange(100, 800, 200)
            Self.rect.x -= 2
#funções para o jogo
def sair_menu():
    global menu, musica_game
    menu = False
    musica_game = pygame.mixer.music.load(os.path.join(diretorio_musicas, "jungle.mp3"))
    musica_game = pygame.mixer.music.play(-1)

# relogio fps
relogio = pygame.time.Clock()

# config. imagem de fundo do menu
fundo_menu = pygame.image.load(os.path.join(diretorio_sprites, "fundo-menu.jpg")).convert()
fundo_menu = pygame.transform.scale(fundo_menu, (largura_tela, altura_tela))
menu = True

#config. imagem de fundo durante game
fundo_game = pygame.image.load(os.path.join(diretorio_sprites, "fundo_game.png")).convert()
fundo_game = pygame.transform.scale(fundo_game, (largura_tela, altura_tela))

#texto menu
mensagem = "Pressione z para começar"
fonte_menu = pygame.font.SysFont('Pixeled', 50, True, False)
start_formatado = fonte_menu.render(mensagem, False, (160, 42, 45))

#musicas
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
for i in range(2):
    medusa = Monstros()
    todas_as_sprites.add(medusa)
    todos_inimigos.add(medusa)
#Loop principal
rodando = True
while rodando:
    while menu:
        tela.blit(fundo_menu, (0,0))
        tela.blit(icon, (meio_largura_tela - (icon.get_width() + 20) // 2, 10))
        tela.blit(start_formatado, (meio_largura_tela - start_formatado.get_width() // 2, 340))
        for event in pygame.event.get():
            if event.type == QUIT:
                rodando = False
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_z:
                    sair_menu()
        pygame.display.flip()
    

    relogio.tick(45)
    tela.blit(fundo_game, (0, 0))
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

    if pygame.key.get_pressed()[K_a]:
        jogador.andar()
    if pygame.key.get_pressed()[K_d]:
        jogador.andar()
    

    colisoes = pygame.sprite.spritecollide(jogador, todos_inimigos, False, pygame.sprite.collide_mask)
    todas_as_sprites.draw(tela)

    if colisoes:
        if jogador.atacando == True:
            medusa.rect.x = largura_tela + randrange(100, 800, 100)
            todas_as_sprites.update()
    else:
        todas_as_sprites.update()


    pygame.display.flip()
