# TO-DO: implementar a dfs
from typing import Tuple, List, Dict, Optional


def dfs(
    start: Tuple[int, int],
    goal: Tuple[int, int],
    grid
) -> Tuple[Dict[Tuple[int, int], Optional[Tuple[int, int]]], List[Tuple[int, int]], List[Tuple[int, int]]]:

    stack: List[Tuple[int, int]] = [start]
    visited: List[Tuple[int, int]] = []
    frontier: List[Tuple[int, int]] = [start]
    came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}

    while stack:
        current = stack.pop()
        if current == goal:
            break

        if current not in visited:
            visited.append(current)
            x, y = current

            for nx, ny in grid.neighbors(x, y):
                neighbor = (nx, ny)
                if neighbor not in came_from:
                    came_from[neighbor] = current
                if neighbor not in visited and grid.is_passable(nx, ny):
                    stack.append(neighbor)
                    frontier.append(neighbor)

    return came_from, visited, frontier
