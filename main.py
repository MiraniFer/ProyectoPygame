import pygame
import random

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN=(0, 255, 0)

# Configuración inicial de Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode([800, 600])
pygame.display.set_caption("Hongos Mágicos")
fuente = "Super Sunday Personal Use.ttf"
background = pygame.image.load("fondo.png").convert()
clock = pygame.time.Clock()

def show_menu():
    """Función para mostrar el menú principal."""
    font = pygame.font.Font(fuente, 74)
    small_font = pygame.font.Font(None, 36)
    menu = True
    pygame.mixer.music.load("musica_fondo.mp3")
    pygame.mixer.music.play()
    while menu:
        screen.fill(WHITE)
        title_text = font.render("Hongos Mágicos", True, BLACK)
        start_text = small_font.render("Presiona ENTER para comenzar", True, BLACK)
        quit_text = small_font.render("Presiona ESC para salir", True, BLACK)
        
        screen.blit(background, [0, 0])
        screen.blit(title_text, (150, 200))
        screen.blit(start_text, (200, 300))
        screen.blit(quit_text, (200, 350))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # ENTER para comenzar el juego
                    menu = False
                if event.key == pygame.K_ESCAPE:  # ESC para salir del juego
                    pygame.quit()
                    quit()

def show_game_over():
    """Función para mostrar el mensaje de Game Over."""
    font = pygame.font.Font(fuente, 74)
    small_font = pygame.font.Font(None, 36)
    screen.blit(background, [0, 0])
    game_over_text = font.render("Game Over", True, RED)
    restart_text = small_font.render("Presiona ENTER para salir", True, BLACK)
    screen.blit(game_over_text, (230, 200))
    screen.blit(restart_text, (240, 300))
    pygame.display.flip()
    
    # Esperar a que el jugador presione ENTER para salir
    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # ENTER para salir
                    game_over = False
                if event.key == pygame.K_ESCAPE:  # ESC para salir
                    pygame.quit()
                    quit()
def show_you_win():
    """Función para mostrar el mensaje de You Win."""
    font = pygame.font.Font(fuente, 74)
    small_font = pygame.font.Font(None, 36)
    screen.blit(background, [0, 0])
    win_text = font.render("You Win!", True, GREEN)
    restart_text = small_font.render("Presiona ENTER para salir", True, BLACK)
    screen.blit(win_text, (250, 200))
    screen.blit(restart_text, (250, 300))
    pygame.display.flip()
    
    # Esperar a que el jugador presione ENTER para salir
    you_win = True
    while you_win:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # ENTER para salir
                    you_win = False
                if event.key == pygame.K_ESCAPE:  # ESC para salir
                    pygame.quit()
                    quit()                    

def main_game():
    """Función que contiene la lógica del juego."""
    class Hongo(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("Mushroom_2.png")
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            
    class Piedra(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("stone.png")
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()        

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("ana.png")
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect()

    x_speed = 0
    y_speed = 0

    hongo_list = pygame.sprite.Group()
    piedra_list = pygame.sprite.Group()  
    all_sprite_list = pygame.sprite.Group()

    # Crear hongos
    for i in range(50):
        hongo = Hongo()
        hongo.rect.x = random.randrange(800)
        hongo.rect.y = random.randrange(600)
        hongo_list.add(hongo)
        all_sprite_list.add(hongo)

    # Crear piedras
    for i in range(5):
        piedra = Piedra()
        piedra.rect.x = random.randrange(750)
        piedra.rect.y = random.randrange(550)
        piedra_list.add(piedra)
        all_sprite_list.add(piedra)

    player = Player()
    all_sprite_list.add(player)

    total_hongos = len(hongo_list)
    collected_hongos = 0

    pygame.mixer.music.load("musica_fondo.mp3")
    pygame.mixer.music.play()

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_speed = -3
                if event.key == pygame.K_RIGHT:
                    x_speed = 3
                if event.key == pygame.K_UP:
                    y_speed = -3
                if event.key == pygame.K_DOWN:
                    y_speed = 3
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    x_speed = 0
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    y_speed = 0

        player.rect.x += x_speed
        player.rect.y += y_speed

        # Detectar colisiones con los hongos
        collected_hongos += len(pygame.sprite.spritecollide(player, hongo_list, True))

        # Detectar colisiones con las piedras (obstáculos)
        if pygame.sprite.spritecollide(player, piedra_list, False):
            # Terminar el juego si el jugador toca una piedra
            show_game_over()
            done = True
        
        if collected_hongos >= total_hongos:
            # Mostrar mensaje de "You Win" si el jugador recoge todos los hongos
            show_you_win()
            done = True

        screen.blit(background, [0, 0])
        all_sprite_list.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Mostrar el menú y luego iniciar el juego
show_menu()
main_game()
