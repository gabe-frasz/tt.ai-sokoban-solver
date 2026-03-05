import sys
import time

from src.algorithms import a_star, dijkstra, greedy
from src.io_parser import export_results, load_map
from src.problem import SokobanProblem
from src.utils import build_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <map_file.txt> [width]")
        sys.exit(1)

    input_file = sys.argv[1]
    map_width = int(sys.argv[2]) if len(sys.argv) > 2 else 0

    initial_state, walls, max_w, max_h = load_map(input_file, min_width=map_width)

    algorithms = {
        "Dijkstra": (dijkstra, "dijkstra.txt"),
        "Greedy": (greedy, "greedy.txt"),
        "A*": (a_star, "a_star.txt"),
    }

    for name, (search_func, output_file) in algorithms.items():
        problem = SokobanProblem(
            initial_state=initial_state, walls=walls, width=max_w, height=max_h
        )

        start = time.time()
        final_node, visited = search_func(problem)
        execution_time = time.time() - start

        export_results(
            output_file, problem, final_node, build_path(final_node), visited
        )

        print()
        print(f"***{name}***")

        if final_node is None:
            print("❌ Found no solution")
            continue

        print(f"✅ Finished in {execution_time:.4f} seconds")
        print(f"Total cost: {final_node.cost}")
        print()


if __name__ == "__main__":
    main()
