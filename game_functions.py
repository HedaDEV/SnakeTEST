import pygame
from config import WIDTH, HEIGHT, HEADER_HEIGHT, BLACK, RED, WHITE, GREY, FONT_SIZE

def game_over_screen(screen, font):
    screen.fill(BLACK)
    game_over_text = font.render('Game Over', True, RED)
    restart_text = font.render('Press Space to Restart', True, WHITE)
    text_rect = game_over_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 20))
    restart_rect = restart_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 20))
    screen.blit(game_over_text, text_rect)
    screen.blit(restart_text, restart_rect)
    pygame.display.update()

    # Wait for the player to press Space to continue
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  # Exit the entire program
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def show_score(screen, font, score):
    score_rect_x, score_rect_y, score_rect_width, score_rect_height = 0, 0, WIDTH, HEADER_HEIGHT
    pygame.draw.rect(screen, GREY, [score_rect_x, score_rect_y, score_rect_width, score_rect_height])
    score_text = font.render(f'Score: {score}', True, WHITE)
    text_rect = score_text.get_rect(center=(score_rect_x + score_rect_width // 2, score_rect_y + score_rect_height // 2))
    screen.blit(score_text, text_rect)

def update_game_area(screen):
    pygame.draw.rect(screen, GREY, [0, HEADER_HEIGHT, WIDTH, HEIGHT - HEADER_HEIGHT])


def collision_with_food(snake_head, food_position, tolerance=10):
    # Check if the snake's head is close enough to the food position
    return (food_position[0] - tolerance <= snake_head[0] <= food_position[0] + tolerance) and \
           (food_position[1] - tolerance <= snake_head[1] <= food_position[1] + tolerance)

def collision_with_boundaries(snake_head):
    # Check if the snake's head collides with the boundaries of the game area
    return (snake_head[0] >= WIDTH or snake_head[0] < 0 or
            snake_head[1] >= HEIGHT or snake_head[1] < HEADER_HEIGHT)

def collision_with_self(snake_head, snake_body):
    # Check if the snake's head collides with any part of its body
    return snake_head in snake_body[1:]

