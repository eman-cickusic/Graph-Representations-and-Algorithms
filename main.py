import pygame
import time
# NEW: Import matplotlib and numpy for plotting
import matplotlib.pyplot as plt
import numpy as np

from grid import Grid, Node
from algorithms import a_star_search, dijkstra_search, weighted_a_star_search, jps_search, theta_star_search, bidirectional_search

# --- Constants ---
WIDTH, HEIGHT = 600, 720
# ... (Colors are unchanged) ...
WHITE, BLACK, GREY = (255, 255, 255), (0, 0, 0), (128, 128, 128)
GREEN, RED, BLUE = (0, 255, 0), (255, 0, 0), (64, 200, 224)
TURQUOISE, ORANGE = (175, 238, 238), (255, 215, 180)
ORANGE_FWD, ORANGE_BWD = (255, 200, 100), (255, 150, 50)
SWAMP_GREEN, ROAD_YELLOW = (52, 84, 46), (214, 201, 142)

# --- Pygame Setup ---
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Visualizer")
pygame.font.init()
FONT = pygame.font.SysFont('arial', 18)
SMALL_FONT = pygame.font.SysFont('arial', 14)

# --- Drawing and Helper Functions (Unchanged) ---
def get_clicked_pos(pos, rows, width):
    gap = width // rows; x, y = pos
    if y >= width: return -1, -1
    return y // gap, x // gap
def draw_nodes(win, grid_obj, rows, width, start_node=None, end_node=None, open_set=None, closed_set=None, path=None, open_set_bwd=None, closed_set_fwd=None, closed_set_bwd=None):
    gap = width // rows
    open_set, closed_set = open_set or set(), closed_set or set()
    closed_set_fwd, closed_set_bwd = closed_set_fwd or set(), closed_set_bwd or set()
    open_set_bwd = open_set_bwd or set()
    path = path or []
    for row in grid_obj.grid:
        for node in row:
            if node.terrain_cost == 5: color = SWAMP_GREEN
            elif node.terrain_cost == 0.5: color = ROAD_YELLOW
            else: color = WHITE
            if closed_set_fwd:
                if node in closed_set_fwd: color = ORANGE_FWD
                if node in closed_set_bwd: color = ORANGE_BWD
            else:
                if node in closed_set: color = ORANGE
            if node in open_set or node in open_set_bwd: color = TURQUOISE
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
def draw(win, grid_obj, rows, width, start_node=None, end_node=None, open_set=None, closed_set=None, path=None, algo_name="", metrics=None, open_set_bwd=None, closed_set_fwd=None, closed_set_bwd=None):
    win.fill(WHITE)
    grid_area_height = width
    info_text_1 = FONT.render(f"Algorithm: {algo_name}", True, BLACK)
    win.blit(info_text_1, (10, grid_area_height + 5))
    if algo_name == "Jump Point Search":
        warning_text = SMALL_FONT.render("(NOTE: JPS ignores terrain costs)", True, RED)
        win.blit(warning_text, (info_text_1.get_width() + 15, grid_area_height + 8))
    if algo_name == "Theta* (Any-Angle)":
        warning_text = SMALL_FONT.render("(NOTE: Any-angle shortcuts may ignore some terrain costs)", True, (200, 100, 0))
        win.blit(warning_text, (info_text_1.get_width() + 15, grid_area_height + 8))
    info_text_2 = FONT.render("C: Clear | M: Maze | X: Benchmark | SPACE: Run", True, BLACK)
    win.blit(info_text_2, (10, grid_area_height + 25))
    info_text_3 = FONT.render("Select: A/D/W/J/T/B | Paint: 1-Swamp 2-Road 0-Erase", True, BLACK)
    win.blit(info_text_3, (10, grid_area_height + 45))
    if metrics:
        metrics_text = FONT.render(f"Time: {metrics['time']:.4f}s | Path Length: {metrics['length']} | Nodes Explored: {metrics['explored']}", True, BLACK)
        win.blit(metrics_text, (10, grid_area_height + 65))
    draw_nodes(win, grid_obj, rows, width, start_node, end_node, open_set, closed_set, path, open_set_bwd, closed_set_fwd, closed_set_bwd)
    draw_grid_lines(win, rows, width)

# --- Benchmarking and Visualization Functions ---

# MODIFIED: Greatly improved plotting layout and style
def visualize_benchmark_results(results):
    names = list(results.keys())
    times = [res['time'] for res in results.values()]
    lengths = [res['path_len'] if res['path_len'] != "N/A" else 0 for res in results.values()]
    explored = [res['explored'] for res in results.values()]

    fig, axs = plt.subplots(3, 1, figsize=(10, 12)) # Adjusted figure size
    fig.suptitle('Algorithm Benchmark Results', fontsize=16, y=0.99)

    # Plot 1: Execution Time
    bars_time = axs[0].bar(names, times, color='skyblue')
    axs[0].set_ylabel('Time (ms)')
    axs[0].set_title('Execution Time')
    axs[0].bar_label(bars_time, fmt='%.2f', padding=3) # Added padding
    
    # Plot 2: Path Length
    bars_len = axs[1].bar(names, lengths, color='lightgreen')
    axs[1].set_ylabel('Number of Steps')
    axs[1].set_title('Path Length')
    axs[1].bar_label(bars_len, padding=3) # Added padding

    # Plot 3: Nodes Explored
    bars_exp = axs[2].bar(names, explored, color='salmon')
    axs[2].set_ylabel('Node Count')
    axs[2].set_title('Nodes Explored')
    axs[2].bar_label(bars_exp, padding=3) # Added padding

    # Rotate x-axis labels for all subplots to prevent overlap
    for ax in axs:
        ax.tick_params(axis='x', rotation=15)

    # Improve layout: Add vertical space between plots
    fig.subplots_adjust(hspace=0.6) 
    
    plt.show()

