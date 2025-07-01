# TO-DO: implementar a dfs
from typing import Tuple, List, Dict, Optional


def dfs(
    start: Tuple[int, int],
    goal: Tuple[int, int],
    grid
) -> Tuple[Dict[Tuple[int, int], Optional[Tuple[int, int]]], List[Tuple[int, int]], List[Tuple[int, int]]]:
    stack: List[Tuple[int, int]] = [start]
    visited: List[Tuple[int, int]] = []
    came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}

    while stack:
        current = stack.pop()
        if current == goal:
            frontier = stack.copy()
            break

        if current not in visited:
            visited.append(current)
            x, y = current

            for nx, ny in grid.neighbors(x, y):
                neighbor = (nx, ny)
                if neighbor not in came_from:
                    came_from[neighbor] = current
                if grid.is_passable(nx, ny) and neighbor not in visited and neighbor not in stack:
                    stack.append(neighbor)
    else:
        frontier = []

    return came_from, visited, frontier