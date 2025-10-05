import pygame
import time
from grid import Grid, Node
from algorithms import a_star_search, dijkstra_search, weighted_a_star_search

# --- Constants ---
# NEW: Smaller window size to fit on more screens
WIDTH, HEIGHT = 600, 680 # Made slightly taller to accommodate text at the bottom

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (64, 200, 224)
TURQUOISE = (175, 238, 238)
ORANGE = (255, 215, 180)

# --- Pygame Setup ---
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Visualizer")
pygame.font.init()
FONT = pygame.font.SysFont('arial', 18)

# --- Helper and Drawing Functions ---
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    # Prevent clicks outside the grid area from crashing
    if y >= width: return -1, -1 
    row = y // gap
    col = x // gap
    return row, col

def draw_nodes(win, grid_obj, rows, width, start_node=None, end_node=None, open_set=None, closed_set=None, path=None):
    gap = width // rows
    open_set, closed_set, path = open_set or set(), closed_set or set(), path or []
    for row in grid_obj.grid:
        for node in row:
            color = WHITE
            if node in open_set: color = TURQUOISE
            elif node in closed_set: color = ORANGE
            if node.is_obstacle: color = BLACK
            pygame.draw.rect(win, color, (node.col * gap, node.row * gap, gap, gap))
    for node in path:
        pygame.draw.rect(win, BLUE, (node.col * gap, node.row * gap, gap, gap))
    if start_node: pygame.draw.rect(win, GREEN, (start_node.col * gap, start_node.row * gap, gap, gap))
    if end_node: pygame.draw.rect(win, RED, (end_node.col * gap, end_node.row * gap, gap, gap))

def draw_grid_lines(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid_obj, rows, width, start_node=None, end_node=None, open_set=None, closed_set=None, path=None, algo_name="", metrics=None):
    win.fill(WHITE)
    
    # --- NEW: Draw information text INSIDE the window ---
    grid_area_height = width # Grid is square
    
    # Draw algorithm and controls info
    info_text_1 = FONT.render(f"Algorithm: {algo_name}", True, BLACK)
    win.blit(info_text_1, (10, grid_area_height + 5))
    info_text_2 = FONT.render("(A)Star | (D)ijkstra | (W)eighted A* | SPACE to run, C to clear", True, BLACK)
    win.blit(info_text_2, (10, grid_area_height + 25))

    # Draw performance metrics if they exist
    if metrics:
        metrics_text = FONT.render(f"Time: {metrics['time']:.4f}s | Path Length: {metrics['length']} | Nodes Explored: {metrics['explored']}", True, BLACK)
        win.blit(metrics_text, (10, grid_area_height + 50))
    
    # Draw the grid and nodes
    draw_nodes(win, grid_obj, rows, width, start_node, end_node, open_set, closed_set, path)
    draw_grid_lines(win, rows, width)
    pygame.display.update()

# --- Main Application Loop ---
def main(win, width):
    GRID_WIDTH = width
    ROWS = 40
    grid = Grid(ROWS, ROWS)
    start_node, end_node = None, None
    run = True
    
    algorithm_func = a_star_search
    algorithm_name = "A* Search"
    last_metrics = None

    while run:
        draw(win, grid, ROWS, GRID_WIDTH, start_node, end_node, algo_name=algorithm_name, metrics=last_metrics)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, GRID_WIDTH)
                if row != -1: # Ensure click is within grid
                    node = grid.get_node(row, col)
                    if node:
                        if not start_node and node != end_node: start_node = node
                        elif not end_node and node != start_node: end_node = node
                        elif node != end_node and node != start_node: node.set_obstacle(True)
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, GRID_WIDTH)
                if row != -1:
                    node = grid.get_node(row, col)
                    if node:
                        node.set_obstacle(False)
                        if node == start_node: start_node = None
                        if node == end_node: end_node = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    algorithm_func, algorithm_name = a_star_search, "A* Search"
                if event.key == pygame.K_d:
                    algorithm_func, algorithm_name = dijkstra_search, "Dijkstra's Algorithm"
                if event.key == pygame.K_w:
                    algorithm_func, algorithm_name = weighted_a_star_search, "Weighted A* (1.5x)"

                if event.key == pygame.K_SPACE and start_node and end_node:
                    # --- NEW: Calculate metrics ---
                    total_explored = 0
                    start_time = time.time()
                    
                    def draw_callback_with_counter(open_set, closed_set):
                        nonlocal total_explored
                        total_explored = len(closed_set)
                        draw(win, grid, ROWS, GRID_WIDTH, start_node, end_node, open_set, closed_set, algo_name=algorithm_name)

                    found, path = algorithm_func(draw_callback_with_counter, grid, start_node, end_node)
                    end_time = time.time()
                    
                    if found:
                        last_metrics = {
                            "time": end_time - start_time,
                            "length": len(path),
                            "explored": total_explored
                        }
                        draw(win, grid, ROWS, GRID_WIDTH, start_node, end_node, path=path, algo_name=algorithm_name, metrics=last_metrics)

                if event.key == pygame.K_c:
                    start_node, end_node, last_metrics = None, None, None
                    grid = Grid(ROWS, ROWS)

    pygame.quit()

if __name__ == "__main__":
    main(WIN, WIDTH)