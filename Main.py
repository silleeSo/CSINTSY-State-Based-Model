import tkinter as tk
from tkinter import messagebox
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
            visualize_step_ucs(current_node, visited=True)

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
                    visualize_step_ucs(current_node, neighbor)

        # If the goal is not reachable, return the visited order, infinity as cost, and an empty path
        return visited_order, float('inf'), [], len(visited_order), max_frontier_size, visit_count


# Function to visualize each step of the algorithm
def visualize_step_ucs(current, neighbor=None, visited=False):
    if visited:
        canvas_uc.itemconfig(node_objects[current], fill="lightgreen")
    if neighbor:
        canvas_uc.itemconfig(line_objects[(current, neighbor)], fill="yellow")
    root.update_idletasks()
    time.sleep(0.5)



def aStarSearch(graph, start, goal, heuristic_values, visualize_step):
    open_nodes = []
    heapq.heappush(open_nodes, (0, start))

    actual_costs = {start: 0}
    function_values = {start: heuristic_values.get(start, 0)}
    parent_records = {}
    visited_nodes = set()

    traversed_path = []
    nodes_expanded = 0
    max_frontier_size = 0
    visit_count = {start: 1}

    while open_nodes:
        max_frontier_size = max(max_frontier_size, len(open_nodes))
        current = heapq.heappop(open_nodes)[1]

        if current in visited_nodes:
            continue

        visited_nodes.add(current)
        traversed_path.append(current)
        nodes_expanded += 1

        if current == goal:
            path = []
            while current in parent_records:
                path.append(current)
                current = parent_records[current]
            path.append(start)
            path.reverse()
            total_cost = actual_costs[goal]
            return path, traversed_path, total_cost, nodes_expanded, max_frontier_size, visit_count

        visualize_step(current, visited=True)

        for neighbor_node, cost in graph[current].items():
            accumulative_cost = actual_costs[current] + cost

            if neighbor_node not in actual_costs or accumulative_cost < actual_costs[neighbor_node]:
                if neighbor_node not in visited_nodes:
                    parent_records[neighbor_node] = current
                    actual_costs[neighbor_node] = accumulative_cost
                    function_values[neighbor_node] = accumulative_cost + heuristic_values.get(neighbor_node, 0)
                    heapq.heappush(open_nodes, (function_values[neighbor_node], neighbor_node))

                    visit_count[neighbor_node] = visit_count.get(neighbor_node, 0) + 1
                    
                    visualize_step(current, neighbor_node)

        time.sleep(0.5)

    return None, traversed_path, float('inf'), nodes_expanded, max_frontier_size, visit_count

def visualize_step(current, neighbor=None, visited=False):
    if visited:
        canvas_astar.itemconfig(node_objects[current], fill="lightgreen")
    if neighbor:
        canvas_astar.itemconfig(line_objects[(current, neighbor)], fill="yellow")
    root.update_idletasks()
    time.sleep(0.5)    
    
    
# Create the main window
root = tk.Tk()
root.title("MCO1 - State Based Model - CSINTSY - S13 - GRP3")

# Create a menu frame
menu_frame = tk.Frame(root)
menu_frame.pack(pady=10)

# Create a welcome message
welcome_label = tk.Label(menu_frame, text="Choose a Search Algorithm", font=("Helvetica", 16))
welcome_label.pack(pady=10)
welcome_label.pack(padx=10)

# Create buttons for AStar Search and Uniform Cost Search
def astar_search_gui():
    menu_frame.pack_forget()
    a_star_search_frame.pack(pady=10)
    root.title("AStar Search")

def uniform_cost_search_gui():
    menu_frame.pack_forget()
    uniform_cost_search_frame.pack(pady=10)
    root.title("Uniform Cost Search")
    

