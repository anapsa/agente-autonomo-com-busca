import heapq

def ucs(posAgente, posCoin, grid):

    N = grid.width
    visit_order = []
    came_from = { posAgente: None }
    cost_so_far = { posAgente: 0 }
    frontier = [posAgente]

    heap = [(0, posAgente)]  # (custo acumulado, posição)

    while heap:
        custo_atual, current = heapq.heappop(heap)

        if current == posCoin:
            return came_from, visit_order, frontier

        if current in frontier:
            frontier.remove(current)

        visit_order.append(current)
        x, y = current

        for nx, ny in grid.neighbors(x, y):
            neighbor = (nx, ny)
            new_cost = cost_so_far[current] + grid.cost(nx, ny)

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current
                heapq.heappush(heap, (new_cost, neighbor))
                if neighbor not in frontier:
                    frontier.append(neighbor)

    return came_from, visit_order, frontier
