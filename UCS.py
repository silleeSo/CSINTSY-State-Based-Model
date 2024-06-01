import heapq

class UniformCostSearch:
    def __init__(self, graph):
        self.graph = graph

    def search(self, start, goal):
        frontier = []
        heapq.heappush(frontier, (0, start))
        cost_so_far = {start: 0}
        came_from = {start: None}
        visited_order = []

        while frontier:
            current_cost, current_node = heapq.heappop(frontier)
            visited_order.append(current_node)

            if current_node == goal:
                return visited_order, current_cost

            for neighbor, cost in self.graph[current_node].items():
                new_cost = current_cost + cost

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(frontier, (new_cost, neighbor))
                    came_from[neighbor] = current_node

        return visited_order, float('inf')

    def update_graph(self, new_graph):
        self.graph = new_graph

# Example usage
if __name__ == "__main__":
    graph = {
        'Dallas': {'Los Angeles': 1700, 'New York': 1500, 'Miami': 1200},
        'Chicago': {'San Francisco': 500, 'New York': 800},
        'San Francisco': {'Los Angeles': 500, 'Chicago': 2200},
        'Los Angeles': {'San Francisco': 500, 'New York': 3000, 'Dallas': 1700},
        'Boston': {'New York': 250},
        'Miami': {'Dallas': 1200, 'New York': 1000},
        'New York': {'Los Angeles': 3000, 'Dallas': 1500, 'Chicago': 800, 'Boston': 250, 'Miami': 1200}
    }

    ucs = UniformCostSearch(graph)
    start = 'Dallas'
    goal = 'New York'
    visited_order, cost = ucs.search(start, goal)
    print(f"Path: {visited_order}")
    print(f"Total Cost: {cost}")
