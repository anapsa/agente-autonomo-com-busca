import pygame
import numpy as np
import random
import math

class Coin:
    def __init__(self, terrain, tile_size):
        self.terrain = terrain
        self.grid_size = terrain.shape[0]
        self.tile_size = tile_size
        self.position = self.spawn()

    def spawn(self):
        while True:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            # Garante que a moeda não esteja na água
            if self.terrain[y][x] >= 0.3:
                return (x, y)

    def draw(self, screen):
        center_x = self.position[0] * self.tile_size + self.tile_size // 2
        center_y = self.position[1] * self.tile_size + self.tile_size // 2
        radius = int(self.tile_size * 1.2)

        pygame.draw.circle(
            screen,
            (255, 215, 0),  # Cor dourada (amarelo ouro)
            (center_x, center_y),
            radius
        )
