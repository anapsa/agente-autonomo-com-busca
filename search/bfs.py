# search/bfs.py

from collections import deque

def bfs(posAgente, posCoin, grid):
    N = grid.width
    fila = deque([posAgente])
    visitado = [[False]*N for _ in range(N)]
    visit_order = []        # ordem dos expandidos
    came_from = { posAgente: None }
    frontier = [ posAgente ]
    
    # marca o nó inicial
    visitado[posAgente[1]][posAgente[0]] = True
    visit_order.append(posAgente)

    while fila:
        current = fila.popleft()
        # remove da fronteira
        if current in frontier:
            frontier.remove(current)

        # se achou a moeda, retorna tudo
        if current == posCoin:
            return came_from, visit_order, frontier

        x, y = current
        for nx, ny in grid.neighbors(x,y):
            if not visitado[ny][nx]:
                visitado[ny][nx]   = True
                came_from[(nx, ny)] = current
                visit_order.append((nx, ny))
                fila.append((nx, ny))
                frontier.append((nx, ny))

    # sem caminho até a moeda
    return came_from, visit_order, frontier
