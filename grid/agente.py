import random
import pygame
from typing import Tuple, Optional, Dict, List
from grid.grid import Grid
from grid.coin import Coin
from search.bfs import bfs
from search.dfs import dfs
from search.ucs import ucs
from search.greedy import greedy
from search.astar import astar

class Agent:
    """
    Agente que:
      - nasce em posição aleatória em célula passável
      - percebe a posição da comida (goal)
      - executa busca (BFS, DFS, UCS, Greedy, A*)
      - armazena lista de visitados, fronteira e caminho
      - desloca-se passo a passo, ajustando velocidade ao custo
      - não remove o caminho original, usa índice para animação
    """
    def __init__(
        self,
        grid: Grid,
        tile_size: int,
        heuristic: str = 'manhattan'
    ):
        self.grid = grid
        self.tile_size = tile_size
        self.heuristic = heuristic
        self.position: Tuple[int, int] = (0, 0)
        self.goal: Optional[Tuple[int, int]] = None
        self.visited: List[Tuple[int, int]] = []
        self.frontier: List[Tuple[int, int]] = []
        self.path: List[Tuple[int, int]] = []
        self.path_idx: int = 0  

    def spawn(self) -> None:
        """Posiciona o agente em célula passável aleatória."""
        w, h = self.grid.width, self.grid.height
        while True:
            x, y = random.randrange(w), random.randrange(h)
            if self.grid.is_passable(x, y):
                self.position = (x, y)
                return

    def perceive(self, coin: Coin) -> None:
        """Define o estado objetivo como a posição da moeda."""
        self.goal = coin.position

    def find_path(self, method: str = 'bfs') -> None:
        """
        Executa busca, popula:
          self.visited: ordem de expansão
          self.frontier: nós remanescentes ao encontrar goal
          self.path: lista de células do caminho
        Reinicia self.path_idx para animação.
        """
        start, goal = self.position, self.goal
        if method == 'bfs':
            came_from, self.visited, self.frontier = bfs(start, goal, self.grid)
        elif method == 'dfs':
            came_from, self.visited, self.frontier = dfs(start, goal, self.grid)
        elif method == 'ucs':
            came_from, self.visited, self.frontier = ucs(start, goal, self.grid)
        elif method == 'greedy':
            came_from, self.visited, self.frontier = greedy(start, goal, self.grid)
        elif method == 'astar':
            came_from, self.visited, self.frontier = astar(start, goal, self.grid)

        
        self.path = []
        node = goal
        while node is not None and node in came_from:
            self.path.append(node)
            node = came_from[node]
        self.path.reverse()

        self.path_idx = 0

    def move_step(self) -> Optional[Tuple[int, int]]:
        """
        Move um passo ao longo de self.path sem removê-la.
        Retorna a nova posição, ou None quando acabar, e limpa path ao final.
        """
       
        if self.path_idx >= len(self.path):
            return None
        next_cell = self.path[self.path_idx]
        self.position = next_cell
        self.path_idx += 1
        
        if self.path_idx >= len(self.path):
            self.path = []
        return next_cell

    def draw(self, screen: pygame.Surface) -> None:
        """Desenha o agente na tela como um círculo."""
        x, y = self.position
        cx = x * self.tile_size + self.tile_size // 2
        cy = y * self.tile_size + self.tile_size // 2
        r = int(self.tile_size * 0.4)
        pygame.draw.circle(screen, (200, 0, 200), (cx, cy), r)
