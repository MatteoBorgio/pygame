import pygame
import sys
import random

def display_score(screen, score):
    text_font = pygame.font.Font("C:/Users/matte/Downloads/Pixeltype.ttf", 50)
    score_surface = text_font.render(f'Punteggio: {score}', False, 'White')
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)
    return score

def obstacle_movement(obstacle_rect_list, screen, snail_surface, fly_surface):
    for rect in obstacle_rect_list[:]:
        rect.x -= 5  # Movimento orizzontale verso sinistra
        if rect.right < 0:  # Se l'ostacolo esce dallo schermo, rimuovilo
            obstacle_rect_list.remove(rect)
        if rect.y > 200:
            screen.blit(snail_surface, rect)
        else:
            screen.blit(fly_surface, rect)
    return obstacle_rect_list

def player_animation():
    global player_surf, player_index, player_rectangle, player_walk
    if player_rectangle.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]
        
        
pygame.init()     # Inizializza pygame

screen = pygame.display.set_mode((800, 400))    # Dimensioni della finestra
clock = pygame.time.Clock()    # Controlla i frame al secondo

game_active = False
start_time = 0
score = 0

sky_surface = pygame.image.load("C:/Users/matte/Downloads/sky.jpg").convert()
sky_surface = pygame.transform.scale(sky_surface, (800, 300))  # Ridimensiona la sfondo per mantenere la proporzione

ground_surface = pygame.image.load("C:/Users/matte/Downloads/ground.png").convert()
ground_surface = pygame.transform.scale(ground_surface, (800, 300)) 

player_walk_1 = pygame.image.load("C:/Users/matte/Downloads/Untitled1066_20250103141955.png").convert_alpha()
player_walk_1 = pygame.transform.scale(player_walk_1, (120, 160))
player_walk_2 = pygame.image.load("C:/Users/matte/Downloads/Untitled1066_20250103142049.png").convert_alpha()
player_walk_2 = pygame.transform.scale(player_walk_2, (120, 160))
player_walk = [player_walk_1, player_walk_2]
player_jump = pygame.image.load("C:/Users/matte/Downloads/Untitled1064_20241231221357.png").convert_alpha()
player_jump= pygame.transform.scale(player_jump, (120, 160))
player_index = 0
player_gravity = 0  

player_surf = player_walk[player_index]
player_rectangle = player_surf.get_rect(midbottom=(100, 310))

player_stand = pygame.image.load("C:/Users/matte/Downloads/Untitled1064_20241231221357.png").convert_alpha()
player_stand = pygame.transform.scale(player_stand, (180, 260))
player_stand_rectangle = player_stand.get_rect(center=(400, 200))

# Definiamo la superficie della lumaca
snail_walk_1 = pygame.image.load("C:/Users/matte/Downloads/snail1.png").convert_alpha()
snail_walk_2 = pygame.image.load("C:/Users/matte/Downloads/snail2.png").convert_alpha()
snail_walk = [snail_walk_1, snail_walk_2]
snail_index = 0
snail_surface = snail_walk[snail_index]

obstacle_rect_list = []

fly_frames_1 = pygame.image.load("C:/Users/matte/Downloads/Fly1.png").convert_alpha()
fly_frames_2 = pygame.image.load("C:/Users/matte/Downloads/Fly2.png").convert_alpha()
fly_frames = [fly_frames_1, fly_frames_2]
fly_index = 0
fly_surface = fly_frames[fly_index]

name_font = pygame.font.Font("C:/Users/matte/Downloads/Pixeltype.ttf", 70)
game_name = name_font.render('Jumping with animals', False, "LightBlue")
game_name_rect = game_name.get_rect(center=(400, 50))

message_font = pygame.font.Font("C:/Users/matte/Downloads/Pixeltype.ttf", 60)
game_message = message_font.render('Press left shift to run', False, 'LightBlue')
game_message_rect = game_message.get_rect(center=(400, 350))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)
fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

pygame.display.set_caption("Jumping with animals")

while True:  # Fa continuare il gioco finché non viene inserito un break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # Chiude pygame
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rectangle.collidepoint(event.pos) and player_rectangle.bottom == 310:
                player_gravity = -25  # Movimento del giocatore verso l'alto      
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_rectangle.bottom == 310:
                player_gravity = -25  # Movimento del giocatore verso l'alto 
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT and not game_active:
            game_active = True
            start_time = pygame.time.get_ticks()

        # Aggiungi un nuovo ostacolo quando il timer scade
        if game_active:
            if event.type == obstacle_timer:  
                # Crea un nuovo rettangolo per l'ostacolo (lumaca)
                if random.randint(0, 2) == 0:
                    new_obstacle = fly_surface.get_rect(midbottom=(random.randint(900, 1100), 150))
                else:
                    new_obstacle = snail_surface.get_rect(midbottom=(random.randint(900, 1100), 300))
                obstacle_rect_list.append(new_obstacle)

                # Aggiorna il timer dell'animazione della lumaca e della mosca fuori dal blocco che aggiunge ostacoli
        if game_active:
            if event.type == snail_animation_timer:
                if snail_index == 0:
                    snail_index = 1
                else:
                    snail_index = 0
                snail_surface = snail_walk[snail_index]

            if event.type == fly_animation_timer:
                if fly_index == 0:
                    fly_index = 1
                else:
                    fly_index = 0
                fly_surface = fly_frames[fly_index]

    if game_active:
        current_time = pygame.time.get_ticks() - start_time
                                                     
        player_gravity += 0.8
        player_rectangle.y += player_gravity

        if player_rectangle.bottom > 310:  # Gestisce la collisione con il terreno
            player_rectangle.bottom = 310
            player_gravity = 0

        screen.blit(sky_surface, (0, 0))  # Posizione del cielo sullo schermo
        screen.blit(ground_surface, (0, 300))  # Posizione del terreno sullo schermo

        score = display_score(screen, current_time // 1000)  # Visualizza il punteggio in secondi
        
        player_animation()

        screen.blit(player_surf, player_rectangle)  # Posizione del giocatore sullo schermo

        # Muovi e rimuovi gli ostacoli
        obstacle_rect_list = obstacle_movement(obstacle_rect_list, screen, snail_surface, fly_surface)

        # Gestione collisione tra giocatore e ostacolo
        for obstacle in obstacle_rect_list:
            if player_rectangle.colliderect(obstacle):
                game_active = False

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rectangle)
        screen.blit(game_name, game_name_rect)
        score_message = message_font.render(f'Your score is: {score}', False, 'LightBlue')
        score_message_rect = score_message.get_rect(center=(400, 350))
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

        # Quando il gioco non è attivo, rimuoviamo tutte le lumache
        obstacle_rect_list.clear()
        player_rectangle.midbottom = (80, 300)

    pygame.display.update() 
    clock.tick(60)