astar_button = tk.Button(menu_frame, text="AStar Search", command=astar_search_gui, width=20, height=2)
astar_button.pack(pady=10)
uniform_cost_button = tk.Button(menu_frame, text="Uniform Cost Search", command=uniform_cost_search_gui, width=20, height=2)
uniform_cost_button.pack(pady=10)

# Create a frame for Uniform Cost Search visualization
uniform_cost_search_frame = tk.Frame(root)
# Add a label on top of the graph
graph_label_uc = tk.Label(uniform_cost_search_frame, text="Uniform Cost Search", font=("Helvetica", 14))
graph_label_uc.pack(pady=10)

canvas_uc = tk.Canvas(uniform_cost_search_frame, width=800, height=600, bg="white")
canvas_uc.pack()

coordinates_uc = {
    "Dallas": (200, 400),
    "Los Angeles": (100, 200),
    "San Francisco": (100, 100),
    "Chicago": (400, 50),
    "New York": (400, 200),
    "Boston": (600, 100),
    "Miami": (600, 300)
}

graph_uc = {
    "Dallas": {"Los Angeles": 1700, "Miami": 1200, "New York": 1500},
    "Los Angeles": {"San Francisco": 500, "Dallas": 1700, "New York": 3000},
    "San Francisco": {"Los Angeles": 500, "Chicago": 2200},
    "Chicago": {"San Francisco": 2200, "New York": 800},
    "New York": {"Chicago": 800, "Boston": 250, "Miami": 1000, "Dallas": 1500, "Los Angeles": 3000},
    "Boston": {"New York": 250},
    "Miami": {"New York": 1000, "Dallas": 1200}
}

ucs = UniformCostSearch(graph_uc, canvas_uc, coordinates_uc)

line_objects_uc = {}
lines_uc = []
for city1, connections in graph_uc.items():
    for city2, distance in connections.items():
        x1, y1 = coordinates_uc[city1]
        x2, y2 = coordinates_uc[city2]
        line = canvas_uc.create_line(x1, y1, x2, y2, fill="blue")
        line_objects_uc[(city1, city2)] = line
        line_objects_uc[(city2, city1)] = line
        lines_uc.append((line, city1, city2))
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        bbox = canvas_uc.create_text(mid_x, mid_y - 10, text=str(distance), fill="black")
        x0, y0, x1, y1 = canvas_uc.bbox(bbox)
        canvas_uc.create_rectangle(x0-2, y0-2, x1+2, y1+2, fill="pink", outline="")
        canvas_uc.lift(bbox)

dropdown_vars_uc = {}
node_objects_uc = {}
for city, (x, y) in coordinates_uc.items():
    canvas_uc.create_rectangle(x-50, y-30, x+50, y+30, fill="white", outline="white")
    node_rect = canvas_uc.create_rectangle(x-48, y-28, x+48, y+28, outline="black", fill="white")
    node_objects_uc[city] = node_rect
    canvas_uc.create_text(x, y-10, text=city, fill="black")

    var = tk.StringVar(root)
    var.set(" ")
    dropdown_vars_uc[city] = var
    dropdown = tk.OptionMenu(canvas_uc, var, " ", "Start", "End")
    dropdown.config(width=5, height=1, font=('Helvetica', 8))
    canvas_uc.create_window(x, y + 12, window=dropdown)

def ucs_find_path():
    start_city = None
    end_city = None
    
    for city, var in dropdown_vars_uc.items():
        if var.get() == "Start":
            start_city = city
        elif var.get() == "End":
            end_city = city
    
    if start_city is not None and end_city is not None:
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
                f"Traversed Path: {visited_str}\n\n"
                f"Total Cost: {total_cost}\n\n"
                f"Time: {end_time - start_time} seconds\n\n"
                f"Nodes Expanded: {nodes_expanded}\n\n"
                f"Max Frontier Size: {max_frontier_size}\n\n"
                f"Memory Usage: Current={current / 1024}KB, Peak={peak / 1024}KB\n\n"
                f"Visit Count: {visit_count}"
            )

            result_text_widget.delete(1.0, tk.END)
            result_text_widget.insert(tk.END, result_text)

             # Highlight the final best path
            for line, city1, city2 in lines:
                if (city1, city2) in zip(path, path[1:]) or (city2, city1) in zip(path, path[1:]):
                    canvas_uc.itemconfig(line, fill="red", width=3)
                else:
                    canvas_uc.itemconfig(line, fill="blue", width=1)
        
        threading.Thread(target=run_algorithm).start()


