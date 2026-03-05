from src.entities import Node


def infer_action(
    previous_position: tuple[int, int], current_position: tuple[int, int]
) -> str:
    dx = current_position[0] - previous_position[0]
    dy = current_position[1] - previous_position[1]

    if dx == 1:
        return "➡️"
    if dx == -1:
        return "⬅️"
    if dy == 1:
        return "⬇️"
    if dy == -1:
        return "⬆️"
    return ""


def build_path(final_node: Node) -> str:
    if final_node is None:
        return "No solution", 0.0, 0

    vertexes = []
    curr_node = final_node

    while curr_node.parent is not None:
        vertexes.append(
            infer_action(
                curr_node.parent.state.agent_position, curr_node.state.agent_position
            )
        )
        curr_node = curr_node.parent

    vertexes.reverse()

    return "".join(vertexes)
