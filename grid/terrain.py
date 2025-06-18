import pygame
import numpy as np
import random
import math
from agente import Agent
from coin import Coin  # Supondo que salvou a classe Coin em coin.py



class TerrainGenerator:
    @staticmethod
    def generate(grid_size, scale=0.1):
        grad_grid = np.zeros((grid_size, grid_size, 2))
        for y in range(grid_size):
            for x in range(grid_size):
                angle = random.uniform(0, 2 * math.pi)
                grad_grid[y][x] = (math.cos(angle), math.sin(angle))

        noise_grid = np.zeros((grid_size, grid_size))
        for y in range(grid_size):
            for x in range(grid_size):
                noise_grid[y][x] = TerrainGenerator._perlin_value(
                    x * scale, y * scale, grad_grid, grid_size
                )
        # Normalize to 0-1
        noise_grid = (noise_grid - noise_grid.min()) / (noise_grid.max() - noise_grid.min())
        return noise_grid

    @staticmethod
    def _perlin_value(x, y, grad_grid, grid_size):
        x0 = int(x) % grid_size
        y0 = int(y) % grid_size
        x1 = (x0 + 1) % grid_size
        y1 = (y0 + 1) % grid_size

        dx = x - x0
        dy = y - y0

        n00 = grad_grid[y0][x0][0] * dx + grad_grid[y0][x0][1] * dy
        n01 = grad_grid[y1][x0][0] * dx + grad_grid[y1][x0][1] * (dy - 1)
        n10 = grad_grid[y0][x1][0] * (dx - 1) + grad_grid[y0][x1][1] * dy
        n11 = grad_grid[y1][x1][0] * (dx - 1) + grad_grid[y1][x1][1] * (dy - 1)

        u = TerrainGenerator._fade(dx)
        v = TerrainGenerator._fade(dy)

        nx0 = (1 - u) * n00 + u * n10
        nx1 = (1 - u) * n01 + u * n11
        return (1 - v) * nx0 + v * nx1

    @staticmethod
    def _fade(t):
        return t * t * t * (t * (t * 6 - 15) + 10)


# ================== Visualização Pygame =======================

# Definir biomas
def get_color(value):
    if value < 0.3:
        return ('blue')   # Água
    elif value < 0.4:
        return ('lavenderblush')  # Areia
    elif value < 0.7:
        return ('pink')    # Grama
    elif value < 0.85:
        return ('magenta')    # Montanha
    else:
        return (190, 190, 190)  # Pico nevado


def main():
    grid_size = 80
    tile_size = 10  # Tiles maiores
    width = grid_size * tile_size
    height = grid_size * tile_size

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Mapa de Terreno")

    #terrain = TerrainGenerator.generate(grid_size, scale=0.1)
    terrain = TerrainGenerator.generate(grid_size, scale=0.05)
    agent = Agent(terrain, tile_size)
    coin = Coin(terrain, tile_size)



    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(60)  # Limitar FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Desenhar terreno
        for y in range(grid_size):
            for x in range(grid_size):
                value = terrain[y][x]
                color = get_color(value)
                pygame.draw.rect(
                    screen,
                    color,
                    (x * tile_size, y * tile_size, tile_size, tile_size)
                )
        
        agent.draw(screen)
        coin.draw(screen)


        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
