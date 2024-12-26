import pygame
import random
import sys

# Inizializzare pygame
pygame.init()

# Definire i colori
NERO = (0, 0, 0)
BIANCO = (255, 255, 255)
VERDE = (0, 255, 0)
BLU = (0, 0, 255)

# Impostazioni della finestra
LARGHEZZA = 400
ALTEZZA = 600
schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Flappy Bird")

# Classe del Pappagallo (o Uccello)
class Pappagallo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLU)
        self.rect = self.image.get_rect()
        self.rect.center = (50, ALTEZZA // 2)
        self.velocità_y = 0

    def update(self):
        tasti = pygame.key.get_pressed()
        if tasti[pygame.K_SPACE]:
            self.velocità_y = -10  # Salto verso l'alto

        # Gravità
        self.velocità_y += 0.5  # Accelerazione verso il basso
        self.rect.y += self.velocità_y

        # Limitare il movimento verticale
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= ALTEZZA:
            self.rect.bottom = ALTEZZA

# Classe per i Tubo (Obstacoli)
class Tubo(pygame.sprite.Sprite):
    def __init__(self, x, y, invertito=False):
        super().__init__()
        self.image = pygame.Surface((50, 500))
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if invertito:
            self.image = pygame.transform.flip(self.image, False, True)

    def update(self):
        self.rect.x -= 5  # Movimento orizzontale verso sinistra
        if self.rect.right < 0:
            self.kill()  # Rimuovere il tubo quando esce dallo schermo

# Funzione principale del gioco
def gioco():
    orologio = pygame.time.Clock()
    tutte_le_sprites = pygame.sprite.Group()
    tubi = pygame.sprite.Group()

    pappagallo = Pappagallo()
    tutte_le_sprites.add(pappagallo)

    # Variabili di gioco
    punteggio = 0
    generare_tubi_evento = pygame.USEREVENT
    pygame.time.set_timer(generare_tubi_evento, 1500)  # Ogni 1,5 secondi

    gioco_in_corso = True

    while gioco_in_corso:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                gioco_in_corso = False
            if evento.type == generare_tubi_evento:
                altezza_tubo = random.randint(100, 400)
                tubo_sopra = Tubo(LARGHEZZA, altezza_tubo - 500, invertito=True)
                tubo_sotto = Tubo(LARGHEZZA, altezza_tubo + 100)
                tubi.add(tubo_sopra, tubo_sotto)
                tutte_le_sprites.add(tubo_sopra, tubo_sotto)

        # Aggiornare le posizioni degli oggetti
        tutte_le_sprites.update()  

        # Verifica collisione
        if pygame.sprite.spritecollide(pappagallo, tubi, False) or pappagallo.rect.top <= 0 or pappagallo.rect.bottom >= ALTEZZA:
            gioco_in_corso = False  # Il gioco finisce se c'è una collisione

        # Rimuovere tubi fuori dallo schermo
        for tubo in tubi:
            if tubo.rect.right < 0:
                tubo.kill()
                punteggio += 1

        # Rendersi allo schermo
        schermo.fill(NERO)
        tutte_le_sprites.draw(schermo)

        # Mostrare il punteggio
        font = pygame.font.SysFont('Arial', 32)
        testo_punteggio = font.render(f"Punteggio: {punteggio}", True, BIANCO)
        schermo.blit(testo_punteggio, (10, 10))

        pygame.display.flip()

        # Regolare la velocità del gioco
        orologio.tick(60)

    # Fine del gioco
    pygame.quit()
    sys.exit()

# Avvia il gioco
gioco()
