import tkinter as tk
from tkinter import Menu, simpledialog
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
        frontier = []
        heapq.heappush(frontier, (0, start))
        visit_count = {start: 1}
        max_frontier_size = 0
        cost_so_far = {start: 0}
        came_from = {start: None}
        visited_order = []

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            current_cost, current_node = heapq.heappop(frontier)
            visited_order.append(current_node)
            visualize_step(current_node, visited=True)

            if current_node == goal:
                path = []
                while current_node is not None:
                    path.append(current_node)
                    current_node = came_from[current_node]
                return visited_order, cost_so_far[goal], path[::-1], len(visited_order), max_frontier_size, visit_count

            for neighbor, cost in self.graph[current_node].items():
                new_cost = current_cost + cost

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(frontier, (new_cost, neighbor))
                    came_from[neighbor] = current_node
                    visit_count[neighbor] = visit_count.get(neighbor, 0) + 1

                    visualize_step(current_node, neighbor)

        return visited_order, float('inf'), [], len(visited_order), max_frontier_size, visit_count


def visualize_step(current, neighbor=None, visited=False):
    if visited:
        app.canvas.itemconfig(app.node_objects[current]['rect'], fill="lightgreen")
    if neighbor:
        app.canvas.itemconfig(app.line_objects[(current, neighbor)], fill="yellow")
    root.update_idletasks()
    time.sleep(0.5)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Uniform Cost Search")

        self.selected_tool = tk.StringVar(value="Select")
        self.menu_bar = Menu(root)
        root.config(menu=self.menu_bar)

        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Run", command=self.run_algorithm)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        self.toolbar = tk.Frame(root, bd=1, relief=tk.RAISED)
        self.create_toolbar_buttons()
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.coordinates = {}
        self.node_objects = {}
        self.dropdown_vars = {}

        self.graph = {}
        self.line_objects = {}
        self.distance_labels = {}

        self.selected_node = None
        self.node_offset_x = 0
        self.node_offset_y = 0

        self.result_text_widget = ScrolledText(root, width=80, height=10, wrap=tk.WORD, bg="white")
        self.result_text_widget.pack(pady=10)

        #self.initialize_map()

    def create_toolbar_buttons(self):
        button_texts = ["Select", "Add", "Connection", "Remove City"]
        for text in button_texts:
            button = tk.Radiobutton(
                self.toolbar, 
                text=text, 
                relief=tk.RAISED, 
                indicatoron=0, 
                variable=self.selected_tool, 
                value=text,
                command=self.tool_selected
            )
            button.pack(side=tk.LEFT, padx=2, pady=2)

    def tool_selected(self):
        selected = self.selected_tool.get()
        if selected == "Add":
            self.canvas.bind("<Button-1>", self.add_city)
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")
        elif selected == "Select":
            self.canvas.bind("<Button-1>", self.select_node)
            self.canvas.bind("<B1-Motion>", self.move_node)
            self.canvas.bind("<ButtonRelease-1>", self.deselect_node)
        elif selected == "Connection":
            self.canvas.bind("<Button-1>", self.connect_cities)
        elif selected == "Remove City":
            self.canvas.bind("<Button-1>", self.remove_city)
        else:
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")

    def add_city(self, event):
        city_name = simpledialog.askstring("City Name", "Enter city name:")
        if city_name:
            x_coord = event.x
            y_coord = event.y
            self.coordinates[city_name] = (x_coord, y_coord)
            self.draw_city(city_name, x_coord, y_coord)

    def draw_city(self, city, x, y):
        node_rect = self.canvas.create_rectangle(x-48, y-28, x+48, y+28, outline="black", fill="ivory")
        text_id = self.canvas.create_text(x, y-10, text=city, fill="black")
        var = tk.StringVar(self.root)
        var.set(" ")
        self.dropdown_vars[city] = var
        dropdown = tk.OptionMenu(self.canvas, var, " ", "Start", "End")
        dropdown.config(width=5, height=1, font=('Helvetica', 8))
        dropdown_id = self.canvas.create_window(x, y + 12, window=dropdown, tags=("dropdown_" + city,))
        self.node_objects[city] = {'rect': node_rect, 'text': text_id, 'dropdown': dropdown_id}

    def select_node(self, event):
        for city, objs in self.node_objects.items():
            rect = objs['rect']
            if self.canvas.bbox(rect)[0] <= event.x <= self.canvas.bbox(rect)[2] and self.canvas.bbox(rect)[1] <= event.y <= self.canvas.bbox(rect)[3]:
                self.selected_node = city
                self.node_offset_x = event.x - self.coordinates[city][0]
                self.node_offset_y = event.y - self.coordinates[city][1]
                break

    def move_node(self, event):
        if self.selected_node:
            x = event.x - self.node_offset_x
            y = event.y - self.node_offset_y
            self.coordinates[self.selected_node] = (x, y)
            self.canvas.coords(self.node_objects[self.selected_node]['rect'], x-48, y-28, x+48, y+28)
            self.canvas.coords(self.node_objects[self.selected_node]['text'], x, y-10)
            self.canvas.coords(self.node_objects[self.selected_node]['dropdown'], x, y + 12)
            self.update_connected_lines(self.selected_node)

    def update_connected_lines(self, city):
        if city in self.graph:
            for connected_city, line in self.line_objects.items():
                if city == connected_city[0]:
                    x1, y1 = self.coordinates[city]
                    x2, y2 = self.coordinates[connected_city[1]]
                    self.canvas.coords(line, x1, y1, x2, y2)
                    self.update_distance_label(city, connected_city[1])
                elif city == connected_city[1]:
                    x1, y1 = self.coordinates[connected_city[0]]
                    x2, y2 = self.coordinates[city]
                    self.canvas.coords(line, x1, y1, x2, y2)
                    self.update_distance_label(connected_city[0], city)

    def draw_connected_lines(self):
        for city1, connections in self.graph.items():
            for city2, distance in connections.items():
                x1, y1 = self.coordinates[city1]
                x2, y2 = self.coordinates[city2]
                line = self.canvas.create_line(x1, y1, x2, y2, fill="blue")
                self.line_objects[(city1, city2)] = line
                self.line_objects[(city2, city1)] = line
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                bbox = self.canvas.create_text(mid_x, mid_y - 10, text=str(distance), fill="black")
                x0, y0, x1, y1 = self.canvas.bbox(bbox)
                self.distance_labels[(city1, city2)] = bbox
                self.canvas.lift(bbox)

    def update_distance_label(self, city1, city2):
        if (city1, city2) in self.distance_labels:
            bbox = self.distance_labels[(city1, city2)]
            x1, y1 = self.coordinates[city1]
            x2, y2 = self.coordinates[city2]
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            self.canvas.coords(bbox, mid_x, mid_y - 10)
            self.canvas.lift(bbox)

    def deselect_node(self, event):
        self.selected_node = None

    def connect_cities(self, event):
        clicked_city = None
        for city, objs in self.node_objects.items():
            rect = objs['rect']
            if self.canvas.bbox(rect)[0] <= event.x <= self.canvas.bbox(rect)[2] and self.canvas.bbox(rect)[1] <= event.y <= self.canvas.bbox(rect)[3]:
                clicked_city = city
                break
        
        if clicked_city:
            connect_to_city = simpledialog.askstring("Connect Cities", f"Enter city to connect {clicked_city} to:")
            if connect_to_city and connect_to_city in self.coordinates and connect_to_city != clicked_city:
                distance = simpledialog.askfloat("Distance", f"Enter distance between {clicked_city} and {connect_to_city}:")
                if distance:
                    if clicked_city not in self.graph:
                        self.graph[clicked_city] = {}
                    self.graph[clicked_city][connect_to_city] = distance
                    if connect_to_city not in self.graph:
                        self.graph[connect_to_city] = {}
                    self.graph[connect_to_city][clicked_city] = distance
                    x1, y1 = self.coordinates[clicked_city]
                    x2, y2 = self.coordinates[connect_to_city]
                    line = self.canvas.create_line(x1, y1, x2, y2, fill="blue")
                    self.line_objects[(clicked_city, connect_to_city)] = line
                    self.line_objects[(connect_to_city, clicked_city)] = line
                    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                    bbox = self.canvas.create_text(mid_x, mid_y - 10, text=str(distance), fill="black")
                    x0, y0, x1, y1 = self.canvas.bbox(bbox)
                    self.distance_labels[(clicked_city, connect_to_city)] = bbox
                    self.canvas.lift(bbox)
                    self.canvas.tag_lower(line)

    def remove_city(self, event):
        clicked_city = None
        for city, objs in self.node_objects.items():
            rect = objs['rect']
            if self.canvas.bbox(rect)[0] <= event.x <= self.canvas.bbox(rect)[2] and self.canvas.bbox(rect)[1] <= event.y <= self.canvas.bbox(rect)[3]:
                clicked_city = city
                break
        
        if clicked_city:
            self.canvas.delete(self.node_objects[clicked_city]['rect'])
            self.canvas.delete(self.node_objects[clicked_city]['text'])
            self.canvas.delete(self.node_objects[clicked_city]['dropdown'])
            del self.node_objects[clicked_city]
            if clicked_city in self.graph:
                del self.graph[clicked_city]
            for city, connections in self.graph.items():
                if clicked_city in connections:
                    del self.graph[city][clicked_city]
            del self.coordinates[clicked_city]

            lines_to_remove = []
            for (city1, city2), line in self.line_objects.items():
                if city1 == clicked_city or city2 == clicked_city:
                    lines_to_remove.append((city1, city2))
                    self.canvas.delete(line)
                    if (city1, city2) in self.distance_labels:
                        self.canvas.delete(self.distance_labels[(city1, city2)])
                        del self.distance_labels[(city1, city2)]
            for line in lines_to_remove:
                del self.line_objects[line]

    def run_algorithm(self):
        start_city = None
        end_city = None

        for city, var in self.dropdown_vars.items():
            if var.get() == "Start":
                start_city = city
            elif var.get() == "End":
                end_city = city

        if start_city is not None and end_city is not None:
            start_time = time.time()
            tracemalloc.start()

            def run_algorithm_thread():
                ucs = UniformCostSearch(self.graph, self.canvas, self.coordinates)
                visited_order, total_cost, path, nodes_expanded, max_frontier_size, visit_count = ucs.search(start_city, end_city)
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

                self.result_text_widget.delete(1.0, tk.END)
                self.result_text_widget.insert(tk.END, result_text)

                for (city1, city2), line in self.line_objects.items():
                    if (city1, city2) in zip(path, path[1:]) or (city2, city1) in zip(path, path[1:]):
                        self.canvas.itemconfig(line, fill="red", width=3)
                    else:
                        self.canvas.itemconfig(line, fill="blue", width=1)

            threading.Thread(target=run_algorithm_thread).start()

    def reset(self):
        for (city1, city2), line in self.line_objects.items():
            self.canvas.itemconfig(line, fill="blue", width=1)
        for city, objs in self.node_objects.items():
            self.canvas.itemconfig(objs['rect'], fill="white")
            self.dropdown_vars[city].set(" ")
        self.result_text_widget.delete(1.0, tk.END)
