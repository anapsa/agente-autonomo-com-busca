import pygame
import numpy as np
import random
import math

class Agent:
    def __init__(self, terrain, tile_size):
        self.terrain = terrain
        self.grid_size = terrain.shape[0]
        self.tile_size = tile_size
        self.position = self.spawn()

    def spawn(self):
        while True:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            # Impede que o agente nasça na água (exemplo)
            if self.terrain[y][x] >= 0.3:
                return (x, y)

    def draw(self, screen):
        scale = 2  # 20% maior que o tile
        size = int(self.tile_size * scale)
        offset = (size - self.tile_size) // 2

        pygame.draw.rect(
            screen,
            'dark green',
            (
                self.position[0] * self.tile_size - offset,
                self.position[1] * self.tile_size - offset,
                size,
                size
            )
        )


    def move_to(self, new_position):
        self.position = new_position
        if new_position not in self.path_traveled:
            self.path_traveled.append(new_position)
