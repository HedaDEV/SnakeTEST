import pygame
import sys
import random

pygame.init()

#note trois difficultes (collision, speed et eliminations bord diff ? )

# Screen config
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

# Couleurs
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
grey = (120,120,120)

font = pygame.font.Font(None, 36)
#bg = pygame.image.load("bg.jpeg")

def game_over_screen():
    screen.fill(black)
    game_over_text = font.render('Game Over', True, red)
    restart_text = font.render('Press Space to Restart', True, white)
    text_rect = game_over_text.get_rect(center=(width / 2, height / 2 - 20))
    restart_rect = restart_text.get_rect(center=(width / 2, height / 2 + 20))
    screen.blit(game_over_text, text_rect)
    screen.blit(restart_text, restart_rect)
    pygame.display.update()

def reset_game():
    global snake_pos, food_pos, food_spawn, snake_direction, change_direction
    snake_pos = [[100, 50], [90, 50], [80, 50]]  
    snake_direction = 'RIGHT'  
    change_direction = snake_direction
    food_pos = [random.randrange(1, (width//10)) * 10, random.randrange(1, (height//10)) * 10]
    food_spawn = True

# Initialisation du serpent
snake_pos = [[100, 50], [90, 50], [80, 50]]  # Head et corps du serpent
snake_direction = 'RIGHT'
change_direction = snake_direction
snake_speed = 5  

# Nourriture
food_pos = [random.randrange(1, (width//10)) * 10, random.randrange(1, (height//10)) * 10]
food_spawn = True

clock = pygame.time.Clock()

# Fonctions de collision
def collision_with_foodOLD(snake_head, food):
    return snake_head[0] == food[0] and snake_head[1] == food[1]

def collision_with_food(snake_head, food, tolerance=10):
    # Vérifie si le serpent est dans la zone définie par la tolerance autour du fruit
    return (food[0] - tolerance <= snake_head[0] <= food[0] + tolerance) and (food[1] - tolerance <= snake_head[1] <= food[1] + tolerance)


def collision_with_boundaries(snake_head):
    return snake_head[0] >= width or snake_head[0] < 0 or snake_head[1] >= height or snake_head[1] < 0

def collision_with_self(snake_head, snake_body):
    return snake_head in snake_body[1:]

# Boucle principale du jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                change_direction = 'RIGHT'
            if event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                change_direction = 'LEFT'
            if event.key == pygame.K_UP and snake_direction != 'DOWN':
                change_direction = 'UP'
            if event.key == pygame.K_DOWN and snake_direction != 'UP':
                change_direction = 'DOWN'

     # MAJ direction du serpent avant de calculer le mouvement
    if change_direction in ['RIGHT', 'LEFT', 'UP', 'DOWN']:
        snake_direction = change_direction


    # Déplacer le serpent
    if change_direction == 'RIGHT':
        snake_head = [snake_pos[0][0] + snake_speed, snake_pos[0][1]]
    elif change_direction == 'LEFT':
        snake_head = [snake_pos[0][0] - snake_speed, snake_pos[0][1]]
    elif change_direction == 'UP':
        snake_head = [snake_pos[0][0], snake_pos[0][1] - snake_speed]
    elif change_direction == 'DOWN':
        snake_head = [snake_pos[0][0], snake_pos[0][1] + snake_speed]

    #snake_pos.insert(0, snake_head)

    if collision_with_food(snake_head, food_pos, tolerance=10):
        food_spawn = False
        snake_pos.insert(0, snake_head)
    else:
        snake_pos.insert(0, snake_head)
        snake_pos.pop()

    if not food_spawn:
        food_pos = [random.randrange(1, (width//10)) * 10, random.randrange(1, (height//10)) * 10]
    food_spawn = True


    if collision_with_boundaries(snake_head) or collision_with_self(snake_head, snake_pos):
        game_over_screen()
        wait_for_space = True
        while wait_for_space:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    wait_for_space = False
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    wait_for_space = False
                    reset_game()
        

    screen.fill(grey)
    
    for pos in snake_pos:
        pygame.draw.rect(screen, green, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(screen, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    pygame.display.update()
    clock.tick(30)  
    


pygame.quit()
sys.exit()
