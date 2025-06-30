
import random
import pygame

class Coin:
    """
    Representa a comida (moeda) no grid:
      - spawn(): escolhe posição aleatória em célula não‑obstáculo
      - draw(): desenha a moeda no Pygame
      - collected: contador de quantas moedas já foram coletadas
    """
    def __init__(self, grid, tile_size):
        self.grid = grid
        self.tile_size = tile_size
        self.position = None
        self.collected = 0

    def spawn(self):
        """
        Gera uma nova posição aleatória em célula passável.
        Atualiza self.position.
        """
        w, h = self.grid.width, self.grid.height
        while True:
            x = random.randrange(w)
            y = random.randrange(h)
            if self.grid.is_passable(x, y):
                self.position = (x, y)
                return self.position

    def collect(self):
        """
        Registra a coleta da moeda.
        Deve ser chamado quando agente colidir com self.position.
        """
        self.collected += 1
        self.position = None  # para forçar novo spawn

    def draw(self, screen):
        """
        Desenha a moeda no grid. 
        Usa um círculo dourado no centro da célula.
        """
        if self.position is None:
            return
        x, y = self.position
        cx = x * self.tile_size + self.tile_size // 2
        cy = y * self.tile_size + self.tile_size // 2
        radius = int(self.tile_size * 0.4)
        pygame.draw.circle(screen, (255, 215, 0), (cx, cy), radius)
