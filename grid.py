# You will need this for the heuristic calculation later
import math

class Node:
    """
    A class to represent a single node in the grid.
    Each node knows its position, its costs for pathfinding, and its parent.
    """
    def __init__(self, row, col, is_obstacle=False):
        self.row = row
        self.col = col
        self.is_obstacle = is_obstacle
        
        # --- Pathfinding Attributes ---
        self.g_cost = float('inf')  # Distance from the start node
        self.h_cost = float('inf')  # Heuristic distance to the end node
        self.f_cost = float('inf')  # Total cost (g_cost + h_cost)
        self.parent = None

    def __repr__(self):
        """String representation for a Node for easy debugging."""
        return f"Node({self.row}, {self.col})"

    def __lt__(self, other):
        """
        Comparison method for the priority queue.
        It compares nodes based on their f_cost.
        """
        return self.f_cost < other.f_cost

    def set_obstacle(self, is_obstacle=True):
        """Sets or unsets the node as an obstacle."""
        self.is_obstacle = is_obstacle

    def reset(self):
        """Resets the pathfinding attributes of the node."""
        self.g_cost = float('inf')
        self.h_cost = float('inf')
        self.f_cost = float('inf')
        self.parent = None

class Grid:
    """
    A class to represent the entire grid of nodes.
    It handles grid creation and finding neighbors of a node.
    """
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = self._create_grid()

    def _create_grid(self):
        """
        Initializes a 2D list of Node objects.
        Helper function for the constructor.
        """
        grid = []
        for i in range(self.rows):
            grid.append([Node(i, j) for j in range(self.cols)])
        return grid

    def get_node(self, row, col):
        """Returns the node at a specific (row, col) position."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def get_neighbors(self, node):
        """
        Gets all valid, non-obstacle neighbors of a given node.
        This implementation allows for 8-directional movement (including diagonals).
        """
        neighbors = []
        # Possible movements: N, S, E, W, NE, NW, SE, SW
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue  # This is the node itself

                r, c = node.row + dr, node.col + dc

                if 0 <= r < self.rows and 0 <= c < self.cols:
                    neighbor_node = self.grid[r][c]
                    if not neighbor_node.is_obstacle:
                        neighbors.append(neighbor_node)
        return neighbors
        
    def reset_pathfinding_data(self):
        """Iterates through all nodes and resets their pathfinding attributes."""
        for row in self.grid:
            for node in row:
                node.reset()

# --- Example Usage (for testing if you wish) ---
if __name__ == '__main__':
    # Create a 10x10 grid
    my_grid = Grid(10, 10)

    # Get a specific node
    node_5_5 = my_grid.get_node(5, 5)
    print(f"Got node: {node_5_5}")

    # Set an obstacle
    obstacle_node = my_grid.get_node(5, 6)
    obstacle_node.set_obstacle(True)
    print(f"Is node (5, 6) an obstacle? {obstacle_node.is_obstacle}")

    # Get neighbors of our node (should not include the obstacle)
    neighbors = my_grid.get_neighbors(node_5_5)
    print(f"Neighbors of {node_5_5}: {neighbors}")

    # Reset the grid for a new pathfinding run
    my_grid.reset_pathfinding_data()
    print("Grid pathfinding data has been reset.")