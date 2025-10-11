# Pathfinding Algorithm Visualizer

A comprehensive Python-based visualization tool for comparing multiple pathfinding algorithms with interactive grid manipulation, terrain costs, maze generation, and performance benchmarking.

## Features

- **Multiple Pathfinding Algorithms**: A*, Dijkstra, Weighted A*, Jump Point Search (JPS), Theta*, and Bidirectional Search
- **Interactive Visualization**: Real-time visualization of algorithm execution with color-coded nodes
- **Terrain System**: Support for variable terrain costs (swamp, road, normal)
- **Maze Generation**: Recursive backtracking algorithm for instant maze creation
- **Performance Benchmarking**: Automated comparison of all algorithms with detailed metrics
- **Visual Analytics**: Matplotlib-powered charts comparing execution time, path length, and nodes explored

## Prerequisites 

- Python 3.7+
- pip (Python package manager)

## Installation

1. Clone or download the project files
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Dependencies

- `pygame` - Interactive visualization and GUI
- `matplotlib` - Performance benchmark visualization
- `numpy` - Data processing for charts

## Usage

### Starting the Application

```bash
python main.py
```

### Controls

#### Mouse Controls
- **Left Click**: Place start node (green) → Place end node (red) → Draw obstacles (black)
- **Right Click**: Remove nodes/obstacles

#### Keyboard Shortcuts - Algorithm Selection
- `A` - A* Search (default)
- `D` - Dijkstra's Algorithm
- `W` - Weighted A* (1.5x heuristic weight)
- `J` - Jump Point Search
- `T` - Theta* (Any-Angle Pathfinding)
- `B` - Bidirectional Search

#### Keyboard Shortcuts - Terrain Painting
Hold while left-clicking to paint terrain:
- `1` - Paint Swamp (5x movement cost, dark green)
- `2` - Paint Road (0.5x movement cost, yellow)
- `0` - Erase terrain (return to normal cost)

#### Keyboard Shortcuts - Actions
- `SPACE` - Execute selected algorithm
- `M` - Generate random maze
- `X` - Run benchmark (compares all algorithms)
- `C` - Clear grid

### Visual Indicators

| Color | Meaning |
|-------|---------|
| 🟩 Green | Start node |
| 🟥 Red | End node |
| ⬛ Black | Obstacle |
| 🟦 Blue | Final path |
| 🟧 Orange | Explored nodes (closed set) |
| 🟦 Turquoise | Open set (frontier) |
| 🟩 Dark Green | Swamp terrain (5x cost) |
| 🟨 Yellow | Road terrain (0.5x cost) |

## Project Structure

```
pathfinding-visualizer/
│
├── main.py           # Main application and GUI logic
├── algorithms.py     # Pathfinding algorithm implementations
├── grid.py          # Grid and Node data structures
├── requirements.txt # Project dependencies
└── README.md        # This file
```

## Algorithm Details

### A* Search
- **Heuristic**: Manhattan distance
- **Optimality**: Optimal with consistent heuristic
- **Use Case**: General-purpose pathfinding with good performance

### Dijkstra's Algorithm
- **Heuristic**: None (uniform cost search)
- **Optimality**: Always optimal
- **Use Case**: When all paths need exploration or no good heuristic exists

### Weighted A*
- **Heuristic**: Manhattan distance × 1.5
- **Optimality**: Suboptimal but faster
- **Use Case**: When speed is prioritized over optimal path

### Jump Point Search (JPS)
- **Heuristic**: Manhattan distance
- **Optimality**: Optimal on uniform-cost grids
- **Use Case**: Large open grids with sparse obstacles
- **Note**: Ignores terrain costs

### Theta*
- **Heuristic**: Euclidean distance
- **Optimality**: Near-optimal with any-angle paths
- **Use Case**: Realistic movement with diagonal shortcuts
- **Note**: May bypass some terrain costs due to line-of-sight

### Bidirectional Search
- **Heuristic**: Forward and backward A*
- **Optimality**: Optimal when paths meet
- **Use Case**: Long-distance pathfinding

## Benchmark Mode

Press `X` to run automated benchmarks comparing all algorithms on the current grid setup. Results include:

- **Execution Time** (milliseconds)
- **Path Length** (number of steps)
- **Nodes Explored** (search efficiency)

Results are displayed both in the console and as visual bar charts.

## Technical Implementation

### Core Components

**Node Class** (`grid.py`)
- Represents individual grid cells
- Stores position, obstacle status, terrain cost, and pathfinding costs (g, h, f)

**Grid Class** (`grid.py`)
- Manages 2D array of nodes
- Handles neighbor retrieval, line-of-sight checks, and maze generation

**Algorithm Functions** (`algorithms.py`)
- Implements all pathfinding algorithms
- Returns success status, path, and exploration metrics

### Performance Considerations

- Priority queue (heapq) for efficient node selection
- Hash sets for O(1) membership testing
- Optimized neighbor iteration
- Minimal memory footprint

## Use Cases

- **Education**: Learn and compare pathfinding algorithms visually
- **Game Development**: Prototype AI navigation systems
- **Research**: Analyze algorithm performance under different conditions
- **Interviews**: Demonstrate understanding of graph algorithms

## Known Limitations

- JPS does not respect terrain costs (optimized for uniform grids)
- Theta* may produce paths that partially ignore terrain due to any-angle optimization
- Grid size fixed at 40×40 (modifiable in source code)
- Large mazes may impact real-time visualization performance

## Contributing

This is an educational project. Feel free to fork and extend with:
- Additional algorithms (D*, LPA*, etc.)
- Configurable grid sizes
- Save/load functionality
- 3D pathfinding

## License

This project is provided as-is for educational purposes.

## Resources

- [A* Algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm)
- [Jump Point Search Paper](https://users.cecs.anu.edu.au/~dharabor/data/papers/harabor-grastien-aaai11.pdf)
- [Theta* Paper](http://idm-lab.org/bib/abstracts/papers/aaai07b.pdf)

## Support

For issues or questions, please refer to the algorithm documentation or Python library documentation for pygame and matplotlib.

---

**Last Updated**: October 2025  
**Python Version**: 3.7+  
**Platform**: Cross-platform (Windows, macOS, Linux)
