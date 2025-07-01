# main.py
import pygame, sys, random
from grid.terrain import Terrain
from grid.grid import Grid
from grid.agente import Agent
from grid.coin import Coin

FPS = 10
TILE = 20
WIDTH, HEIGHT = 30, 20  # tamanho do grid em células

def draw_grid(screen, terrain):
    colors = {
        None: ( 50,  50,  50),  # obstáculo
         1:   (194, 178, 128),  # areia
         5:   ( 34, 139,  34),  # atoleiro
        10:   ( 30, 144, 255),  # água
    }
    for y in range(HEIGHT):
        for x in range(WIDTH):
            rect = pygame.Rect(x*TILE, y*TILE, TILE, TILE)
            pygame.draw.rect(screen, colors[terrain.grid[y][x]], rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH*TILE, HEIGHT*TILE))
    clock = pygame.time.Clock()

    # 1. Gera mapa e objetos
    terrain = Terrain(WIDTH, HEIGHT)
    grid    = Grid(WIDTH, HEIGHT, terrain)
    agent   = Agent(grid, TILE)
    coin    = Coin(grid, TILE)

    # lista de buscas disponíveis e índice atual
    methods = ['bfs','dfs','ucs','greedy','astar']
    method_idx = 3
    current_method = methods[method_idx]
    # cria fonte para desenhar texto
    font = pygame.font.SysFont(None, 24)

    # listas para animação
    visit_idx = 0
    traveled = []

    def restart_search(method='astar'):
        nonlocal visit_idx, traveled
        agent.spawn()
        coin.spawn()
        agent.perceive(coin)
        agent.find_path(method=method)
        visit_idx = 0
        traveled = []

    # primeira busca
    restart_search(method = "greedy")

    running = True
    while running:
        clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
        
            # troca o método de busca ao pressionar 1-5
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_1:
                    method_idx = 0  
                elif ev.key == pygame.K_2:
                    method_idx = 1
                elif ev.key == pygame.K_3:
                    method_idx = 2
                elif ev.key == pygame.K_4:
                    method_idx = 3
                elif ev.key == pygame.K_5:
                    method_idx = 4
                else:
                    method_idx = method_idx
                #atualizando e reiniciando
                current_method = methods[method_idx]
                restart_search(method=current_method)

        # desenha o terreno
        draw_grid(screen, terrain)
        # escreve qual busca está em uso
        txt = font.render(f'Busca: {current_method.upper()}', True, (255,255,255))
        screen.blit (txt, (10,10))

        # 1) pinta nós visitados até visit_idx
        for x, y in agent.visited[:visit_idx]:
            s = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
            s.fill((255,0,255,120))
            screen.blit(s, (x*TILE, y*TILE))

        # 2) pinta a fronteira completa
        for x, y in agent.frontier:
            pygame.draw.rect(screen, (255,255,0), (x*TILE, y*TILE, TILE, TILE), 2)

        # 3) se já visitou tudo, pinta o caminho final completo
        if visit_idx >= len(agent.visited):
            for x, y in agent.path:
                pygame.draw.rect(screen, (200,0,0), (x*TILE, y*TILE, TILE, TILE), 3)

        # 4) move o índice de visitação
        if visit_idx < len(agent.visited):
            visit_idx += 1

        # 5) desenha o caminho já percorrido pelo agente
        for x, y in traveled:
            pygame.draw.rect(screen, (150,0,150), (x*TILE, y*TILE, TILE, TILE))

        # 6) desenha agente e moeda
        agent.draw(screen)
        coin.draw(screen)
        pygame.display.flip()

        # 7) movimenta o agente passo a passo após a visitação
        if visit_idx >= len(agent.visited):
            if agent.path:
                next_cell = agent.move_step()
                traveled.append(next_cell)
                cost = terrain.cost(*next_cell)
                pygame.time.delay(50 * cost)
            else:
                # coleta e reinicia
                if agent.position == coin.position:
                    coin.collect()
                    restart_search(method=current_method)
                else:
                    # sem caminho, apenas reinicia
                    restart_search(method=current_method)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
