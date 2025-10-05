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

# --- Core A* Algorithm (MODIFIED to return metrics) ---
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
        if draw_callback:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False, {}, 0
        _, current_node = heapq.heappop(open_set_heap)
        open_set_hash.remove(current_node)
        if current_node == end_node:
            path = _reconstruct_path(end_node)
            return True, path, len(closed_set)
        for neighbor in grid.get_neighbors(current_node):
            if neighbor in closed_set:
                continue
            step_cost = _get_distance(current_node, neighbor) * neighbor.terrain_cost
            tentative_g_cost = current_node.g_cost + step_cost
            if tentative_g_cost < neighbor.g_cost:
                neighbor.parent = current_node
                neighbor.g_cost = tentative_g_cost
                neighbor.h_cost = _heuristic(neighbor, end_node)
                neighbor.f_cost = neighbor.g_cost + (neighbor.h_cost * weight)
                if neighbor not in open_set_hash:
                    heapq.heappush(open_set_heap, (neighbor.f_cost, neighbor))
                    open_set_hash.add(neighbor)
        if draw_callback:
            draw_callback(open_set=open_set_hash, closed_set=closed_set)
        if current_node != start_node:
            closed_set.add(current_node)
    return False, {}, len(closed_set)

# --- Wrappers (Unchanged) ---
def dijkstra_search(draw_callback, grid, start_node, end_node):
    return a_star_search(draw_callback, grid, start_node, end_node, weight=0.0)

def weighted_a_star_search(draw_callback, grid, start_node, end_node, weight=1.5):
    return a_star_search(draw_callback, grid, start_node, end_node, weight=weight)

# --- JPS Implementation (MODIFIED to return metrics) ---
# ... (Helper functions _is_walkable, _identify_successors, _jump are unchanged) ...
def _is_walkable(grid, row, col):
    node = grid.get_node(row, col)
    return node is not None and not node.is_obstacle
def _identify_successors(grid, current_node, start_node, end_node):
    successors, neighbors, parent = [], [], current_node.parent
    r, c = current_node.row, current_node.col
    if parent is None:
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                if dr==0 and dc==0: continue
                if _is_walkable(grid, r+dr, c+dc): neighbors.append((dr,dc))
    else:
        pr, pc = parent.row, parent.col
        dr, dc = (r - pr) // max(1, abs(r-pr)), (c - pc) // max(1, abs(c-pc))
        if dr != 0 and dc != 0:
            if _is_walkable(grid, r, c+dc): neighbors.append((0,dc))
            if _is_walkable(grid, r+dr, c): neighbors.append((dr,0))
            if _is_walkable(grid, r, c+dc) or _is_walkable(grid, r+dr,c):
                if _is_walkable(grid, r+dr, c+dc): neighbors.append((dr,dc))
            if not _is_walkable(grid, r, c-dc) and _is_walkable(grid, r+dr, c-dc): neighbors.append((dr,-dc))
            if not _is_walkable(grid, r-dr, c) and _is_walkable(grid, r-dr, c+dc): neighbors.append((-dr,dc))
        else:
            if dr == 0:
                if _is_walkable(grid, r, c+dc):
                    neighbors.append((0,dc))
                    if not _is_walkable(grid, r+1, c): neighbors.append((1,dc))
                    if not _is_walkable(grid, r-1, c): neighbors.append((-1,dc))
            else:
                if _is_walkable(grid, r+dr, c):
                    neighbors.append((dr,0))
                    if not _is_walkable(grid, r, c+1): neighbors.append((dr,1))
                    if not _is_walkable(grid, r, c-1): neighbors.append((dr,-1))
    for dr, dc in neighbors:
        jump_point = _jump(grid, r, c, dr, dc, start_node, end_node)
        if jump_point: successors.append(jump_point)
    return successors
