from typing import Optional, Dict
import random

class Terrain:
    """
    Gera um ambiente totalmente observável e discreto (grid) com 4 tipos de terreno:
      - Obstáculo (None): não atravessável
      - Terreno de custo baixo (1): areia
      - Terreno de custo médio (5): atoleiro
      - Terreno de custo alto (10): água
    """

    # custos por tipo de terreno
    TERRAIN_COSTS: Dict[str, Optional[int]] = {
        'OBSTACLE': None,
        'SAND':     1,
        'SWAMP':    5,
        'WATER':    10,
    }

    def __init__(
        self,
        width: int,
        height: int,
        probs: Optional[Dict[str, float]] = None
    ):
        """
        width, height: dimensões do grid em colunas e linhas.
        probs: probabilidades de cada tipo de terreno,
               ex: {'OBSTACLE':0.1, 'SAND':0.4, 'SWAMP':0.3, 'WATER':0.2}
        """
        self.width = width
        self.height = height

        # probabilidades padrão (podem ser ajustadas)
        self.probs: Dict[str, float] = probs or {
            'OBSTACLE': 0.1,
            'SAND':     0.4,
            'SWAMP':    0.3,
            'WATER':    0.2,
        }

        # gera o grid
        self.grid: list[list[Optional[int]]] = [
            [self._random_cell() for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def _random_cell(self) -> Optional[int]:
        """Escolhe um tipo de terreno pela distribuição de probs."""
        r = random.random()
        acc = 0.0
        for terrain_type, p in self.probs.items():
            acc += p
            if r <= acc:
                return Terrain.TERRAIN_COSTS[terrain_type]
        # fallback caso arredondamento não some 1.0
        return Terrain.TERRAIN_COSTS['SAND']

    def is_passable(self, x: int, y: int) -> bool:
        """Retorna True se a célula (x,y) não for obstáculo."""
        return self.grid[y][x] is not None

    def cost(self, x: int, y: int) -> int:
        """
        Retorna o custo de atravessar a célula (x,y).
        Lança ValueError se for obstáculo.
        """
        c = self.grid[y][x]
        if c is None:
            raise ValueError(f"Célula ({x},{y}) é obstáculo — agente não pode passar.")
        return c

    def reset(self) -> None:
        """Regenera todo o mapa aleatoriamente, reiniciando self.grid."""
        self.grid = [
            [self._random_cell() for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def __getitem__(self, row: int) -> list[Optional[int]]:
        """Permite acesso direto terrain[y][x] para renderização."""
        return self.grid[row]
