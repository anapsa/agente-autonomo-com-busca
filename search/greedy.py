# algoritmo guloso

import heapq

def greedy(posAgente, posCoin, grid):
    def heuristic(a, b):
        # Distância de Manhattan
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    visit_order = []
    came_from = { posAgente: None }
    frontier = [posAgente]
    heap = [(heuristic(posAgente, posCoin), posAgente)]  # (h(n), posição)

    visited = set()

    while heap:
        _, current = heapq.heappop(heap)

        if current == posCoin:
            return came_from, visit_order, frontier

        if current in frontier:
            frontier.remove(current)

        visit_order.append(current)
        visited.add(current)
        x, y = current

        for nx, ny in grid.neighbors(x, y):
            neighbor = (nx, ny)
            if neighbor not in visited:
                came_from[neighbor] = current
                h = heuristic(neighbor, posCoin)
                heapq.heappush(heap, (h, neighbor))
                if neighbor not in frontier:
                    frontier.append(neighbor)

    return came_from, visit_order, frontier