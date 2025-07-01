# main.py
import pygame, sys, random
from grid.terrain import Terrain
from grid.grid import Grid
from grid.agente import Agent
from grid.coin import Coin

FPS = 10
TILE = 20
WIDTH, HEIGHT = 30, 20  # tamanho do grid em células
SIDEBAR_W = 160         # largura da sidebar em pixels

SEARCH_METHODS = ['bfs','dfs','ucs','greedy','astar']

# Cores da interface
COLOR_BG = (30, 30, 30)
COLOR_ITEM = (70, 70, 70)
COLOR_HOVER = (100, 100, 100)
COLOR_ACTIVE = (200, 200, 200)


def draw_sidebar(screen, font, current_method):
    sidebar_rect = pygame.Rect(0, 0, SIDEBAR_W, HEIGHT * TILE)
    pygame.draw.rect(screen, COLOR_BG, sidebar_rect)
    for idx, method in enumerate(SEARCH_METHODS):
        y = 20 + idx * 40
        item_rect = pygame.Rect(10, y, SIDEBAR_W - 20, 30)
        mx, my = pygame.mouse.get_pos()
        color = COLOR_HOVER if item_rect.collidepoint(mx, my) else COLOR_ITEM
        if method == current_method:
            pygame.draw.rect(screen, COLOR_ACTIVE, item_rect.inflate(4,4))
        pygame.draw.rect(screen, color, item_rect)
        txt = font.render(method.upper(), True, (255,255,255))
        screen.blit(txt, (item_rect.x + 10, item_rect.y + 5))


def draw_grid(screen, terrain):
    colors = {
        None: (50, 50, 50),   # obstáculo
        1:    (194, 178, 128),# areia
        5:    (34, 139, 34),  # atoleiro
        10:   (30, 144, 255), # água
    }
    for y in range(HEIGHT):
        for x in range(WIDTH):
            rect = pygame.Rect(SIDEBAR_W + x*TILE, y*TILE, TILE, TILE)
            pygame.draw.rect(screen, colors[terrain.grid[y][x]], rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH*TILE + SIDEBAR_W, HEIGHT*TILE))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    terrain = Terrain(WIDTH, HEIGHT)
    grid    = Grid(WIDTH, HEIGHT, terrain)
    agent   = Agent(grid, TILE)
    coin    = Coin(grid, TILE)

    current_method = SEARCH_METHODS[0]
    def restart_search(method):
        nonlocal current_method, visit_idx, traveled
        current_method = method
        agent.spawn(); coin.spawn()
        agent.perceive(coin)
        agent.find_path(method=method)
        visit_idx = 0
        traveled = []

    visit_idx = 0
    traveled = []
    restart_search(current_method)

    running = True
    while running:
        clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = ev.pos
                if mx < SIDEBAR_W:
                    idx = (my - 20) // 40
                    if 0 <= idx < len(SEARCH_METHODS):
                        restart_search(SEARCH_METHODS[idx])

        screen.fill((0,0,0))
        draw_sidebar(screen, font, current_method)
        draw_grid(screen, terrain)
        info = font.render(f'Busca: {current_method.upper()}', True, (255,255,255))
        screen.blit(info, (SIDEBAR_W+10, 10))

        # animação de nós visitados
        for x, y in agent.visited[:visit_idx]:
            s = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
            s.fill((255,0,255,120))
            screen.blit(s, (SIDEBAR_W + x*TILE, y*TILE))

        # animação da fronteira
        for x, y in agent.frontier:
            pygame.draw.rect(screen, (255,255,0), (SIDEBAR_W+x*TILE, y*TILE, TILE, TILE), 2)

        # exibe caminho final
        if visit_idx >= len(agent.visited):
            for x, y in agent.path:
                pygame.draw.rect(screen, (200,0,0), (SIDEBAR_W+x*TILE, y*TILE, TILE, TILE), 3)

        # avança animação
        if visit_idx < len(agent.visited):
            visit_idx += 1

        # trilha percorrida
        for x, y in traveled:
            pygame.draw.rect(screen, (150,0,150), (SIDEBAR_W+x*TILE, y*TILE, TILE, TILE))

        # desenha agente com offset
        ax, ay = agent.position
        acx = SIDEBAR_W + ax*TILE + TILE//2
        acy = ay*TILE + TILE//2
        pygame.draw.circle(screen, (200,0,200), (acx, acy), int(TILE*0.4))

        # desenha moeda com offset
        if coin.position is not None:
            mx, my = coin.position
            ccx = SIDEBAR_W + mx*TILE + TILE//2
            ccy = my*TILE + TILE//2
            pygame.draw.circle(screen, (255,215,0), (ccx, ccy), int(TILE*0.4))

        pygame.display.flip()

        # animação de movimento
        if visit_idx >= len(agent.visited):
            if agent.path:
                nxt = agent.move_step()
                traveled.append(nxt)
                pygame.time.delay(50 * terrain.cost(*nxt))
            else:
                if agent.position == coin.position:
                    coin.collect()
                restart_search(current_method)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