def reset_uc():
    for line, city1, city2 in lines:
        canvas_uc.itemconfig(line, fill="blue", width=1)
    for city, rect in node_objects.items():
        canvas_uc.itemconfig(rect, fill="white")
        dropdown_vars[city].set(" ")
    result_text_widget.delete(1.0, tk.END)

frame = tk.Frame(uniform_cost_search_frame)
frame.pack(pady=10)

find_button = tk.Button(frame, text="Find Path", command=ucs_find_path)
find_button.pack(side=tk.LEFT, padx=10)

reset_button = tk.Button(frame, text="Reset", command=reset_uc)
reset_button.pack(side=tk.LEFT, padx=10)

back_button = tk.Button(frame, text="Back to Menu", command=lambda: back_to_menu())
back_button.pack(side=tk.LEFT, padx=10)

result_text_widget = ScrolledText(uniform_cost_search_frame, width=80, height=10, wrap=tk.WORD, bg="white")
result_text_widget.pack(pady=10)

def back_to_menu():
    uniform_cost_search_frame.pack_forget()
    a_star_search_frame.pack_forget()
    root.title("MCO1 - State Based Model - CSINTSY - S13 - GRP3")
    menu_frame.pack(pady=10)


# Create a frame for AStar Search visualization
a_star_search_frame = tk.Frame(root)
# Add a label on top of the graph
graph_label_astar = tk.Label(a_star_search_frame, text="AStar Search", font=("Helvetica", 14))
graph_label_astar.pack(pady=10)

canvas_astar = tk.Canvas(a_star_search_frame, width=800, height=600, bg="white")
canvas_astar.pack(side=tk.LEFT)


coordinates_astar = {
    "Dallas": (200, 400),
    "Los Angeles": (100, 200),
    "San Francisco": (100, 100),
    "Chicago": (400, 50),
    "New York": (400, 200),
    "Boston": (600, 100),
    "Miami": (600, 300)
}

heuristics_astar = {
    'Miami': 2000,
    'New York': 800,
    'Boston': 900,
    'Dallas': 1200,
    'San Francisco': 2200,
    'Los Angeles': 2400,
    'Chicago': 0
}

graph = {city: {} for city in coordinates_astar}
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
    x1, y1 = coordinates_astar[city1]
    x2, y2 = coordinates_astar[city2]
    line = canvas_astar.create_line(x1, y1, x2, y2, fill="blue")
    lines.append((line, city1, city2))
    line_objects[(city1, city2)] = line
    line_objects[(city2, city1)] = line
    graph[city1][city2] = distance
    graph[city2][city1] = distance
    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2

    bbox = canvas_astar.create_text(mid_x, mid_y - 10, text=str(distance), fill="black")
    x0, y0, x1, y1 = canvas_astar.bbox(bbox)
    canvas_astar.create_rectangle(x0-2, y0-2, x1+2, y1+2, fill="pink", outline="")
    canvas_astar.lift(bbox)

node_objects = {}
dropdown_vars = {}
for city, (x, y) in coordinates_astar.items():
    rect = canvas_astar.create_rectangle(x-50, y-30, x+50, y+30, fill="white", outline="white")
    node_objects[city] = rect
    canvas_astar.create_rectangle(x-48, y-28, x+48, y+28, outline="black", fill="white")
    canvas_astar.create_text(x, y-10, text=city, fill="black")

    var = tk.StringVar(root)
    var.set(" ")
    dropdown_vars[city] = var
    dropdown = tk.OptionMenu(canvas_astar, var, " ", "Start", "End")
    dropdown.config(width=5, height=1, font=('Helvetica', 8))
    canvas_astar.create_window(x, y + 12, window=dropdown)

