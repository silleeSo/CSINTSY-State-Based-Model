import heapq

def aStarSearch(graph, start, goal, heuristic_values):
    open_nodes = []
    heapq.heappush(open_nodes, (0, start))
    
    # Keep records of visited nodes
    actual_costs = {start: 0}
    function_values = {start: heuristic_values[start]}
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

        # For each neighboring node in the newly explored node, calculate the function value 
        for neighbor_node, cost in graph[current].items():
            accumulative_cost = actual_costs[current] + cost  # Calculate accumulative cost in path traversed so far + the path to the current neighbor node

            # If neighbor node function value has not yet been calculated OR this newly calculated function value cost for that node is smaller than what is recorded
            if neighbor_node not in actual_costs or accumulative_cost < actual_costs[neighbor_node]:  
                if neighbor_node not in visited_nodes:
                    # Overwrite/create records about this neighbor node
                    parent_records[neighbor_node] = current  # Record current node as a parent of this neighbor
                    actual_costs[neighbor_node] = accumulative_cost  # Record actual path cost towards this neighbor
                    function_values[neighbor_node] = accumulative_cost + heuristic_values[neighbor_node]  # Record the function value of this neighbor node
                    heapq.heappush(open_nodes, (function_values[neighbor_node], neighbor_node))  # Add this neighbor to open nodes

    return None, float('inf')  # Return None and infinity if there is no path