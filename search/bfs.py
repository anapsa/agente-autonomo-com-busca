# TO-DO: implementar a bfs
from collections import deque

def Bfs(grid, posAgente, posCoin):
    N = len(grid)
    fila = deque([ (posAgente[0], posAgente[1]) ])
    direcoes = [(0,1), (0,-1), (1,0), (-1,0)]
    visitado = [[False]*N for _ in range(N)]
    visit_order = []
    pai = [[None]*N for _ in range(N)] # diz de que celula cada celula foi alcançada
    coin = (posCoin[0], posCoin[1])

    visitado[posAgente[1]][posAgente[0]] = True
    visit_order.append(((posAgente[0], posAgente[1])))

    while fila:
        x, y = fila.popleft() 
        if (x,y) == coin:
            path = reconstruirCaminho(pai, (posAgente[0], posAgente[1]), posCoin)
            return path, visit_order
        
        for dx, dy in direcoes: #para calcular os prox passos
            nx = x + dx
            ny = y + dy

            if (0<= nx < N) and (0 <= ny < N) and not visitado[ny][nx]:
                visitado[ny][nx] = True
                pai[ny][nx] = (x,y)
                visit_order.append((nx, ny))
                fila.append((nx,ny))

    return [], visit_order #quando não tem caminho

def reconstruirCaminho(pai, posAgente, posCoin):
    caminho = []
    atual = posCoin
    # anda “para trás” pelos ponteiros pai até chegar em start
    while atual != posAgente:
        caminho.insert(0, atual)
        atual = pai[atual[1]][atual[0]]
    caminho.insert(0, posAgente)
    return caminho
