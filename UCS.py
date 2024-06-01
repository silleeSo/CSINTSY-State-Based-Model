import heapq

class UniformCostSearch:
    def __init__(self, graph):
        self.graph = graph

    def search(self, start, goal):
        # Priority queue to store nodes to be explored, starting with the initial node and cost of 0
        frontier = []
        heapq.heappush(frontier, (0, start))

        # Store the cost to reach each node
        cost_so_far = {start: 0}
        # Store the path taken to reach each node
        came_from = {start: None}

        # Store all visited nodes
        visited_order = []

        while frontier:
            # Pop the node with the lowest cost from the priority queue
            current_cost, current_node = heapq.heappop(frontier)
            # Record the current node as visited
            visited_order.append(current_node)

            # If the current node is the goal, return the visited order and the total cost
            if current_node == goal:
                return visited_order, current_cost

            # Explore neighbors of the current node
            for neighbor, cost in self.graph[current_node].items():
                # Calculate the new cost to reach the neighbor
                new_cost = current_cost + cost

                # If this path to the neighbor is cheaper, update cost and path
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(frontier, (new_cost, neighbor))
                    came_from[neighbor] = current_node

        # If the goal is not reachable, return the visited order and close the node by returning infinity
        return visited_order, float('inf')

    def update_graph(self, new_graph):
        # Update the graph
        self.graph = new_graph

<<<<<<< Updated upstream
# MCO1 Given Graph
if __name__ == "__main__":
    # Define the graph with the given distances
    graph = {
        'Dallas': {'Los Angeles': 1700, 'New York': 1500, 'Miami': 1200},
        'Chicago': {'San Francisco': 500, 'New York': 800},
        'San Francisco': {'Los Angeles': 500, 'Chicago': 2200},
        'Los Angeles': {'San Francisco': 500, 'New York': 3000, 'Dallas': 1700},
        'Boston': {'New York': 250},
        'Miami': {'Dallas': 1200, 'New York': 1000},
        'New York': {'Los Angeles': 3000, 'Dallas': 1500, 'Chicago': 800, 'Boston': 250, 'Miami': 1200}
    }

    # Create the instance of the UniformCostSearch class with the graph
    ucs = UniformCostSearch(graph)
    start = 'Dallas'
    goal = 'Chicago'

    # Perform the search from start to goal
    visited_order, cost = ucs.search(start, goal)

    # Print the path (visited nodes in order) and the total cost
    print(f"Path: {visited_order}")
    print(f"Total Cost: {cost}")
=======
>>>>>>> Stashed changes
