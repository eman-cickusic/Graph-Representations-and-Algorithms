import math
import random # NEW: Import the random library for maze generation

class Node:
    # (This class is unchanged from the previous step)
    def __init__(self, row, col, is_obstacle=False):
        self.row = row
        self.col = col
        self.is_obstacle = is_obstacle
        self.terrain_cost = 1
        self.g_cost = float('inf')
        self.h_cost = float('inf')
        self.f_cost = float('inf')
        self.parent = None
    def __repr__(self):
        return f"Node({self.row}, {self.col})"
    def __lt__(self, other):
        return self.f_cost < other.f_cost
    def set_obstacle(self, is_obstacle=True):
        self.is_obstacle = is_obstacle
    def set_terrain(self, cost):
        self.terrain_cost = cost
    def reset(self):
        self.g_cost = float('inf')
        self.h_cost = float('inf')
        self.f_cost = float('inf')
        self.parent = None

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = self._create_grid()

    def _create_grid(self):
        # (This method is unchanged)
        grid = []
        for i in range(self.rows):
            grid.append([Node(i, j) for j in range(self.cols)])
        return grid

    def get_node(self, row, col):
        # (This method is unchanged)
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def get_neighbors(self, node):
        # (This method is unchanged)
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = node.row + dr, node.col + dc
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    neighbor_node = self.grid[r][c]
                    if not neighbor_node.is_obstacle:
                        neighbors.append(neighbor_node)
        return neighbors

    def reset_pathfinding_data(self):
        # (This method is unchanged)
        for row in self.grid:
            for node in row:
                node.reset()
    
    def line_of_sight(self, node1, node2):
        # (This method is unchanged)
        x0, y0 = node1.col, node1.row
        x1, y1 = node2.col, node2.row
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        x, y = x0, y0
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            node = self.get_node(y, x)
            if node is None or node.is_obstacle:
                return False
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy
        return True

    # NEW: Maze generation using recursive backtracking
    def generate_maze(self, start_row=0, start_col=0):
        """ Generates a perfect maze on the grid. """
        # 1. Start with a grid full of walls.
        for row in self.grid:
            for node in row:
                node.set_obstacle(True)
                node.set_terrain(1) # Reset terrain

        stack = []
        start_node = self.get_node(start_row, start_col)
        start_node.set_obstacle(False)
        stack.append(start_node)

        while stack:
            current_node = stack[-1]
            r, c = current_node.row, current_node.col
            
            neighbors = []
            # Check neighbors 2 cells away
            for dr, dc in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    neighbor = self.get_node(nr, nc)
                    if neighbor.is_obstacle:
                        neighbors.append(neighbor)
            
            if neighbors:
                next_node = random.choice(neighbors)
                
                # Carve the path between current and next node
                wall_r = (r + next_node.row) // 2
                wall_c = (c + next_node.col) // 2
                wall_between = self.get_node(wall_r, wall_c)
                
                wall_between.set_obstacle(False)
                next_node.set_obstacle(False)
                
                stack.append(next_node)
            else:
                stack.pop()