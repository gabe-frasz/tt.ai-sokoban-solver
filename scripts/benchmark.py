import os
import sys
import time

import matplotlib.pyplot as plt

# Helps python find the 'src' folder from the current folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gerar_mapa import generate_map
from src.algorithms import a_star, dijkstra, greedy
from src.io_parser import load_map
from src.problem import SokobanProblem

MAX_ATTEMPTS = 3


def rodar_benchmark():
    print("Iniciando bateria de testes...")

    map_sizes = [4, 8, 16, 24, 64]
    nodes_history = {"A*": [], "Greedy": [], "Dijkstra": []}
    algorithms = {"A*": a_star, "Greedy": greedy, "Dijkstra": dijkstra}

    for size in map_sizes:
        temp_file = f"temp_map_{size}x{size}.txt"

        failed, attempts = True, 0
        while failed and attempts <= MAX_ATTEMPTS:
            attempts += 1

            generate_map(width=size, height=size, output_file=temp_file)
            problem_config = load_map(temp_file)
            problem = SokobanProblem(
                initial_state=problem_config[0],
                walls=problem_config[1],
                width=size,
                height=size,
            )

            print(
                f"### Testando mapa {size}x{size}{f"(tentativa {attempts}/{MAX_ATTEMPTS})" if attempts > 1 else ""}..."
            )

            # Run A* to validate the map
            print("A* -> ⏳")
            start_time = time.time()
            final_node, visited = a_star(problem)

            if final_node is None:
                if attempts < MAX_ATTEMPTS:
                    print("⚠️ Mapa sem solução. Descartando e gerando novo...")
                else:
                    print(
                        f"❌ Desistindo do tamanho {size} após {MAX_ATTEMPTS} tentativas. Preenchendo com 0 visitados."
                    )

                    for name in nodes_history.keys():
                        nodes_history[name].append(0)
                continue

            end_time = time.time()
            print(f"A* -> ✅ in {end_time - start_time:.2f}s")
            failed = False
            nodes_history["A*"].append(visited)

            for name, search_func in algorithms.items():
                if name == "A*":
                    continue

                print(f"{name} -> ⏳")
                start_time = time.time()
                _, visited = search_func(problem)
                end_time = time.time()
                nodes_history[name].append(visited)
                print(f"{name} -> ✅ in {end_time - start_time:.2f}s")

        if os.path.exists(temp_file):
            os.remove(temp_file)


    # ==========================================
    # CHART GENERATION (GROUPED BARS)
    # ==========================================
    plt.figure(figsize=(10, 6))

    bar_width = 0.25
    x_pos = range(len(map_sizes))

    a_star_pos = [p - bar_width for p in x_pos]
    greedy_pos = [p + bar_width for p in x_pos]
    dijkstra_pos = [p + bar_width for p in x_pos]

    plt.bar(a_star_pos, nodes_history["A*"], width=bar_width, label="A*", color="#2ca02c")
    plt.bar(greedy_pos, nodes_history["Greedy"], width=bar_width, label="Greedy", color="#ff7f0e")
    plt.bar(dijkstra_pos, nodes_history["Dijkstra"], width=bar_width, label="Dijkstra", color="#d62728")

    # Show NxN labels on the X axis
    plt.xticks(x_pos, [f"{s}x{s}" for s in map_sizes])

    # Let Y axis logarithmic
    plt.yscale("log")

    plt.title("Comparação de Desempenho dos Algoritmos (Escala Logarítmica)", fontsize=14, fontweight="bold")
    plt.xlabel("Tamanho do Mapa (N x N)", fontsize=12)
    plt.ylabel("Quantidade de Nós Visitados (log)", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.legend(fontsize=12)

    img_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "generated",
        "benchmark_result.png",
    )
    plt.savefig(img_path)
    print(f"\n✅ Benchmark concluído! Gráfico salvo em: {img_path}")

    plt.show()


if __name__ == "__main__":
    rodar_benchmark()
