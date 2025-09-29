# Graph Representations and Algorithms: Interactive Tutorial

This project is an interactive educational tool designed to visualize and compare various pathfinding algorithms on a 2D grid. Users can create custom mazes, select different algorithms, and watch in real-time how they explore the grid to find the shortest path. The application also provides key performance metrics for direct comparison.

## Features

*   **Interactive Grid Editor:**
    *   Dynamically create and clear the grid.
    *   Use the mouse to place the **start** (green) and **end** (red) nodes.
    *   "Paint" and erase **obstacles** (black walls) with the mouse.

*   **Algorithm Selection:**
    *   Switch between three fundamental pathfinding algorithms on the fly:
        *   **A\* Search:** The industry-standard, efficient, and optimal algorithm.
        *   **Dijkstra's Algorithm:** A foundational algorithm that guarantees the shortest path but explores a larger area.
        *   **Weighted A\* Search:** A faster, "greedy" version of A\* that trades optimality for speed.

*   **Step-by-Step Visualization:**
    *   Watch the algorithms work in real-time.
    *   The **"open set"** (nodes being considered) is colored turquoise.
    *   The **"closed set"** (nodes already explored) is colored orange.
    *   The final, shortest path is drawn in blue.

*   **Comparative Analysis:**
    *   After a search is complete, key performance metrics are displayed on-screen:
        *   **Time:** The execution time of the search in seconds.
        *   **Path Length:** The number of nodes in the final path.
        *   **Nodes Explored:** The total number of nodes the algorithm had to check.

## How to Run

### Prerequisites
*   Python 3.x installed on your system.

### Steps
1.  **Place the Files:** Ensure `main.py`, `algorithms.py`, and `grid.py` are all in the same folder.
2.  **Install Dependencies:** Open a terminal in the project folder and install Pygame:
    ```bash
    python -m pip install pygame
    ```
3.  **Run the Application:** Execute the main script from the terminal:
    ```bash
    python main.py
    ```
    *(Note: If the `python` command does not work, you may need to use the full path to your Python executable as discovered during setup.)*

## Controls

*   **Left Click:**
    *   First click sets the **start node**.
    *   Second click sets the **end node**.
    *   Subsequent clicks/drags create **obstacles**.
*   **Right Click:** Erases any node (start, end, or obstacle).

*   **'A' Key:** Select **A\* Search**.
*   **'D' Key:** Select **Dijkstra's Algorithm**.
*   **'W' Key:** Select **Weighted A\* Search**.

*   **SPACE Bar:** Runs the currently selected algorithm.
*   **'C' Key:** Clears the entire grid, resetting everything.
