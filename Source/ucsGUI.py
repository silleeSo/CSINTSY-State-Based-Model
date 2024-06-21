import tkinter as tk
import heapq
import time
import threading
import tracemalloc
from tkinter.scrolledtext import ScrolledText


# Uniform Cost Search algorithm
class UniformCostSearch:
    def __init__(self, graph, canvas, coordinates):
        self.graph = graph
        self.canvas = canvas
        self.coordinates = coordinates

    def search(self, start, goal):
        # Priority queue to store nodes to be explored, starting with the initial node and cost of 0
        frontier = []
        heapq.heappush(frontier, (0, start))

        # Frequency count of node visits
        visit_count = {start: 1}

        # Track the maximum size of the priority queue
        max_frontier_size = 0

        # Store the cost to reach each node
        cost_so_far = {start: 0}
        # Store the path taken to reach each node
        came_from = {start: None}

        # Store all visited nodes
        visited_order = []

        while frontier:
            # Track the maximum size of the priority queue
            max_frontier_size = max(max_frontier_size, len(frontier))

            # Pop the node with the lowest cost from the priority queue
            current_cost, current_node = heapq.heappop(frontier)
            # Record the current node as visited
            visited_order.append(current_node)

            # Visualize the current step
            visualize_step(current_node, visited=True)

            # If the current node is the goal, reconstruct the path and return it
            if current_node == goal:
                path = []
                while current_node is not None:
                    path.append(current_node)
                    current_node = came_from[current_node]
                return visited_order, cost_so_far[goal], path[::-1], len(visited_order), max_frontier_size, visit_count

            # Explore neighbors of the current node
            for neighbor, cost in self.graph[current_node].items():
                # Calculate the new cost to reach the neighbor
                new_cost = current_cost + cost

                # If this path to the neighbor is cheaper, update cost and path
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(frontier, (new_cost, neighbor))
                    came_from[neighbor] = current_node
                    visit_count[neighbor] = visit_count.get(neighbor, 0) + 1

                    # Visualize the current step
                    visualize_step(current_node, neighbor)

        # If the goal is not reachable, return the visited order, infinity as cost, and an empty path
        return visited_order, float('inf'), [], len(visited_order), max_frontier_size, visit_count


# Function to visualize each step of the algorithm
def visualize_step(current, neighbor=None, visited=False):
    if visited:
        canvas.itemconfig(node_objects[current], fill="lightgreen")
    if neighbor:
        canvas.itemconfig(line_objects[(current, neighbor)], fill="yellow")
    root.update_idletasks()
    time.sleep(0.5)


# Create the main window
root = tk.Tk()
root.title("Uniform Cost Search | City Graph")
graph_label_uc = tk.Label(root, text="Uniform Cost Search", font=("Helvetica", 18, "bold"))
graph_label_uc.pack(pady=20)
# Create a canvas widget
canvas = tk.Canvas(root, width=800, height=600, bg="white")
canvas.pack()

# Define coordinates for each city
coordinates = {
    "Dallas": (200, 400),
    "Los Angeles": (100, 200),
    "San Francisco": (100, 100),
    "Chicago": (400, 50),
    "New York": (400, 200),
    "Boston": (600, 100),
    "Miami": (600, 300)
}

# Define the graph (connections between cities with distances)
graph = {
    "Dallas": {"Los Angeles": 1700, "Miami": 1200, "New York": 1500},
    "Los Angeles": {"San Francisco": 500, "Dallas": 1700, "New York": 3000},
    "San Francisco": {"Los Angeles": 500, "Chicago": 2200},
    "Chicago": {"San Francisco": 2200, "New York": 800},
    "New York": {"Chicago": 800, "Boston": 250, "Miami": 1000, "Dallas": 1500, "Los Angeles": 3000},
    "Boston": {"New York": 250},
    "Miami": {"New York": 1000, "Dallas": 1200}
}

# Create UniformCostSearch instance with the graph
ucs = UniformCostSearch(graph, canvas, coordinates)

