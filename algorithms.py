import pygame
import heapq
import math
from grid import Node, Grid

# --- Helper Functions (Unchanged) ---
def _heuristic(node_a, node_b):
    return abs(node_a.row - node_b.row) + abs(node_a.col - node_b.col)

def _get_distance(node_a, node_b):
    dist_row = node_a.row - node_b.row
    dist_col = node_a.col - node_b.col
    return math.sqrt(dist_row**2 + dist_col**2)

def _reconstruct_path(end_node):
    path = []
    current_node = end_node
    while current_node is not None:
        path.append(current_node)
        current_node = current_node.parent
    return path[::-1]

# --- Core A* Algorithm (Unchanged) ---
def a_star_search(draw_callback, grid, start_node, end_node, weight=1.0):
    grid.reset_pathfinding_data()
    open_set_heap = []
    open_set_hash = {start_node}
    closed_set = set()
    start_node.g_cost = 0
    start_node.h_cost = _heuristic(start_node, end_node)
    start_node.f_cost = start_node.g_cost + (start_node.h_cost * weight)
    heapq.heappush(open_set_heap, (start_node.f_cost, start_node))

    while open_set_heap:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False, {}
        _, current_node = heapq.heappop(open_set_heap)
        open_set_hash.remove(current_node)
        if current_node == end_node:
            path = _reconstruct_path(end_node)
            return True, path
        for neighbor in grid.get_neighbors(current_node):
            if neighbor in closed_set:
                continue
            tentative_g_cost = current_node.g_cost + _get_distance(current_node, neighbor)
            if tentative_g_cost < neighbor.g_cost:
                neighbor.parent = current_node
                neighbor.g_cost = tentative_g_cost
                neighbor.h_cost = _heuristic(neighbor, end_node)
                neighbor.f_cost = neighbor.g_cost + (neighbor.h_cost * weight)
                if neighbor not in open_set_hash:
                    heapq.heappush(open_set_heap, (neighbor.f_cost, neighbor))
                    open_set_hash.add(neighbor)
        draw_callback(open_set=open_set_hash, closed_set=closed_set)
        if current_node != start_node:
            closed_set.add(current_node)
    return False, {}

# --- Algorithm Wrappers (MODIFIED) ---

def dijkstra_search(draw_callback, grid, start_node, end_node):
    """
    Dijkstra's is A* with the heuristic weight set to 0.
    We now pass the draw_callback through.
    """
    return a_star_search(draw_callback, grid, start_node, end_node, weight=0.0)

def weighted_a_star_search(draw_callback, grid, start_node, end_node, weight=1.5):
    """
    Weighted A* with a default weight of 1.5.
    We now pass the draw_callback through.
    """
    return a_star_search(draw_callback, grid, start_node, end_node, weight=weight)