def visualize_step(current, neighbor=None, visited=False):
    if visited:
        canvas_astar.itemconfig(node_objects[current], fill="lightgreen")
    if neighbor:
        canvas_astar.itemconfig(line_objects[(current, neighbor)], fill="yellow")
    root.update_idletasks()

def find_path_astar():
    start_city = None
    end_city = None
    
    for city, var in dropdown_vars.items():
        if var.get() == "Start":
            start_city = city
        elif var.get() == "End":
            end_city = city
    
    if start_city is not None and end_city is not None:
    
        start_time = time.time()
        tracemalloc.start()

        def run_algorithm():
            
            path, traversed_path, total_cost, nodes_expanded, max_frontier_size, visit_count = aStarSearch(
                graph, start_city, end_city, heuristics_astar, visualize_step
            )

            end_time = time.time()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            if path is None:
                result_text = "No path found.\n"
            else:
                path_str = " -> ".join(path)
                traversed_path_str = " -> ".join(traversed_path)
                result_text = (
                    f"Final Path: {path_str}\n\n"
                    f"Traversed Path: {traversed_path_str}\n\n"
                    f"Total Cost: {total_cost}\n\n"
                    f"Time: {end_time - start_time:.2f} seconds\n\n"
                    f"Nodes Expanded: {nodes_expanded}\n\n"
                    f"Max Frontier Size: {max_frontier_size}\n\n"    
                    f"Memory Usage: Current={current / 1024}KB, Peak={peak / 1024}KB\n\n"
                    f"Visit Count: {visit_count}\n"
                )
            result_text_widget.delete(1.0, tk.END)
            result_text_widget.insert(tk.END, result_text)

            if path:
                for line, city1, city2 in lines:
                    if (city1, city2) in zip(path, path[1:]) or (city2, city1) in zip(path, path[1:]):
                        canvas_astar.itemconfig(line, fill="red", width=3)
                    else:
                        canvas_astar.itemconfig(line, fill="blue", width=1)
        
        threading.Thread(target=run_algorithm).start()

def reset():
    for line, city1, city2 in lines:
        canvas_astar.itemconfig(line, fill="blue", width=1)
    for city, rect in node_objects.items():
        canvas_astar.itemconfig(rect, fill="white")
        dropdown_vars[city].set(" ")
    result_text_widget.delete(1.0, tk.END)

frame = tk.Frame(a_star_search_frame)
frame.pack(pady=10)

heading_label = tk.Label(frame, text="Heuristic Values", font=('Helvetica', 14, 'bold'))
heading_label.pack()

label_text = """
Chicago                     0
Miami                        2000
New York                  800
Boston                      900
Dallas                       1200
San Francisco         2200
Los Angeles            2400
"""
distance_label = tk.Label(frame, text=label_text, justify=tk.LEFT, font=('Helvetica', 12))
distance_label.pack()

find_button = tk.Button(frame, text="Find Path", command=find_path_astar)
find_button.pack(side=tk.LEFT, padx=10)

reset_button = tk.Button(frame, text="Reset", command=reset)
reset_button.pack(side=tk.LEFT, padx=10)

back_button = tk.Button(frame, text="Back to Menu", command=lambda: back_to_menu())
back_button.pack(side=tk.LEFT, padx=10)


result_text_widget = ScrolledText(a_star_search_frame, width=80, height=10, wrap=tk.WORD, bg="white")
result_text_widget.pack(pady=10)

# Initially only show the menu frame
menu_frame.pack()
uniform_cost_search_frame.pack_forget()
a_star_search_frame.pack_forget()

root.mainloop()