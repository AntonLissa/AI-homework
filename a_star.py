import heapq

class Node:
    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other): # for priority queue by f value
        return self.f < other.f

def child_node(problem, parent_node, action, heuristic):
    new_state = problem.apply_action(parent_node.state, action)
    g = parent_node.g + 1
    h = heuristic(new_state)
    return Node(new_state, parent_node, g, h)

# allows modular use of A* with different problems and heuristics
def a_star(problem, heuristic, verbose=False, iteration_limit=500000):
    start_node = Node(problem.initial_state, g=0, h=heuristic(problem.initial_state))
    frontier = []
    heapq.heappush(frontier, start_node)
    explored = set()

    nodes_generated = 1  # starting node
    nodes_expanded = 0
    max_frontier_size = 1
    i = 0
    while frontier:
        if i >= iteration_limit:
            print(" - Iteration limit reached, stopping search.")
            return None, {
                    'nodes_generated': nodes_generated,
                    'nodes_expanded': nodes_expanded,
                    'max_frontier_size': max_frontier_size
                }

        i+=1
        node = heapq.heappop(frontier)
        nodes_expanded += 1

        if problem.is_goal(node.state):
            # metrics
            return reconstruct_path(node), {
                'nodes_generated': nodes_generated,
                'nodes_expanded': nodes_expanded,
                'max_frontier_size': max_frontier_size
            }

        explored.add(problem.state_to_hashable(node.state))

        # expand node by applying all possible actions
        actions = problem.get_actions(node.state)
        for action in actions:
            child = child_node(problem, node, action, heuristic)
            nodes_generated += 1
            child_hash = problem.state_to_hashable(child.state)

            in_frontier = False
            for f_node in frontier:
                if problem.state_to_hashable(f_node.state) == child_hash:
                    in_frontier = True
                    if child.g < f_node.g:
                        frontier.remove(f_node)
                        heapq.heappush(frontier, child)
                    break
            # add to frontier if not explored and not in frontier
            if child_hash not in explored and not in_frontier:
                heapq.heappush(frontier, child)

        max_frontier_size = max(max_frontier_size, len(frontier))

        if verbose:
            print(f"\n- Exploring node with g={node.g}, h={node.h}, f={node.f}")
            print(f"    - Frontier size: {len(frontier)}; Explored size: {len(explored)}")

    return None, {
        'nodes_generated': nodes_generated,
        'nodes_expanded': nodes_expanded,
        'max_frontier_size': max_frontier_size
    }

# this function reconstructs the path from start to goal
def reconstruct_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return path[::-1]

# Heuristic: count of empty cells
def heuristic(state):
    return sum(row.count(0) for row in state)