def _jump(grid, r, c, dr, dc, start_node, end_node):
    nr, nc = r+dr, c+dc
    if not _is_walkable(grid, nr, nc): return None
    neighbor_node = grid.get_node(nr, nc)
    if neighbor_node == end_node: return neighbor_node
    if dr!=0 and dc!=0:
        if (not _is_walkable(grid, nr-dr, nc) and _is_walkable(grid, nr-dr, nc+dc)) or \
           (not _is_walkable(grid, nr, nc-dc) and _is_walkable(grid, nr+dr, nc-dc)):
            return neighbor_node
    else:
        if dr!=0:
            if (not _is_walkable(grid, nr, nc+1) and _is_walkable(grid, nr+dr, nc+1)) or \
               (not _is_walkable(grid, nr, nc-1) and _is_walkable(grid, nr+dr, nc-1)):
                return neighbor_node
        else:
            if (not _is_walkable(grid, nr+1, nc) and _is_walkable(grid, nr+1, nc+dc)) or \
               (not _is_walkable(grid, nr-1, nc) and _is_walkable(grid, nr-1, nc+dc)):
                return neighbor_node
    if dr!=0 and dc!=0:
        if _jump(grid, nr, nc, dr, 0, start_node, end_node) or _jump(grid, nr, nc, 0, dc, start_node, end_node):
            return neighbor_node
    return _jump(grid, nr, nc, dr, dc, start_node, end_node)
def jps_search(draw_callback, grid, start_node, end_node):
    grid.reset_pathfinding_data()
    open_set_heap = []
    open_set_hash = {start_node}
    closed_set = set()
    start_node.g_cost = 0
    start_node.h_cost = _heuristic(start_node, end_node)
    start_node.f_cost = start_node.g_cost + start_node.h_cost
    heapq.heappush(open_set_heap, (start_node.f_cost, start_node))
    while open_set_heap:
        if draw_callback:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); return False, {}, 0
        _, current_node = heapq.heappop(open_set_heap)
        open_set_hash.remove(current_node)
        if current_node == end_node:
            path = _reconstruct_path(end_node)
            return True, path, len(closed_set)
        closed_set.add(current_node)
        successors = _identify_successors(grid, current_node, start_node, end_node)
        for successor in successors:
            if successor in closed_set: continue
            tentative_g_cost = current_node.g_cost + _get_distance(current_node, successor)
            if tentative_g_cost < successor.g_cost:
                successor.parent = current_node
                successor.g_cost = tentative_g_cost
                successor.h_cost = _heuristic(successor, end_node)
                successor.f_cost = successor.g_cost + successor.h_cost
                if successor not in open_set_hash:
                    heapq.heappush(open_set_heap, (successor.f_cost, successor))
                    open_set_hash.add(successor)
        if draw_callback:
            draw_callback(open_set=open_set_hash, closed_set=closed_set)
    return False, {}, len(closed_set)

# --- Theta* Implementation (MODIFIED to return metrics) ---
def theta_star_search(draw_callback, grid, start_node, end_node, weight=1.0):
    grid.reset_pathfinding_data()
    open_set_heap = []
    open_set_hash = {start_node}
    closed_set = set()
    start_node.g_cost = 0
    start_node.h_cost = _get_distance(start_node, end_node)
    start_node.f_cost = start_node.g_cost + (start_node.h_cost * weight)
    heapq.heappush(open_set_heap, (start_node.f_cost, start_node))
    while open_set_heap:
        if draw_callback:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); return False, {}, 0
        _, current_node = heapq.heappop(open_set_heap)
        open_set_hash.remove(current_node)
        if current_node == end_node:
            path = _reconstruct_path(end_node)
            return True, path, len(closed_set)
        closed_set.add(current_node)
        for neighbor in grid.get_neighbors(current_node):
            if neighbor in closed_set: continue
            parent = current_node.parent
            if parent is not None and grid.line_of_sight(parent, neighbor):
                tentative_g_cost = parent.g_cost + _get_distance(parent, neighbor)
                if tentative_g_cost < neighbor.g_cost:
                    neighbor.parent = parent
                    neighbor.g_cost = tentative_g_cost
                    neighbor.h_cost = _get_distance(neighbor, end_node)
                    neighbor.f_cost = neighbor.g_cost + (neighbor.h_cost * weight)
                    if neighbor not in open_set_hash:
                        heapq.heappush(open_set_heap, (neighbor.f_cost, neighbor))
                        open_set_hash.add(neighbor)
            else:
                step_cost = _get_distance(current_node, neighbor) * neighbor.terrain_cost
                tentative_g_cost = current_node.g_cost + step_cost
                if tentative_g_cost < neighbor.g_cost:
                    neighbor.parent = current_node
                    neighbor.g_cost = tentative_g_cost
                    neighbor.h_cost = _get_distance(neighbor, end_node)
                    neighbor.f_cost = neighbor.g_cost + (neighbor.h_cost * weight)
                    if neighbor not in open_set_hash:
                        heapq.heappush(open_set_heap, (neighbor.f_cost, neighbor))
                        open_set_hash.add(neighbor)
        if draw_callback:
            draw_callback(open_set=open_set_hash, closed_set=closed_set)
    return False, {}, len(closed_set)