'''''
    def initialize_map(self):
        coordinates = {
            "Dallas": (200, 400),
            "Los Angeles": (100, 200),
            "San Francisco": (100, 100),
            "Chicago": (400, 50),
            "New York": (400, 200),
            "Boston": (600, 100),
            "Miami": (600, 300)
        }

        graph = {
            "Dallas": {"Los Angeles": 1700, "Miami": 1200, "New York": 1500},
            "Los Angeles": {"San Francisco": 500, "Dallas": 1700, "New York": 3000},
            "San Francisco": {"Los Angeles": 500, "Chicago": 2200},
            "Chicago": {"San Francisco": 2200, "New York": 800},
            "New York": {"Chicago": 800, "Boston": 250, "Miami": 1000, "Dallas": 1500, "Los Angeles": 3000},
            "Boston": {"New York": 250},
            "Miami": {"New York": 1000, "Dallas": 1200}
        }

        self.coordinates = coordinates
        self.graph = graph

        for city, (x, y) in coordinates.items():
            self.draw_city(city, x, y)

       ## self.draw_connected_lines()
       # '''

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)

    frame = tk.Frame(root)
    frame.pack(pady=10)

    find_button = tk.Button(frame, text="Find Path", command=app.run_algorithm)
    find_button.pack(side=tk.LEFT, padx=10)

    reset_button = tk.Button(frame, text="Reset", command=app.reset)
    reset_button.pack(side=tk.LEFT, padx=10)

    root.mainloop()
