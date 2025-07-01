import heapq

def astar(posAgente, posCoin, grid):
    def heuristic(a, b):

        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    visit_order = []
    came_from = {posAgente: None}
    cost_so_far = {posAgente: 0}
    frontier = [posAgente]
    heap = [(heuristic(posAgente, posCoin), 0, posAgente)]

    while heap:
        f_atual, g_atual, current = heapq.heappop(heap)

        if current == posCoin:
            return came_from, visit_order, frontier

        if current in frontier:
            frontier.remove(current)

        visit_order.append(current)
        x, y = current

        for nx, ny in grid.neighbors(x, y):
            neighbor = (nx, ny)
            new_cost = cost_so_far[current] + grid.cost(nx, ny)
            h = heuristic(neighbor, posCoin)
            f = new_cost + h

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current
                heapq.heappush(heap, (f, new_cost, neighbor))
                if neighbor not in frontier:
                    frontier.append(neighbor)

    return came_from, visit_order, frontier