def run_benchmark(grid, start_node, end_node):
    if not start_node or not end_node:
        print("\n[BENCHMARK FAILED] Please set a start and end node first."); return
    algorithms_to_test = {"A*": a_star_search, "Dijkstra": dijkstra_search, "Weighted A*": weighted_a_star_search, "Theta*": theta_star_search, "Bidirectional": bidirectional_search, "JPS": jps_search}
    results = {}
    for name, func in algorithms_to_test.items():
        start_time = time.perf_counter()
        found, path, explored = func(None, grid, start_node, end_node)
        end_time = time.perf_counter()
        results[name] = {'time': (end_time - start_time) * 1000, 'path_len': len(path) if found else "N/A", 'explored': explored}
    print("\n" + "="*50); print(" " * 15 + "BENCHMARK RESULTS"); print("="*50)
    print(f"{'Algorithm':<15} | {'Time (ms)':<10} | {'Path Len':<10} | {'Explored':<10}"); print("-"*50)
    for name, res in results.items():
        print(f"{name:<15} | {res['time']:<10.3f} | {str(res['path_len']):<10} | {res['explored']:<10}")
    print("="*50)
    visualize_benchmark_results(results)

# --- Main Application Loop ---
def main(win, width):
    GRID_WIDTH = width; ROWS = 40
    grid = Grid(ROWS, ROWS)
    start_node, end_node = None, None
    run = True
    algorithm_func = a_star_search; algorithm_name = "A* Search"
    last_metrics = None
    while run:
        if algorithm_name == "Bidirectional Search":
             draw(win, grid, ROWS, GRID_WIDTH, start_node, end_node, algo_name=algorithm_name, metrics=last_metrics, closed_set_fwd=set(), closed_set_bwd=set())
        else:
            draw(win, grid, ROWS, GRID_WIDTH, start_node, end_node, algo_name=algorithm_name, metrics=last_metrics)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False
            if pygame.mouse.get_pressed()[0]:
                keys = pygame.key.get_pressed()
                if not (keys[pygame.K_1] or keys[pygame.K_2] or keys[pygame.K_0]):
                    pos = pygame.mouse.get_pos(); row, col = get_clicked_pos(pos, ROWS, GRID_WIDTH)
                    if row != -1:
                        node = grid.get_node(row, col)
                        if node and not node.is_obstacle:
                            if not start_node and node != end_node: start_node = node
                            elif not end_node and node != start_node: end_node = node
                            elif node != end_node and node != start_node: node.set_obstacle(True)
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos(); row, col = get_clicked_pos(pos, ROWS, GRID_WIDTH)
                if row != -1:
                    node = grid.get_node(row, col)
                    if node:
                        node.set_obstacle(False)
                        if node == start_node: start_node = None
                        if node == end_node: end_node = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a: algorithm_func, algorithm_name = a_star_search, "A* Search"
                if event.key == pygame.K_d: algorithm_func, algorithm_name = dijkstra_search, "Dijkstra's Algorithm"
                if event.key == pygame.K_w: algorithm_func, algorithm_name = weighted_a_star_search, "Weighted A* (1.5x)"
                if event.key == pygame.K_j: algorithm_func, algorithm_name = jps_search, "Jump Point Search"
                if event.key == pygame.K_t: algorithm_func, algorithm_name = theta_star_search, "Theta* (Any-Angle)"
                if event.key == pygame.K_b: algorithm_func, algorithm_name = bidirectional_search, "Bidirectional Search"
                if event.key == pygame.K_m: grid.generate_maze(); start_node, end_node, last_metrics = None, None, None
                if event.key == pygame.K_x: run_benchmark(grid, start_node, end_node)
                if event.key == pygame.K_SPACE and start_node and end_node:
                    start_time = time.time()
                    def callback_handler(*args, **kwargs):
                        if algorithm_name == "Bidirectional Search":
                            draw(win, grid, ROWS, GRID_WIDTH, start_node, end_node, open_set=args[0], closed_set_fwd=args[1], open_set_bwd=args[2], closed_set_bwd=args[3], algo_name=algorithm_name)
                        else:
                            draw(win, grid, ROWS, GRID_WIDTH, start_node, end_node, **kwargs, algo_name=algorithm_name)
                        pygame.display.update()
                    found, path, total_explored = algorithm_func(callback_handler, grid, start_node, end_node)
                    end_time = time.time()
                    if found:
                        last_metrics = { "time": end_time - start_time, "length": len(path), "explored": total_explored }
                        draw(win, grid, ROWS, GRID_WIDTH, start_node, end_node, path=path, algo_name=algorithm_name, metrics=last_metrics)
                        pygame.display.update()
                if event.key == pygame.K_c:
                    grid = Grid(ROWS, ROWS); start_node, end_node, last_metrics = None, None, None
        keys = pygame.key.get_pressed(); mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            pos = pygame.mouse.get_pos(); row, col = get_clicked_pos(pos, ROWS, GRID_WIDTH)
            if row != -1:
                node = grid.get_node(row, col)
                if node and node != start_node and node != end_node:
                    if keys[pygame.K_1]: node.set_terrain(5); node.set_obstacle(False)
                    elif keys[pygame.K_2]: node.set_terrain(0.5); node.set_obstacle(False)
                    elif keys[pygame.K_0]: node.set_terrain(1); node.set_obstacle(False)
    pygame.quit()

if __name__ == "__main__":
    main(WIN, WIDTH)