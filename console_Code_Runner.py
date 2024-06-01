from UCS import UniformCostSearch
from AStar import aStarSearch
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
    heuristics = {
    'Miami': 2000,
    'New York': 800,
    'Boston': 900,
    'Dallas': 1200,
    'San Francisco': 2200,
    'Los Angeles': 2400
    }
    ucs = UniformCostSearch(graph)
    start = 'Dallas'
    goal = 'New York'
    visited_order, cost = ucs.search(start, goal)
    print(f"-----Uniform Cost Search-----")
    print(f"Path: {visited_order}")
    print(f"Total Cost: {cost}")
    print(f"-----A* Search-----")
    path, cost = aStarSearch(graph, start, goal, heuristics)
    print(f"Total Cost: {cost}")
    print(f"Path: {path}")

 