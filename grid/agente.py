import random
import pygame
from grid.grid import Grid
from grid.coin import Coin
from search.bfs import bfs
from search.dfs import dfs
from search.ucs import ucs
# from search.astar import astar
from search.greedy import greedy


class Agent:
    """
    Agente que:
      - nasce em posição aleatória em célula passável
      - percebe a posição da comida (goal)
      - escolhe método de busca (bfs, dfs, ucs, greedy, astar)
      - executa a busca retornando path, visited e frontier
      - desloca-se passo a passo, ajustando sua “velocidade” ao custo do terreno
      - desenha-se no Pygame
    """
    def __init__(self, grid: Grid, tile_size: int, heuristic: str = 'manhattan'):
        self.grid = grid
        self.tile_size = tile_size
        self.heuristic = heuristic
        self.position = None     # (x, y)
        self.goal = None         # (x, y)
        self.path = []           # lista de (x,y) do caminho até goal
        self.visited = []        # nós já expandidos pela busca
        self.frontier = []       # fronteira durante a busca

    def spawn(self):
        """ Coloca o agente em uma célula aleatória não‑obstáculo. """
        w, h = self.grid.width, self.grid.height
        while True:
            x, y = random.randrange(w), random.randrange(h)
            if self.grid.is_passable(x, y):
                self.position = (x, y)
                return

    def perceive(self, coin: Coin):
        """ Enxerga a comida e define o objetivo. """
        self.goal = coin.position

    def find_path(self, method: str = 'ucs'):
        """
        Executa a busca escolhida e preenche:
          self.path, self.visited, self.frontier
        method ∈ {'bfs','dfs','ucs','greedy','astar'}
        """
        start = self.position
        goal = self.goal

        if method == 'bfs':
            came_from, self.visited, self.frontier = bfs(start, goal, self.grid)
        elif method == 'dfs':
            came_from, self.visited, self.frontier = dfs(start, goal, self.grid)
        elif method == 'ucs':
            came_from, self.visited, self.frontier = ucs(start, goal, self.grid)
        elif method == 'greedy':
            came_from, self.visited, self.frontier = greedy(start, goal, self.grid)
        # else:  # 'astar'
        #     came_from, self.visited, self.frontier = astar(start, goal, self.grid, self.heuristic)

        # Reconstrói o caminho final do goal de volta ao start
        self.path = []
        node = goal
        while node is not None and node in came_from:
            self.path.append(node)
            node = came_from[node]
        self.path.reverse()

    def move_step(self):
        """
        Move um passo ao longo de self.path.
        Retorna a célula nova ou None se o caminho já terminou.
        """
        if not self.path:
            return None
        next_cell = self.path.pop(0)
        self.position = next_cell
        return next_cell

    def draw(self, screen: pygame.Surface):
        """ Desenha o agente no screen do Pygame. """
        x, y = self.position
        cx = x * self.tile_size + self.tile_size // 2
        cy = y * self.tile_size + self.tile_size // 2
        radius = int(self.tile_size * 0.4)
        pygame.draw.circle(screen, (200, 0, 200), (cx, cy), radius)