# Draw the connections (edges) and distances
line_objects = {}
lines = []
for city1, connections in graph.items():
    for city2, distance in connections.items():
        x1, y1 = coordinates[city1]
        x2, y2 = coordinates[city2]
        line = canvas.create_line(x1, y1, x2, y2, fill="blue")
        line_objects[(city1, city2)] = line
        line_objects[(city2, city1)] = line  # Ensure both directions are covered
        lines.append((line, city1, city2))
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2

        # Create a background rectangle for the distance label
        bbox = canvas.create_text(mid_x, mid_y - 10, text=str(distance), fill="black")
        x0, y0, x1, y1 = canvas.bbox(bbox)
        canvas.create_rectangle(x0-2, y0-2, x1+2, y1+2, fill="pink", outline="")
        canvas.lift(bbox)  # Ensure the text is above the rectangle

# Draw the cities (nodes) with a background to hide overlapping lines
dropdown_vars = {}
node_objects = {}
for city, (x, y) in coordinates.items():
    # Draw a white rectangle behind the city label to hide the lines
    canvas.create_rectangle(x-50, y-30, x+50, y+30, fill="white", outline="white")
    node_rect = canvas.create_rectangle(x-48, y-28, x+48, y+28, outline="black", fill="white")
    node_objects[city] = node_rect
    canvas.create_text(x, y-10, text=city, fill="black")

    # Create dropdown inside each city box
    var = tk.StringVar(root)
    var.set(" ")  # Default value
    dropdown_vars[city] = var
    dropdown = tk.OptionMenu(canvas, var, " ", "Start", "End")
    dropdown.config(width=5, height=1, font=('Helvetica', 8))
    canvas.create_window(x, y + 12, window=dropdown)

# Function to find the path and display it
def find_path():
    start_city = None
    end_city = None
    
    for city, var in dropdown_vars.items():
        if var.get() == "Start":
            start_city = city
        elif var.get() == "End":
            end_city = city
    
    if start_city is not None and end_city is not None:
        # Measure time before executing the algorithm
        start_time = time.time()
        tracemalloc.start()  # Start memory tracking
        
        # Run the algorithm in a separate thread to keep the GUI responsive
        def run_algorithm():
            visited_order, total_cost, path, nodes_expanded, max_frontier_size, visit_count = ucs.search(start_city, end_city)
            
            # Measure time after executing the algorithm
            end_time = time.time()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            path_str = " -> ".join(path)
            visited_str = " -> ".join(visited_order)
            
            result_text = (
                f"Final Path: {path_str}\n\n"
                f"Path Traversed: {visited_str}\n\n"
                f"Total Cost: {total_cost}\n\n"
                f"Time: {end_time - start_time} seconds\n\n"
                f"Nodes Expanded: {nodes_expanded}\n\n"
                f"Max Frontier Size: {max_frontier_size}\n\n"
                f"Memory Usage: Current={current / 1024}KB, Peak={peak / 1024}KB\n\n"
                f"Visit Count: {visit_count}"
            )

            # Clear previous result and insert new result
            result_text_widget.delete(1.0, tk.END)
            result_text_widget.insert(tk.END, result_text)

            # Highlight the final best path
            for line, city1, city2 in lines:
                if (city1, city2) in zip(path, path[1:]) or (city2, city1) in zip(path, path[1:]):
                    canvas.itemconfig(line, fill="red", width=3)
                else:
                    canvas.itemconfig(line, fill="blue", width=1)
        
        threading.Thread(target=run_algorithm).start()

# Function to reset the canvas and dropdowns
def reset():
    for line, city1, city2 in lines:
        canvas.itemconfig(line, fill="blue", width=1)
    for city, rect in node_objects.items():
        canvas.itemconfig(rect, fill="white")
        dropdown_vars[city].set(" ")
    result_text_widget.delete(1.0, tk.END)
def back_to_menu():
    root.destroy()

# Frame for buttons
frame = tk.Frame(root)
frame.pack(pady=10)

# Button to find and display the path
find_button = tk.Button(frame, text="Find Path", command=find_path)
find_button.pack(side=tk.LEFT, padx=10)

# Button to reset
reset_button = tk.Button(frame, text="Reset", command=reset)
reset_button.pack(side=tk.LEFT, padx=10)

back_button = tk.Button(frame, text="Back to Menu", command=lambda: back_to_menu())
back_button.pack(side=tk.LEFT, padx=10)

# Create a scrollable text widget for displaying the result
result_text_widget = ScrolledText(root, width=80, height=10, wrap=tk.WORD, bg="white")
result_text_widget.pack(pady=10)


# Start the Tkinter event loop
root.mainloop()