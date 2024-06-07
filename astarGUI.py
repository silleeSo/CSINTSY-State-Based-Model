import tkinter as tk
import heapq
import time
import threading

def aStarSearch(graph, start, goal, heuristic_values, visualize_step):
    open_nodes = []
    heapq.heappush(open_nodes, (0, start))
    
    # Keep records of visited nodes
    actual_costs = {start: 0}
    function_values = {start: heuristic_values.get(start, 0)}
    parent_records = {}
    visited_nodes = set()
    
    while open_nodes:
        current = heapq.heappop(open_nodes)[1]  # Get the node with the lowest function value in open_nodes
        if current in visited_nodes:
            continue
        visited_nodes.add(current)

        if current == goal:
            path = []
            while current in parent_records:
                path.append(current)
                current = parent_records[current]
            path.append(start)
            path.reverse()  # Since you started from the goal and backtracked, you have to reverse the path generated
            return path, actual_costs[goal]

        # Visualize the current node being explored
        visualize_step(current, visited=True)

        # For each neighboring node in the newly explored node, calculate the function value 
        for neighbor_node, cost in graph[current].items():
            accumulative_cost = actual_costs[current] + cost  # Calculate accumulative cost in path traversed so far + the path to the current neighbor node

            # If neighbor node function value has not yet been calculated OR this newly calculated function value cost for that node is smaller than what is recorded
            if neighbor_node not in actual_costs or accumulative_cost < actual_costs[neighbor_node]:  
                if neighbor_node not in visited_nodes:
                    # Overwrite/create records about this neighbor node
                    parent_records[neighbor_node] = current  # Record current node as a parent of this neighbor
                    actual_costs[neighbor_node] = accumulative_cost  # Record actual path cost towards this neighbor
                    function_values[neighbor_node] = accumulative_cost + heuristic_values.get(neighbor_node, 0)  # Record the function value of this neighbor node
                    heapq.heappush(open_nodes, (function_values[neighbor_node], neighbor_node))  # Add this neighbor to open nodes

                    # Visualize the path being considered
                    visualize_step(current, neighbor_node)

        time.sleep(0.5)  # Add delay to visualize each step

    return None, float('inf')  # Return None and infinity if there is no path

# Create the main window
root = tk.Tk()
root.title("AStar | City Graph")

# Create a canvas widget
canvas = tk.Canvas(root, width=800, height=500, bg="white")
canvas.pack(side=tk.LEFT)

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

# Define the heuristic values
heuristics = {
    'Miami': 2000,
    'New York': 800,
    'Boston': 900,
    'Dallas': 1200,
    'San Francisco': 2200,
    'Los Angeles': 2400,
    'Chicago': 0  # Add heuristic for Chicago or default to 0
}

# Draw the connections (edges) and distances
graph = {city: {} for city in coordinates}
connections = [
    ("Dallas", "Los Angeles", 1700),
    ("Los Angeles", "San Francisco", 500),
    ("San Francisco", "Chicago", 2200),
    ("Chicago", "New York", 800),
    ("New York", "Boston", 250),
    ("New York", "Miami", 1000),
    ("New York", "Dallas", 1500),
    ("New York", "Los Angeles", 3000),
    ("Dallas", "Miami", 1200),
]

lines = []
line_objects = {}
for city1, city2, distance in connections:
    x1, y1 = coordinates[city1]
    x2, y2 = coordinates[city2]
    line = canvas.create_line(x1, y1, x2, y2, fill="blue")
    lines.append((line, city1, city2))
    line_objects[(city1, city2)] = line
    line_objects[(city2, city1)] = line
    graph[city1][city2] = distance
    graph[city2][city1] = distance
    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2

    # Create a background rectangle for the distance label
    bbox = canvas.create_text(mid_x, mid_y - 10, text=str(distance), fill="black")
    x0, y0, x1, y1 = canvas.bbox(bbox)
    canvas.create_rectangle(x0-2, y0-2, x1+2, y1+2, fill="pink", outline="")
    canvas.lift(bbox)  # Ensure the text is above the rectangle

# Draw the cities (nodes) with a background to hide overlapping lines
node_objects = {}
dropdown_vars = {}
for city, (x, y) in coordinates.items():
    # Draw a white rectangle behind the city label to hide the lines
    rect = canvas.create_rectangle(x-50, y-30, x+50, y+30, fill="white", outline="white")
    node_objects[city] = rect
    canvas.create_rectangle(x-48, y-28, x+48, y+28, outline="black", fill="white")
    canvas.create_text(x, y-10, text=city, fill="black")

    # Create dropdown inside each city box
    var = tk.StringVar(root)
    var.set(" ")  # Default value
    dropdown_vars[city] = var
    dropdown = tk.OptionMenu(canvas, var, " ", "Start", "End")
    dropdown.config(width=5, height=1, font=('Helvetica', 8))
    canvas.create_window(x, y + 12, window=dropdown)

# Function to visualize each step of the algorithm
def visualize_step(current, neighbor=None, visited=False):
    if visited:
        canvas.itemconfig(node_objects[current], fill="lightgreen")
    if neighbor:
        canvas.itemconfig(line_objects[(current, neighbor)], fill="yellow")
    root.update_idletasks()

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
        
        # Run the algorithm in a separate thread to keep the GUI responsive
        def run_algorithm():
            path, total_cost = aStarSearch(graph, start_city, end_city, heuristics, visualize_step)
            
            # Measure time after executing the algorithm
            end_time = time.time()
            
            path_str = " -> ".join(path)
            result_text = f"Path: {path_str}\nTotal Cost: {total_cost}\nTime: {end_time - start_time} seconds\n"
            result_label.config(text=result_text)

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
    result_label.config(text="")
# Frame for the distance table
frame = tk.Frame(root)
frame.pack(side=tk.RIGHT, padx=20, pady=20)

# Label for the distance table heading
heading_label = tk.Label(frame, text="Direct Distance from Chicago", font=('Helvetica', 14, 'bold'))
heading_label.pack()

# Label for the distance table content
label_text = """
Miami                        2000
New York                    800
Boston                       900
Dallas                      1200
San Francisco         2200
Los Angeles             2400
"""
distance_label = tk.Label(frame, text=label_text, justify=tk.LEFT, font=('Helvetica', 12))
distance_label.pack()

# Label to display the result
result_label = tk.Label(frame, text="", justify=tk.LEFT, font=('Helvetica', 12), bg="white")
result_label.pack(pady=30, padx=50)

# Button to find the path
find_button = tk.Button(frame, text="Find Path", command=find_path)
find_button.pack(side=tk.LEFT, padx=10)

# Button to reset
reset_button = tk.Button(frame, text="Reset", command=reset)
reset_button.pack(side=tk.LEFT, padx=10)

# Start the Tkinter event loop
root.mainloop()
