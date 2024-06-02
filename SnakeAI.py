import pygame
import sys
import random
import gymnasium as gym
from gymnasium import spaces
import numpy as np

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


class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['console']}

    def __init__(self):
        super(SnakeEnv, self).__init__()
        self.action_space = spaces.Discrete(4)  # 0: Up, 1: Down, 2: Left, 3: Right
        self.observation_space = spaces.Box(low=0, high=255, shape=(width, height, 1), dtype=np.uint8)
        
        self.snake = Snake([(100, 150), (90, 150), (80, 150)])
        self.food = Food(width, height, header_height)
        self.score = 0

    def manhattan_distance(self, point1, point2):
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    def step(self, action):

        # Capture the old distance to the food
        old_distance = self.manhattan_distance(self.snake.positions[0], self.food.position)

        self.snake.change_direction(['UP', 'DOWN', 'LEFT', 'RIGHT'][action])
        self.snake.move()

        # Calculate the new distance to the food
        new_distance = self.manhattan_distance(self.snake.positions[0], self.food.position)

        done = False
        reward = 0

        if collision_with_food(self.snake.positions[0], self.food.position):
            self.snake.grow()
            self.food.randomize_position()
            self.score += 1
            reward = 10
        if collision_with_boundaries(self.snake.positions[0]) or collision_with_self(self.snake.positions[0], self.snake.positions):
            reward = -100
            done = True

        # Adjust reward based on movement towards or away from the food
        if new_distance < old_distance:
            reward += 1  # Small reward for moving closer
        elif new_distance > old_distance:
            reward -= 1  # Small penalty for moving away

        obs = self.get_observation()
        return obs, reward, done, {}

    def reset(self):
        self.snake = Snake([(100, 150), (90, 150), (80, 150)])
        self.food.randomize_position()
        self.score = 0
        return self.get_observation()
    
    def render(self, mode='graphics', close=False):
        if close:
            pygame.quit()
            return

        if mode == 'graphics':
            screen.fill(grey)  # Set the background
            self.food.draw()   # Draw the food
            self.snake.draw()  # Draw the snake
            show_score()       # Display the score
            pygame.display.update()  # Update the display
        elif mode == 'console':
            print(f'Score: {self.score}')

    def get_observation(self):
        # This could be the positions of the snake and food or a rendered image
        return np.zeros((width, height, 1), dtype=np.uint8)

    def close(self):
        pass



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


#snake = Snake([(100, 150), (90, 150), (80, 150)])
#food = Food(width, height, header_height)
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


class QLearningAgent:
    def __init__(self, action_size):
        self.q_table = np.zeros((10000, action_size))  # Simplified state space for example
        self.epsilon = 0.5  # Exploration rate (def: 0.1)
        self.gamma = 0.99  # Discount factor (def: 0.99)
        self.alpha = 0.1  # Learning rate (def: 0.1)

    def get_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0, 3)  # Explore action space
        return np.argmax(self.q_table[state])  # Exploit learned values

    def update_q_table(self, state, action, reward, next_state):
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.gamma * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.alpha * td_error

# Main training loop
env = SnakeEnv()
agent = QLearningAgent(env.action_space.n)

for episode in range(1000):
    state = env.reset()
    done = False

    while not done:
        env.render()
        action = agent.get_action(state)
        next_state, reward, done, _ = env.step(action)
        agent.update_q_table(state, action, reward, next_state)
        state = next_state
        if reward > 1:
            print(f'reward: {reward}')

    if episode % 100 == 0:
        print(f'Episode: {episode}, Score: {env.score}')
    


pygame.quit()
sys.exit()
