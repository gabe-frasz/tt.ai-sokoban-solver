import heapq

from src.entities import Node


def dijkstra(problem) -> (Node, int):
    initial_state = problem.initial_state
    initial_node = Node(state=initial_state)

    priority_queue = []
    heapq.heappush(priority_queue, initial_node)

    visited = {}

    while len(priority_queue) > 0:
        curr_node = heapq.heappop(priority_queue)

        if problem.is_goal(curr_node.state):
            return curr_node, len(visited)

        if curr_node.state in visited and visited[curr_node.state] <= curr_node.cost:
            continue

        visited[curr_node.state] = curr_node.cost

        successors = problem.generate_successors(curr_node.state)

        for new_state in successors:
            step_cost = problem.get_cost(curr_node.state)
            new_cost = curr_node.cost + step_cost

            if new_state in visited and visited[new_state] <= new_cost:
                continue

            new_node = Node(
                state=new_state,
                parent=curr_node,
                cost=new_cost,
            )

            heapq.heappush(priority_queue, new_node)

    return None, len(visited)


def greedy(problem) -> (Node, int):
    initial_state = problem.initial_state
    initial_node = Node(
        state=initial_state, heuristic=problem.get_heuristic(initial_state)
    )
    initial_node.total = initial_node.heuristic  # consider heuristic only

    priority_queue = []
    heapq.heappush(priority_queue, initial_node)

    visited = set()

    while len(priority_queue) > 0:
        curr_node = heapq.heappop(priority_queue)

        if problem.is_goal(curr_node.state):
            return curr_node, len(visited)

        if curr_node.state in visited:
            continue

        visited.add(curr_node.state)

        successors = problem.generate_successors(curr_node.state)

        for new_state in successors:
            if new_state in visited:
                continue

            step_cost = problem.get_cost(curr_node.state)
            new_cost = curr_node.cost + step_cost
            new_h = problem.get_heuristic(new_state)

            new_node = Node(
                state=new_state,
                parent=curr_node,
                cost=new_cost,
                heuristic=new_h,
            )
            new_node.total = new_h  # consider heuristic only

            heapq.heappush(priority_queue, new_node)

    return None, len(visited)


def a_star(problem) -> (Node, int):
    initial_state = problem.initial_state
    initial_node = Node(
        state=initial_state, heuristic=problem.get_heuristic(initial_state)
    )

    priority_queue = []
    heapq.heappush(priority_queue, initial_node)

    visited = {}

    while len(priority_queue) > 0:
        curr_node = heapq.heappop(priority_queue)

        if problem.is_goal(curr_node.state):
            return curr_node, len(visited)

        if curr_node.state in visited and visited[curr_node.state] <= curr_node.cost:
            continue

        visited[curr_node.state] = curr_node.cost

        successors = problem.generate_successors(curr_node.state)

        for new_state in successors:
            step_cost = problem.get_cost(curr_node.state)
            new_cost = curr_node.cost + step_cost

            if new_state in visited and visited[new_state] <= new_cost:
                continue

            new_node = Node(
                state=new_state,
                parent=curr_node,
                cost=new_cost,
                heuristic=problem.get_heuristic(new_state),
            )

            heapq.heappush(priority_queue, new_node)

    return None, len(visited)