# --- Bidirectional Search Implementation (MODIFIED to return metrics) ---
# ... (_reconstruct_bidirectional_path is unchanged) ...
def _reconstruct_bidirectional_path(meeting_node, start_node, end_node, parent_map_fwd, parent_map_bwd):
    path_fwd = []
    current = meeting_node
    while current != start_node:
        path_fwd.append(current)
        current = parent_map_fwd[current]
    path_fwd.append(start_node)
    path_fwd.reverse()
    path_bwd = []
    current = meeting_node
    while current != end_node:
        path_bwd.append(current)
        current = parent_map_bwd[current]
    path_bwd.append(end_node)
    return path_fwd + path_bwd[1:]
def bidirectional_search(draw_callback, grid, start_node, end_node, weight=1.0):
    grid.reset_pathfinding_data()
    open_set_fwd, closed_set_fwd = {start_node}, set()
    g_cost_fwd = {node: float('inf') for row in grid.grid for node in row}
    g_cost_fwd[start_node] = 0
    parent_map_fwd = {}
    open_set_bwd, closed_set_bwd = {end_node}, set()
    g_cost_bwd = {node: float('inf') for row in grid.grid for node in row}
    g_cost_bwd[end_node] = 0
    parent_map_bwd = {}
    while open_set_fwd and open_set_bwd:
        if draw_callback:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); return False, {}, 0
        # Forward Step
        current_fwd = min(open_set_fwd, key=lambda node: g_cost_fwd[node] + _heuristic(node, end_node) * weight)
        open_set_fwd.remove(current_fwd)
        closed_set_fwd.add(current_fwd)
        if current_fwd in closed_set_bwd:
            path = _reconstruct_bidirectional_path(current_fwd, start_node, end_node, parent_map_fwd, parent_map_bwd)
            return True, path, len(closed_set_fwd) + len(closed_set_bwd)
        for neighbor in grid.get_neighbors(current_fwd):
            if neighbor in closed_set_fwd: continue
            step_cost = _get_distance(current_fwd, neighbor) * neighbor.terrain_cost
            tentative_g_cost = g_cost_fwd[current_fwd] + step_cost
            if tentative_g_cost < g_cost_fwd[neighbor]:
                parent_map_fwd[neighbor] = current_fwd
                g_cost_fwd[neighbor] = tentative_g_cost
                if neighbor not in open_set_fwd:
                    open_set_fwd.add(neighbor)
        # Backward Step
        current_bwd = min(open_set_bwd, key=lambda node: g_cost_bwd[node] + _heuristic(node, start_node) * weight)
        open_set_bwd.remove(current_bwd)
        closed_set_bwd.add(current_bwd)
        if current_bwd in closed_set_fwd:
            path = _reconstruct_bidirectional_path(current_bwd, start_node, end_node, parent_map_fwd, parent_map_bwd)
            return True, path, len(closed_set_fwd) + len(closed_set_bwd)
        for neighbor in grid.get_neighbors(current_bwd):
            if neighbor in closed_set_bwd: continue
            step_cost = _get_distance(current_bwd, neighbor) * neighbor.terrain_cost
            tentative_g_cost = g_cost_bwd[current_bwd] + step_cost
            if tentative_g_cost < g_cost_bwd[neighbor]:
                parent_map_bwd[neighbor] = current_bwd
                g_cost_bwd[neighbor] = tentative_g_cost
                if neighbor not in open_set_bwd:
                    open_set_bwd.add(neighbor)
        if draw_callback:
            draw_callback(open_set_fwd, closed_set_fwd, open_set_bwd, closed_set_bwd)
    return False, {}, len(closed_set_fwd) + len(closed_set_bwd)