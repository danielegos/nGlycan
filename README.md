# N-Glycan DCI v0.01

## Overview
This Python program allows the user to interactively create a grid of nodes and edges representing an N-glycan structure. It includes features to add and remove nodes and edges, and calculates a "Distance & Connectivity Index (DCI)" based on the structure. The program uses a graphical interface built with Tkinter.

## Features
- **Grid Creation**: Visualize and manipulate a grid where nodes (vertices) can be added and connected.
- **Node and Edge Management**: Add, remove, and modify nodes and edges.
- **DCI Calculation**: Compute a Distance & Connectivity Index (DCI) score, which is a weighted sum based on node distances and degrees.
- **Graphical Interface**: Intuitive GUI with buttons for managing the grid and calculating the DCI score.
- **Pathfinding and Degree Counting**: Automatically calculates paths from each node to the base node and counts the degree of each node.

## Requirements
- Python 3.x
- Tkinter library (usually pre-installed with Python)
- PrettyTable library (for displaying tables):
  ```bash
  pip install prettytable
  ```

## Usage

### 1. Running the Program
To run the program, execute the script with Python:
```bash
python nglycan_dci.py
```

### 2. Interacting with the Interface
- **Add Circle**: Click on the grid to add nodes. The first node placed is the base node.
- **Remove Circle**: Click on an existing node to remove it.
- **Add Edge**: Click two different nodes to add an edge between them.
- **Remove Edge**: Click an existing edge to remove it.
- **Calculate DCI**: After creating the graph, click this button to calculate the DCI score based on the node connections.

### 3. Instructions
The grid represents an N-glycan structure. The first node you place is the base node, and subsequent nodes are added with constraints based on distance and alignment.

### 4. Resetting the Program
Click the **Reset Program** button to clear the grid and start over.

### 5. Output
The program prints the following information:
- The weighted matrix for the N-glycan structure.
- The Distance & Connectivity Index (DCI) score for the structure.

## Assumptions
1. The first circle added is the base node.
2. Only edges between adjacent nodes can be drawn.
3. No fucosylation occurs at the base node.
4. The graph is undirected, and edges are added between two nodes only.

## File Structure
- **nglycan_dci.py**: Main script containing the application code.
- **output.txt**: (Optional) If directed, the output will be saved to a text file.

## License
This project is open-source and available under the MIT License.
