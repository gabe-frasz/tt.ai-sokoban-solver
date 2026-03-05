import sys

from src.entities import Node, State
from src.utils import EMOJI_TO_WEIGHT


def load_map(filepath: str, min_width: int = 0) -> (State, set, int, int):
    with open(filepath, 'r', encoding="utf-8") as f:
        linhas = f.readlines()

    walls = set()
    boxes = set()
    targets = set()
    agent_position = (0, 0)
    
    max_height = len(linhas)
    max_width = 0

    for y, linha in enumerate(linhas):
        # Break line into an array of strings using the empty spaces
        tokens = linha.strip().split()
        
        actual_line_size = max(len(tokens), min_width)
        max_width = max(max_width, actual_line_size)

        for x in range(actual_line_size):
            # If X is smaller than the text read, get the symbol.
            # Else, fill artificially with free space.
            symbol = tokens[x] if x < len(tokens) else "⚪️"

            if symbol == "🧱":
                walls.add((x, y))
            elif symbol == "🟢":
                targets.add((x, y))
            elif symbol == "🙎":
                agent_position = (x, y)
            elif symbol in EMOJI_TO_WEIGHT:
                weight = EMOJI_TO_WEIGHT[symbol]
                boxes.add(((x, y), weight))
            # ⚪️ is ignored because if it's not on state, it's a free space

    initial_state = State(
        agent_position=agent_position,
        holding=None,
        boxes=frozenset(boxes),
        targets_positions=frozenset(targets),
        delivered_boxes=frozenset()
    )

    return initial_state, walls, max_width, max_height

def export_results(filepath: str, problem, final_node: Node, solution_path: str, visited_nodes: int):
    with open(filepath, 'w', encoding="utf-8") as f:
        f.write("Final state\n")

        # Redirect stdout to file
        stdout_original = sys.stdout
        sys.stdout = f
        
        if final_node is not None:
            problem.print(final_node.state)
        
        # Redirect stdout back to original
        sys.stdout = stdout_original

        f.write(f"Moves\n{solution_path}\n")
        f.write(f"Visited nodes\n{visited_nodes}\n")
