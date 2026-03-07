import argparse
import time

from src.algorithms import a_star, dijkstra, greedy
from src.io_parser import export_results, load_map
from src.problem import SokobanProblem
from src.utils import build_path


def main():
    parser = argparse.ArgumentParser(
        description="Solucionador de Sokoban com IA (A*, Dijkstra, Ganancioso)"
    )
    parser.add_argument("arquivo", type=str, help="Caminho para o arquivo do mapa (entrada.txt)")
    parser.add_argument(
        "--largura", type=int, default=0, help="Largura adicional do mapa (opcional)"
    )

    args = parser.parse_args()

    initial_state, walls, max_w, max_h = load_map(args.arquivo, min_width=args.largura)

    algorithms = {
        "Dijkstra": (dijkstra, "dijkstra.txt"),
        "Ganancioso": (greedy, "ganancioso.txt"),
        "A*": (a_star, "a_estrela.txt"),
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
        print(f"### {name} ###")

        if final_node is None:
            print("❌ Nenhuma solução encontrada")
        else:
            print(f"✅ Finalizado em {execution_time:.4f} segundos")
            print(f"Custo total: {final_node.cost}")

        print()


if __name__ == "__main__":
    main()
