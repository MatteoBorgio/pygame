import pygame
import sys

def display_score(screen, score):
    text_font = pygame.font.SysFont('Times New Roman',32)
    score_surface = text_font.render(f'Punteggio: {score}', False, 'Black')
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)

pygame.init()     # Inizializza pygame

screen = pygame.display.set_mode((800, 400))    # Dimensioni della finestra

clock = pygame.time.Clock()    # Controlla i frame al secondo

game_active = True 

start_time = 0

sky_surface = pygame.image.load("C:/Users/matte/Downloads/sky.jpg").convert()
sky_surface = pygame.transform.scale(sky_surface, (800, 300))  # Ridimensiona la sfondo per mantenere la proporzione

ground_surface = pygame.image.load("C:/Users/matte/Downloads/ground.png").convert()
ground_surface = pygame.transform.scale(ground_surface, (800, 300)) 

player_surface = pygame.image.load("C:/Users/matte/Downloads/personaggio.png").convert_alpha()
player_surface = pygame.transform.scale(player_surface, (100, 140))
player_rectangle = player_surface.get_rect(midbottom = (100, 325))
player_gravity = 0  
player_stand = pygame.image.load("C:/Users/matte/Downloads/personaggio.png").convert_alpha()
player_stand = pygame.transform.scale(player_stand, (200, 280))
player_stand_rectangle = player_stand.get_rect(center = (400, 200)) 

snail_surface = pygame.image.load("C:/Users/matte/Downloads/snail.png").convert_alpha()
snail_surface = pygame.transform.scale(snail_surface, (40, 80))
snail_rectangle = snail_surface.get_rect(midbottom = (700, 317))
snail_speed = 4

pygame.display.set_caption("Il mio gioco")

while True: # Fa continuare il gioco finchè non viene inserito un break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()     # Chiude pygame
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rectangle.collidepoint(event.pos) and player_rectangle.bottom == 325:
                player_gravity = -20  # Movimento del giocatore verso l'alto      
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_rectangle.bottom == 325:
                player_gravity = -20  # Movimento del giocatore verso l'alto 
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT and game_active == False:
            game_active = True
            snail_rectangle.left = 700
            start_time = pygame.time.get_ticks()


    if game_active:

        current_time = pygame.time.get_ticks() - start_time
                                                     
        player_gravity += 0.8
        player_rectangle.y += player_gravity

        if player_rectangle.bottom > 325:  # Gestisce la collisione con il terreno
            player_rectangle.bottom = 325
            player_gravity = 0

        screen.blit(sky_surface, (0, 0))  # Posizione del cielo sullo schermo
        screen.blit(ground_surface, (0, 300))  # Posizione del terreno sullo schermo

        snail_rectangle.x -= snail_speed   # Movimento della lumaca

        if snail_rectangle.left < -50: # Gestisce l'uscita dallo schermo
            snail_rectangle.x = 900
        
        if snail_rectangle.colliderect(player_rectangle):
            game_active = False

        display_score(screen, current_time // 1000)  # Visualizza il punteggio in secondi
                        
        screen.blit(player_surface, player_rectangle) # Posizione del giocatore sullo schermo
        screen.blit(snail_surface, snail_rectangle) # Posizione della lumaca sullo schermo

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rectangle)

    pygame.display.update() 
    clock.tick(60)

