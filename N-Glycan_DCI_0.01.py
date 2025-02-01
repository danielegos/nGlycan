import tkinter as tk
import math
import os
import sys
from collections import deque
from prettytable import PrettyTable


# Define the class to redirect print() output to a Text widget
class PrintToText:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)  # Insert text at the end of the widget
        self.text_widget.yview(tk.END)  # Scroll to the end to show the new text

    def flush(self):
        pass  # This is required to avoid errors, but we don’t need it for this purpose


# Define the main application class
class GridApplication:
    def __init__(self, master):
        self.master = master
        self.master.title("N-Glycan DCI v0.01")

        # Create a Canvas widget
        self.canvas = tk.Canvas(self.master, width=1800, height=600, bg='#1E1F22') # Uncomment for large UI
        # self.canvas = tk.Canvas(self.master, width=600, height=600, bg='#1E1F22')  # Uncomment for small UI
        self.canvas.pack()

        # Grid size
        self.grid_size = 50
        self.vertices = []  # List to store the centers of circles

        # Dictionaries to store edges and circles
        self.edges = {}  # List to store edges
        self.circles = {}  # Dictionary to store circle items


        # Flag to track if the first circle has been placed
        self.first_circle_placed = False
        self.first_vertex = None  # Track the first selected vertex for edges

        # Mode tracking
        self.mode = None  # Default mode is Circle
        self.start_x = None
        self.start_y = None
        self.current_line = None  # To track the current line being drawn

        # Draw grid
        self.draw_grid()

        # Buttons for mode selection
        self.add_circle_button = tk.Button(self.master, text="Add Circle", command=self.select_add_circle_mode, background="#2B2D30", foreground="#DFE1E5")
        self.add_circle_button.pack(side="left", padx=5)

        self.rm_circle_button = tk.Button(self.master, text="Remove Circle", command=self.select_rm_circle_mode, background="#2B2D30", foreground="#DFE1E5")
        self.rm_circle_button.pack(side="left", padx=5)

        self.add_edge_button = tk.Button(self.master, text="Add Edge", command=self.select_add_edge_mode, background="#2B2D30", foreground="#DFE1E5")
        self.add_edge_button.pack(side="left", padx=5)

        self.rm_edge_button = tk.Button(self.master, text="Remove Edge", command=self.select_rm_edge_mode, background="#2B2D30", foreground="#DFE1E5")
        self.rm_edge_button.pack(side="left", padx=5)

        # Button to calculate DCI
        self.dci_calc_button = tk.Button(self.master, text="Calculate DCI", command=self.select_calc_dci_mode, background="#639F52", foreground="#1E1F22")
        self.dci_calc_button.pack(side="left", padx=5)

        # Button to reset program
        self.reset_button = tk.Button(self.master, text="Reset Program", command=self.reset_program, background="#AA4926", foreground="#DFE1E5")
        self.reset_button.pack(side="left", padx=5)

        # Create a Text widget for printing output
        self.text_area = tk.Text(self.master, height=100, width=200)
        self.text_area.pack(padx=10, pady=10)

        # Redirect print() to the Text widget
        printer = PrintToText(self.text_area)
        sys.stdout = printer

        print("Instructions:"
              "\nClick [Add Circle], then click on the left side of the grid to place the base node."
              "\nPlacement of subsequent nodes is restricted to specific points. "
              "Orient the N-glycan with the base node at the left and the furthest node on the right.")
        print("\nAssumptions:"
              "\n1) The first circle you add is the base node of the N-glycan. "
              "\n2) You will not attempt to duplicate edges."
              "\n3) You will only draw edges between two adjacent nodes."
              "\n4) No fucosylation occurs at the base node.")



        # Bind mouse events to canvas
        self.canvas.bind("<Button-1>", self.handle_click)  # Left click to place vertices or start edge

    def draw_grid(self):
        """Draw the grid lines on the canvas."""
        for i in range(0, 1800, self.grid_size):
            self.canvas.create_line(i, 0, i, 1800, fill="#2B2D30", tags="grid")
            self.canvas.create_line(0, i, 1800, i, fill="#2B2D30", tags="grid")

    def select_add_circle_mode(self):
        """Switch to Add Circle mode."""
        self.mode = "Add Circle"

    def select_add_edge_mode(self):
        """Switch to Add Edge mode."""
        self.mode = "Add Edge"

    def select_rm_circle_mode(self):
        """Switch to Remove Circle mode."""
        self.mode = "Remove Circle"

    def select_rm_edge_mode(self):
        """Switch to Remove Edge mode."""
        self.mode = "Remove Edge"

    def handle_click(self, event):
        """Handle click events for adding vertices or starting edges."""
        x, y = event.x, event.y

        # Check the current mode
        if self.mode == "Add Circle":
            # Place vertex in Circle mode
            grid_x = round(x / self.grid_size) * self.grid_size
            grid_y = round(y / self.grid_size) * self.grid_size

            if not self.first_circle_placed:
                self.add_vertex(grid_x, grid_y)
                self.first_circle_placed = True
                # print("First Vertex:",self.vertices)
            else:
                # Check if the distance condition (8 times the radius) and perpendicular/parallel condition hold
                radius = self.grid_size / 2
                for center in self.vertices:
                    dx = grid_x - center[0]
                    dy = grid_y - center[1]
                    distance = math.sqrt(dx ** 2 + dy ** 2)
                    required_distance = 8 * radius  # Distance should be eight times the radius

                    # If the distance is correct, check for perpendicular or parallel alignment
                    if abs(distance - required_distance) < self.grid_size / 2:
                        if grid_x == center[0] or grid_y == center[1]:  # Same x or same y
                            self.add_vertex(grid_x, grid_y)
                            # print("Adding Vertex:",self.vertices)
                            return  # Place only one circle per click

        elif self.mode == "Add Edge":
            # Handle adding edges (black) between two vertices
            grid_x = round(x / self.grid_size) * self.grid_size
            grid_y = round(y / self.grid_size) * self.grid_size

            if not self.first_vertex:
                # First click to select the first vertex for the edge
                if (grid_x, grid_y) in self.vertices:
                    self.first_vertex = (grid_x, grid_y)
                else:
                    print("First point must be an existing vertex!")
            else:
                # Second click to select the second vertex and add an edge
                if (grid_x, grid_y) in self.vertices and (grid_x, grid_y) != self.first_vertex:
                    self.add_edge(self.first_vertex, (grid_x, grid_y))
                    self.first_vertex = None  # Reset for the next edge creation
                else:
                    print("Second point must be an existing vertex and different from the first one!")

        elif self.mode == "Remove Circle":
            # Check if a circle exists at the clicked location
            item = self.canvas.find_closest(event.x, event.y)[0]
            if item in self.circles:
                self.canvas.delete(item)
                # print(self.circles[item])
                self.vertices.remove(self.circles[item])
                del self.circles[item]

                # print("\nPrinting vertices:",self.vertices)

        elif self.mode == "Remove Edge":
            # Check if an edge exists at the clicked location
            item = self.canvas.find_closest(event.x, event.y)[0]
            if item in self.edges:
                self.canvas.delete(item)
                del self.edges[item]

        # elif self.mode == "Calculate DCI":
        #     paths = self.find_paths_to_base(self.edges)
        #     self.calculate_dci(paths)

    def add_vertex(self, x, y):
        """Add a vertex and draw a blue circle."""
        radius = self.grid_size / 2
        self.vertices.append((x, y))

        # Draw blue circle with radius = 2 * vertex radius
        circle = self.canvas.create_oval(
            x - 2 * radius, y - 2 * radius,
            x + 2 * radius, y + 2 * radius,
            fill="#DFE1E5", outline="#DFE1E5", tags="circle" #, width=10
        )
        self.circles[circle] = (x, y)
        # print(self.circles)

    def add_edge(self, vertex1, vertex2):
        """Draw a black edge between two vertices."""
        # Draw a black edge between the selected vertices with increased width (3x)
        edge = self.canvas.create_line(
            vertex1[0], vertex1[1], vertex2[0], vertex2[1],
            width=10, fill="#AA4926", capstyle=tk.ROUND, tags="edge"
        )
        self.edges[edge] = (vertex1, vertex2)
        # print(self.edges)

    def reset_program(self):
        self.master.destroy()  # Destroy the current Tkinter root
        python = sys.executable  # Get the Python executable path
        os.execl(sys.executable, sys.executable, *sys.argv)

    def find_node_degrees(self, edges):
        """Computes the degree of each node in the graph."""
        graph = {}
        for edge in edges.values():
            a, b = edge
            if a not in graph:
                graph[a] = []
            if b not in graph:
                graph[b] = []
            graph[a].append(b)
            graph[b].append(a)

        return {node: len(neighbors) for node, neighbors in graph.items()}

    def find_paths_to_base(self, edges):
        # Step 1: Extract all nodes and find the base node
        nodes = set()
        for edge in edges.values():
            nodes.update(edge)
        base_node = min(nodes, key=lambda p: p[0])  # Node with lowest x-coordinate

        # Step 2: Build adjacency list
        graph = {node: [] for node in nodes}
        for edge in edges.values():
            a, b = edge
            graph[a].append(b)
            graph[b].append(a)

        # Step 3: BFS to find shortest paths to base node
        paths = {"A": {"path": [], "steps to base node": 0,
                       "degree_counts": {"2nd": 0, "3rd": 0, "4th": 0}}}  # Base node entry
        queue = deque([(base_node, [base_node])])
        visited = {base_node}

        key_label = iter("BCDEFGHIJKLMNOPQRSTUVWXYZ")
        key_map = {}

        # Get node_degrees
        node_degrees = self.find_node_degrees(edges)

        while queue:
            current, path = queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    # print("Printing new_path variable: ", new_path)
                    # print("Steps to base node of new_path: ", len(new_path) - 1)

                    # Increment node degrees based on whether each node in node_degrees is in new_path
                    second_degree_counter = 0
                    third_degree_counter = 0
                    fourth_degree_counter = 0

                    # Loop over keys
                    for key in node_degrees:
                        # print("Printing key label: ", key)
                        # print("Printing value label: ", value)
                        #                     print("Printing value at key label: ", node_degrees[key])
                        degree_for_node = node_degrees[key]
                        #                     print("Printing node_degrees: ", node_degrees)
                        # Check if key is in this node's path, but not including the node itself (exclude last index)
                        if key in new_path[:-1]:
                            # Increment the correct n-degree counter
                            if degree_for_node == 2:
                                second_degree_counter += 1
                                # print("Incrementing second degree counter: ", second_degree_counter)
                            if degree_for_node == 3:
                                third_degree_counter += 1
                            if degree_for_node == 4:
                                fourth_degree_counter += 1

                    key = next(key_label)
                    key_map[key] = {"path": new_path, "steps to base node": len(new_path) - 1, "degree_counts": {
                        "2nd": second_degree_counter,
                        "3rd": third_degree_counter,
                        "4th": fourth_degree_counter}
                                    }
                    queue.append((neighbor, new_path))

        paths.update(key_map)
        return paths

    def calculate_dci(self, paths):
        node_table = PrettyTable()
        node_table.field_names = ["Node",
                                  "Steps to Base Node",
                                  "2ndDeg Nodes\u2E4B * 2",
                                  "3rdDeg Nodes\u2E4B * 3",
                                  "4thDeg Nodes\u2E4B * 4",
                                  "Node Score"]

        # Extract information from paths dictionary and append that into the node_table_rows list
        #   Keep track of dci_score
        dci_score = 0
        for path in paths:
            row = []
            # print("Node:", path, "Path: ", paths[path]["path"], "Steps: ", paths[path]["steps to base node"], "2ndDeg Nodes: ", paths[path]["degree_counts"]["2nd"])
            # Use syntax above to get information from each path
            row.append(path)  # Path letter symbol
            row.append(paths[path]["steps to base node"])  # Steps to base node
            row.append(paths[path]["degree_counts"]["2nd"] * 2)  # Number of second degree nodes * Weight of 2
            row.append(paths[path]["degree_counts"]["3rd"] * 3)  # Number of third degree nodes * Weight of 3
            row.append(paths[path]["degree_counts"]["4th"] * 4)  # Number of fourth degree nodes * Weight of 4
            row.append(sum(row[1:5]))

            # Increment dci_score for each node (i.e., for each row in this table)
            dci_score += row[5]

            # Add row to node_table
            node_table.add_row(row)

        # Print completed, pretty table
        print("\nPrinting Weighted Matrix for Structure:\n", node_table,
              "\n\u2E4BExcluding the degree of the node in question. Weights equal node degree.")

        # Calculate dci_score by summing all node scores in node_table
        print("\n",
              "Distance & Connectivity Index (DCI Score): ", dci_score)

    def select_calc_dci_mode(self):
        """Switch to Edge mode."""
        self.mode = "Calculate DCI"
        paths = self.find_paths_to_base(self.edges)
        self.calculate_dci(paths)

# Create the main window and run the application
def main():
    root = tk.Tk()
    app = GridApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
