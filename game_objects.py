import pygame
import random
from config import WIDTH, HEIGHT, HEADER_HEIGHT, GREEN, RED

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

    def draw(self, screen):
        for position in self.positions:
            pygame.draw.rect(screen, GREEN, pygame.Rect(position[0], position[1], 10, 10))

    def change_direction(self, new_direction):
        opposite_directions = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if new_direction != opposite_directions[self.direction]:
            self.direction = new_direction

class Food:
    def __init__(self):
        self.position = self.randomize_position()

    def randomize_position(self):
        x = random.randrange(1, (WIDTH // 10)) * 10
        y = random.randrange(1, ((HEIGHT - HEADER_HEIGHT) // 10)) * 10 + HEADER_HEIGHT
        return (x, y)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, pygame.Rect(self.position[0], self.position[1], 10, 10))
