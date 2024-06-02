import pygame
import sys
from config import WIDTH, HEIGHT, BLACK, FONT_SIZE
from game_objects import Snake, Food
from game_functions import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.Font(None, FONT_SIZE)
    clock = pygame.time.Clock()
    background = pygame.image.load('bg.png').convert()
    snake = Snake([(100, 150), (90, 150), (80, 150)])
    food = Food()
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    snake.change_direction('RIGHT')
                elif event.key == pygame.K_LEFT:
                    snake.change_direction('LEFT')
                elif event.key == pygame.K_UP:
                    snake.change_direction('UP')
                elif event.key == pygame.K_DOWN:
                    snake.change_direction('DOWN')
                elif event.key == pygame.K_SPACE:
                    snake = Snake([(100, 150), (90, 150), (80, 150)])  # Reset snake
                    food = Food()  # Reset food
                    score = 0  # Reset score

        snake.move()
        # Check for collisions
        if collision_with_food(snake.positions[0], food.position):
            snake.grow()
            score += 1
            food.position = food.randomize_position()

        if collision_with_boundaries(snake.positions[0]) or collision_with_self(snake.positions[0], snake.positions):
            game_over_screen(screen, font)
            snake = Snake([(100, 150), (90, 150), (80, 150)])
            food = Food()
            score = 0

        #update_game_area(screen)
        screen.blit(background, (0, HEADER_HEIGHT))
        show_score(screen, font, score)
        snake.draw(screen)
        food.draw(screen)
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
