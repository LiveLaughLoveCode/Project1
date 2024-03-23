import pygame
import random

# Set up some constants
WIDTH, HEIGHT = 1600, 900
YELLOW = (255, 255, 0)
ITEM_SIZE = 20

class Item:
    def __init__(self):
        self.pos = [random.randint(0, WIDTH), random.randint(0, HEIGHT)]

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, self.pos, ITEM_SIZE)

    def collides_with(self, player_pos, player_size):
        distance = ((self.pos[0] - player_pos[0]) ** 2 + (self.pos[1] - player_pos[1]) ** 2) ** 0.5
        return distance < ITEM_SIZE + player_size

    @staticmethod
    def regenerate_items(items):
        if not items:
            items[:] = [Item() for _ in range(10)]