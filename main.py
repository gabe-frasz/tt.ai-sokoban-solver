import sys
import time

from src.algorithms import a_star, dijkstra, greedy
from src.io_parser import load_map
from src.problem import SokobanProblem
from src.utils import build_path


def main():
    if len(sys.argv) < 2:
        print("Correct usage: python main.py <map_file.txt> [width]")
        sys.exit(1)

    input_file = sys.argv[1]
    map_width = int(sys.argv[2]) if len(sys.argv) > 2 else 0

    initial_state, walls, max_w, max_h = load_map(input_file, min_width=map_width)

    algorithms = {
        "A*": (a_star, "a_star.txt"),
        "Greedy": (greedy, "greedy.txt"),
        "Dijkstra": (dijkstra, "dijkstra.txt"),
    }

    for name, (search_func, output_file) in algorithms.items():
        print(f"***{name}***")

        problem = SokobanProblem(
            initial_state=initial_state, walls=walls, width=max_w, height=max_h
        )

        start = time.time()
        final_node, visited = search_func(problem)
        execution_time = time.time() - start

        path = build_path(final_node)

        if final_node is None:
            print("❌ {name} found no solution")
            continue

        print(f"✅ {name} finished in {execution_time:.4f} seconds")
        # export_results(output_file, problem, build_path)

        print("Initial state:")
        problem.print(problem.initial_state)
        print(f"Resulting path: {path}")
        print("Final state:")
        problem.print(final_node.state)
        print(f"Total steps: {int(len(path) / 2)}")  # each unicode char equals 2 chars
        print(f"Total cost: {final_node.cost}")
        print(f"Visited nodes: {visited}")



if __name__ == "__main__":
    main()
