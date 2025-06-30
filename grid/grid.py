class Grid:
    def __init__(self, width, height, terrain):
        """
        Grid discreto com limites e neighbors válidos.
        width, height: dimensões do grid em células.
        terrain: instância de Terrain.
        """
        self.width = width
        self.height = height
        self.terrain = terrain

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_passable(self, x, y):
        return self.terrain.is_passable(x, y)

    def cost(self, x, y):
        return self.terrain.cost(x, y)

    def neighbors(self, x, y):
        # movimentos em 4 direções
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x + dx, y + dy
            if self.in_bounds(nx, ny) and self.is_passable(nx, ny):
                yield (nx, ny)