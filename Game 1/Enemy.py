import pygame
import random

# Set up some constants
WIDTH, HEIGHT = 1600, 900
BLUE = (0, 0, 255)
ENEMY_SIZE = 50  # Same size as the player
ENEMY_SPEED = 0.4

class Enemy:
    def __init__(self, player_pos):
        # Ensure the enemy spawns at least 200 pixels away from the player
        while True:
            self.pos = [random.randint(0, WIDTH), random.randint(0, HEIGHT)]
            dx, dy = self.pos[0] - player_pos[0], self.pos[1] - player_pos[1]
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist >= 200:
                break
        self.speed = ENEMY_SPEED
        self.start_time = pygame.time.get_ticks()  # Get the current time

    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, self.pos, ENEMY_SIZE)

    def update(self, player_pos):
        if pygame.time.get_ticks() - self.start_time < 3000:  # If less than 3 seconds have passed
            return  # Don't update the enemy's position
        dx, dy = player_pos[0] - self.pos[0], player_pos[1] - self.pos[1]
        dist = (dx ** 2 + dy ** 2) ** 0.5
        self.pos[0] += self.speed * dx / dist
        self.pos[1] += self.speed * dy / dist

    def collides_with(self, player_pos, player_size):
        distance = ((self.pos[0] - player_pos[0]) ** 2 + (self.pos[1] - player_pos[1]) ** 2) ** 0.5
        return distance < ENEMY_SIZE + player_size