import tkinter as tk
import heapq
import time
import threading
import tracemalloc


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

root = tk.Tk()
root.title("AStar | City Graph")

canvas = tk.Canvas(root, width=800, height=500, bg="white")
canvas.pack(side=tk.LEFT)

coordinates = {
    "Dallas": (200, 400),
    "Los Angeles": (100, 200),
    "San Francisco": (100, 100),
    "Chicago": (400, 50),
    "New York": (400, 200),
    "Boston": (600, 100),
    "Miami": (600, 300)
}

heuristics = {
    'Miami': 2000,
    'New York': 800,
    'Boston': 900,
    'Dallas': 1200,
    'San Francisco': 2200,
    'Los Angeles': 2400,
    'Chicago': 0
}

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

    bbox = canvas.create_text(mid_x, mid_y - 10, text=str(distance), fill="black")
    x0, y0, x1, y1 = canvas.bbox(bbox)
    canvas.create_rectangle(x0-2, y0-2, x1+2, y1+2, fill="pink", outline="")
    canvas.lift(bbox)

node_objects = {}
dropdown_vars = {}
for city, (x, y) in coordinates.items():
    rect = canvas.create_rectangle(x-50, y-30, x+50, y+30, fill="white", outline="white")
    node_objects[city] = rect
    canvas.create_rectangle(x-48, y-28, x+48, y+28, outline="black", fill="white")
    canvas.create_text(x, y-10, text=city, fill="black")

    var = tk.StringVar(root)
    var.set(" ")
    dropdown_vars[city] = var
    dropdown = tk.OptionMenu(canvas, var, " ", "Start", "End")
    dropdown.config(width=5, height=1, font=('Helvetica', 8))
    canvas.create_window(x, y + 12, window=dropdown)

def visualize_step(current, neighbor=None, visited=False):
    if visited:
        canvas.itemconfig(node_objects[current], fill="lightgreen")
    if neighbor:
        canvas.itemconfig(line_objects[(current, neighbor)], fill="yellow")
    root.update_idletasks()

def find_path():
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
                graph, start_city, end_city, heuristics, visualize_step
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
                    f"Path: {path_str}\n"
                    f"Path Traversed: {traversed_path_str}\n\n"
                    f"Total Cost: {total_cost}\n\n"
                    f"Time: {end_time - start_time:.2f} seconds\n\n"
                    f"Nodes Expanded: {nodes_expanded}\n\n"
                    f"Max Frontier Size: {max_frontier_size}\n\n"    
                    f"Memory Usage: Current={current / 1024}KB, Peak={peak / 1024}KB\n\n"
                    f"Visit Count: {visit_count}\n"
                )
            result_label.config(text=result_text)

            if path:
                for line, city1, city2 in lines:
                    if (city1, city2) in zip(path, path[1:]) or (city2, city1) in zip(path, path[1:]):
                        canvas.itemconfig(line, fill="red", width=3)
                    else:
                        canvas.itemconfig(line, fill="blue", width=1)
        
        threading.Thread(target=run_algorithm).start()

def reset():
    for line, city1, city2 in lines:
        canvas.itemconfig(line, fill="blue", width=1)
    for city, rect in node_objects.items():
        canvas.itemconfig(rect, fill="white")
        dropdown_vars[city].set(" ")
    result_label.config(text="")

frame = tk.Frame(root)
frame.pack(side=tk.RIGHT, padx=20, pady=20)

heading_label = tk.Label(frame, text="Heuristic Values", font=('Helvetica', 14, 'bold'))
heading_label.pack()

label_text = """
Chicago                     0
Miami                        2000
New York                    800
Boston                       900
Dallas                      1200
San Francisco         2200
Los Angeles             2400
"""
distance_label = tk.Label(frame, text=label_text, justify=tk.LEFT, font=('Helvetica', 12))
distance_label.pack()

result_label = tk.Label(
    frame, 
    text="", 
    justify=tk.LEFT, 
    font=('Helvetica', 12), 
    bg="white", 
    wraplength=400,  # Set wraplength to ensure text wraps within the label
    anchor="nw"  # Align text to the top-left corner
)
result_label.pack(pady=30, padx=50, fill=tk.BOTH, expand=True) 

find_button = tk.Button(frame, text="Find Path", command=find_path)
find_button.pack(side=tk.LEFT, padx=10)

reset_button = tk.Button(frame, text="Reset", command=reset)
reset_button.pack(side=tk.LEFT, padx=10)

root.mainloop()
