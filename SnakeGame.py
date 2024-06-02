import pygame
import sys
import random

pygame.init()

#note trois difficultes (collision, speed et eliminations bord diff ? )

# Screen config
header_height = 50
width, height = 640, 480 + header_height  # Add header height to the total window height
screen = pygame.display.set_mode((width, height))

# Colors
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
grey = (120,120,120)

font = pygame.font.Font(None, 36)
score = 0  # Initialize score

class Snake:
    def __init__(self, initial_positions, speed=5):
        self.positions = initial_positions
        self.direction = 'RIGHT'
        self.speed = speed

    def move(self):
        x, y = self.positions[0]
        if self.direction == 'RIGHT':
            x += self.speed
        elif self.direction == 'LEFT':
            x -= self.speed
        elif self.direction == 'UP':
            y -= self.speed
        elif self.direction == 'DOWN':
            y += self.speed
        self.positions.insert(0, (x, y))
        self.positions.pop()

    def grow(self):
        self.positions.append(self.positions[-1])

    def draw(self):
        for position in self.positions:
            pygame.draw.rect(screen, green, pygame.Rect(position[0], position[1], 10, 10))

    def change_direction(self, new_direction):
        opposite_directions = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if new_direction != opposite_directions[self.direction]:
            self.direction = new_direction

class Food:
    def __init__(self, screen_width, screen_height, header_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.header_height = header_height
        self.position = self.randomize_position()

    def randomize_position(self):
        x = random.randrange(1, (self.screen_width // 10)) * 10
        y = random.randrange(1, ((self.screen_height - self.header_height) // 10)) * 10 + self.header_height
        return (x, y)

    def draw(self):
        pygame.draw.rect(screen, red, pygame.Rect(self.position[0], self.position[1], 10, 10))


def game_over_screen():
    screen.fill(black)
    game_over_text = font.render('Game Over', True, red)
    restart_text = font.render('Press Space to Restart', True, white)
    text_rect = game_over_text.get_rect(center=(width / 2, height / 2 - 20))
    restart_rect = restart_text.get_rect(center=(width / 2, height / 2 + 20))
    screen.blit(game_over_text, text_rect)
    screen.blit(restart_text, restart_rect)
    pygame.display.update()

def reset_game(snake, food):
    global score
    snake.positions = [(100, 150), (90, 150), (80, 150)]
    snake.direction = 'RIGHT'
    food.position = food.randomize_position()
    score = 0

def show_score():
    score_rect_x, score_rect_y, score_rect_width, score_rect_height = 0, 0, width, header_height
    pygame.draw.rect(screen, black, [score_rect_x, score_rect_y, score_rect_width, score_rect_height])
    score_text = font.render(f'Score: {score}', True, white)
    text_rect = score_text.get_rect(center=(score_rect_x + score_rect_width // 2, score_rect_y + score_rect_height // 2))
    screen.blit(score_text, text_rect)

def update_game_area():
    # Fill only the game area with grey
    pygame.draw.rect(screen, grey, [0, header_height, width, height - header_height])


snake = Snake([(100, 150), (90, 150), (80, 150)])
food = Food(width, height, header_height)
clock = pygame.time.Clock()


# Fonctions de collision
def collision_with_foodOLD(snake_head, food):
    return snake_head[0] == food[0] and snake_head[1] == food[1]

def collision_with_food(snake_head, food, tolerance=10):
    # Vérifie si le serpent est dans la zone définie par la tolerance autour du fruit
    return (food[0] - tolerance <= snake_head[0] <= food[0] + tolerance) and (food[1] - tolerance <= snake_head[1] <= food[1] + tolerance)


def collision_with_boundaries(snake_head):
    return (snake_head[0] >= width or snake_head[0] < 0 or
            snake_head[1] >= height or snake_head[1] < header_height)


def collision_with_self(snake_head, snake_body):
    return snake_head in snake_body[1:]

# Boucle principale du jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.change_direction('RIGHT')
            elif event.key == pygame.K_LEFT:
                snake.change_direction('LEFT')
            elif event.key == pygame.K_UP:
                snake.change_direction('UP')
            elif event.key == pygame.K_DOWN:
                snake.change_direction('DOWN')
            elif event.key == pygame.K_SPACE: # and is in game_over (boolean) ? 
                reset_game(snake, food)

    snake.move()

    if collision_with_food(snake.positions[0], food.position, tolerance=10):
        snake.grow()
        score += 1
        food.position = food.randomize_position()


    if collision_with_boundaries(snake.positions[0]) or collision_with_self(snake.positions[0], snake.positions):
        game_over_screen()
        wait_for_space = True
        while wait_for_space:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    wait_for_space = False
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    wait_for_space = False
                    reset_game(snake, food)
        
    update_game_area()
    show_score()
    
    snake.draw()
    food.draw()

    pygame.display.update()
    clock.tick(30)  
    


pygame.quit()
sys.exit()
