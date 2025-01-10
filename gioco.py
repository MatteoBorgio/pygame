import pygame
import sys
import random

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_walk_1 = pygame.image.load("C:/Users/matte/Downloads/Untitled1066_20250103141955.png").convert_alpha()
        self.player_walk_1 = pygame.transform.scale(self.player_walk_1, (120, 160))
        self.player_walk_2 = pygame.image.load("C:/Users/matte/Downloads/Untitled1066_20250103142049.png").convert_alpha()
        self.player_walk_2 = pygame.transform.scale(self.player_walk_2, (120, 160))
        self.player_walk = [self.player_walk_1, self.player_walk_2]
        self.player_jump = pygame.image.load("C:/Users/matte/Downloads/Untitled1067_20250103145935.png").convert_alpha()
        self.player_jump = pygame.transform.scale(self.player_jump, (120, 160))
        
        self.index = 0
        self.image = self.player_walk[self.index]
        self.rect = self.image.get_rect(midbottom=(100, 310))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 310:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 0.8
        self.rect.y += self.gravity
        if self.rect.bottom >= 310:
            self.rect.bottom = 310

    def animations(self):
        if self.rect.bottom < 310:
            self.image = self.player_jump
        else:
            self.index += 0.1
            if self.index >= len(self.player_walk):
                self.index = 0
            self.image = self.player_walk[int(self.index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animations()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            self.frames = [
                pygame.image.load("C:/Users/matte/Downloads/Fly1.png").convert_alpha(),
                pygame.image.load("C:/Users/matte/Downloads/Fly2.png").convert_alpha()
            ]
            y_pos = 150
        else:
            self.frames = [
                pygame.image.load("C:/Users/matte/Downloads/snail1.png").convert_alpha(),
                pygame.image.load("C:/Users/matte/Downloads/snail2.png").convert_alpha()
            ]
            y_pos = 300

        self.animations_index = 0
        self.image = self.frames[self.animations_index]
        self.rect = self.image.get_rect(midbottom=(random.randint(900, 1100), y_pos))

    def animate(self):
        self.animations_index += 0.1
        if self.animations_index >= len(self.frames):
            self.animations_index = 0
        self.image = self.frames[int(self.animations_index)]

    def update(self):
        self.animate()
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()

class Hearts(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hearts = []
        self.hearts_surface = pygame.image.load("C:/Users/matte/Downloads/heart-48942_640.png").convert_alpha()
        self.hearts_surface = pygame.transform.scale(self.hearts_surface, (25, 25))
        self.image = self.hearts_surface
        self.rect = self.image.get_rect()

def display_score(screen, score):
    text_font = pygame.font.Font("C:/Users/matte/Downloads/Pixeltype.ttf", 50)
    score_surface = text_font.render(f'Punteggio: {score}', False, 'White')
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)          

message_displayed = False
message_time = 0

def display_message(screen):
    message_surface = pygame.image.load("C:/Users/matte/Downloads/broken_heart.webp")
    message_surface = pygame.transform.scale(message_surface, (300, 200))
    message_rect = message_surface.get_rect(center=(400, 200))
    screen.blit(message_surface, message_rect)

pygame.init()

screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()

game_active = False
start_time = 0
score = 0
count = 0

sky_surface = pygame.image.load("C:/Users/matte/Downloads/sky.jpg").convert()
sky_surface = pygame.transform.scale(sky_surface, (800, 300))

ground_surface = pygame.image.load("C:/Users/matte/Downloads/ground.png").convert()
ground_surface = pygame.transform.scale(ground_surface, (800, 300))

player = pygame.sprite.GroupSingle()
player.add(Player())

hearts = pygame.sprite.Group()

heart1 = Hearts()
heart1.rect.topleft = (650, 30)  # Posizione del primo cuore
heart2 = Hearts()
heart2.rect.topleft = (680, 30)  # Posizione del secondo cuore
heart3 = Hearts()
heart3.rect.topleft = (710, 30)  # Posizione del terzo cuore

hearts.add(heart1, heart2, heart3)

player_stand = pygame.image.load("C:/Users/matte/Downloads/Untitled1064_20241231221357.png").convert_alpha()
player_stand = pygame.transform.scale(player_stand, (180, 260))
player_stand_rectangle = player_stand.get_rect(center=(400, 200))

obstacles = pygame.sprite.Group()

name_font = pygame.font.Font("C:/Users/matte/Downloads/Pixeltype.ttf", 70)
game_name = name_font.render('Jumping with animals', False, "LightBlue")
game_name_rect = game_name.get_rect(center=(400, 50))

message_font = pygame.font.Font("C:/Users/matte/Downloads/Pixeltype.ttf", 60)
game_message = message_font.render('Press left shift to run', False, 'LightBlue')
game_message_rect = game_message.get_rect(center=(400, 350))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

message_timer_event = pygame.USEREVENT + 2
pygame.time.set_timer(message_timer_event, 3000)  

pygame.display.set_caption("Jumping with animals")

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT and not game_active:
                game_active = True
                start_time = pygame.time.get_ticks()
            if event.key == pygame.K_SPACE and game_active:
                player.sprite.player_input()
        
        if event.type == obstacle_timer and game_active:
            if random.randint(0, 1) == 0:
                obstacles.add(Obstacle('fly'))
            else:
                obstacles.add(Obstacle('snail'))

        if event.type == message_timer_event:
            message_displayed = False  

    if game_active:
        
        current_time = pygame.time.get_ticks() - start_time
        score = current_time // 1000

        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        
        display_score(screen, score)

        player.update()
        player.draw(screen)

        obstacles.update()
        obstacles.draw(screen)

        hearts.draw(screen)

        if pygame.sprite.spritecollide(player.sprite, obstacles, False):
            count += 1
            if count == 1:
                hearts.remove(heart1)
                message_displayed = True 
            elif count == 2:
                hearts.remove(heart2)
                message_displayed = True  
            elif count == 3:
                hearts.remove(heart3)
                game_active = False
                count = 0
                obstacles.empty()  # Rimuovi tutti gli ostacoli
                hearts.empty() #Rimuovi tutti i cuori
                player.sprite.rect.midbottom = (100, 310)  # Ripristina la posizione del giocatore
            obstacles.empty()  # Rimuovi tutti gli ostacoli
            player.sprite.rect.midbottom = (100, 310)  # Ripristina la posizione del giocatore

    else:
        hearts.add(heart1, heart2, heart3)
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rectangle)  # Mostra il giocatore nella posizione iniziale
        screen.blit(game_name, game_name_rect)
        score_message = message_font.render(f'Your score is: {score}', False, 'LightBlue')
        score_message_rect = score_message.get_rect(center=(400, 350))
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    if message_displayed:
        display_message(screen)

    pygame.display.update()
    clock.tick(60)

