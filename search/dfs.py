# TO-DO: implementar a dfs
from typing import Tuple, List, Dict, Optional


def dfs(
    start: Tuple[int, int],
    goal: Tuple[int, int],
    grid
) -> Tuple[Dict[Tuple[int, int], Optional[Tuple[int, int]]], List[Tuple[int, int]], List[Tuple[int, int]]]:
    """
    Depth-First Search (DFS) implementation.

    Args:
        start: Starting cell coordinates (x, y).
        goal: Goal cell coordinates (x, y).
        grid: Grid object providing is_passable and neighbors(x, y).

    Returns:
        came_from: Mapping from each visited node to its predecessor.
        visited: List of nodes in the order they were expanded.
        frontier: List of nodes still in the stack when goal was found.
    """
    stack: List[Tuple[int, int]] = [start]
    visited: List[Tuple[int, int]] = []
    came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}

    while stack:
        current = stack.pop()
        if current == goal:
            # fronteira remanescente no stack
            frontier = stack.copy()
            break

        if current not in visited:
            visited.append(current)
            x, y = current

            for nx, ny in grid.neighbors(x, y):
                neighbor = (nx, ny)
                if neighbor not in came_from:
                    came_from[neighbor] = current
                # só empilha se passável e ainda não expandido ou descoberto
                if grid.is_passable(nx, ny) and neighbor not in visited and neighbor not in stack:
                    stack.append(neighbor)
    else:
        # se loop terminar sem break, sem frontier
        frontier = []

    return came_from, visited, frontier