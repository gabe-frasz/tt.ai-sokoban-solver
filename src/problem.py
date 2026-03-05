from src.entities import State
from src.utils import WEIGHT_TO_EMOJI


class SokobanProblem:
    def __init__(self, initial_state: State, walls: set, width: int, height: int):
        self.initial_state = initial_state
        self.walls = walls
        self.width = width
        self.height = height

    def start(self) -> State:
        return self.initial_state

    def is_goal(self, state: State) -> bool:
        return len(state.boxes) == 0 and state.holding is None

    def generate_successors(self, state: State) -> list[State]:
        successors = []
        directions = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}

        curr_x, curr_y = state.agent_position

        for dx, dy in directions.values():
            new_x, new_y = curr_x + dx, curr_y + dy
            new_position = (new_x, new_y)

            is_out_of_bounds = (
                new_x < 0 or new_x >= self.width or new_y < 0 or new_y >= self.height
            )
            is_wall = new_position in self.walls

            if is_out_of_bounds or is_wall:
                continue

            new_holding = state.holding
            new_boxes = set(state.boxes)
            new_targets_positions = set(state.targets_positions)
            new_delivered_boxes = set(state.delivered_boxes)

            if new_holding is None:
                found_box = next((b for b in state.boxes if b[0] == new_position), None)
                if found_box:
                    new_holding = found_box[1]  # box weight
                    new_boxes.remove(found_box)
            else:
                if new_position in new_targets_positions:
                    new_delivered_boxes.add((new_position, new_holding))

                    new_holding = None
                    new_targets_positions.remove(new_position)

            successors.append(
                State(
                    agent_position=new_position,
                    holding=new_holding,
                    boxes=frozenset(new_boxes),
                    targets_positions=frozenset(new_targets_positions),
                    delivered_boxes=frozenset(new_delivered_boxes),
                )
            )

        return successors

    def get_cost(self, state: State) -> float:
        if state.holding is not None:
            return 1 + state.holding
        return 1

    def get_heuristic(self, state: State) -> float:
        h_total = 0.0
        agent_x, agent_y = state.agent_position

        # 1. Total box cost
        # For each box, find the closest target and multiply the distance by (1 + box weight)
        for (bx, by), weight in state.boxes:
            if state.targets_positions:
                min_target_distance = min(
                    abs(bx - tx) + abs(by - ty) for tx, ty in state.targets_positions
                )
                h_total += min_target_distance * (1 + weight)

        # 2. Agent cost
        if state.holding is None:
            # If agent is not holding a box, add the distance to the closest box
            if state.boxes:
                min_box_distance = min(
                    abs(bx - agent_x) + abs(by - agent_y) for (bx, by), _ in state.boxes
                )
                h_total += min_box_distance
        else:
            # If agent is holding a box, add the distance to the closest target multiplied by (1 + box weight)
            if state.targets_positions:
                min_target_distance = min(
                    abs(tx - agent_x) + abs(ty - agent_y)
                    for tx, ty in state.targets_positions
                )
                h_total += min_target_distance * (1 + state.holding)

        return h_total

    def print(self, state: State):
        boxes_map = {pos: weight for pos, weight in state.boxes}
        delivered_boxes_map = {pos: weight for pos, weight in state.delivered_boxes}

        for y in range(self.height):
            for x in range(self.width):
                pos = (x, y)

                if pos == state.agent_position:
                    if pos in delivered_boxes_map:
                        print(f"{WEIGHT_TO_EMOJI[delivered_boxes_map[pos]]}🙎", end="")
                    elif state.holding is not None:
                        print(f"{WEIGHT_TO_EMOJI[state.holding]}🙎", end="")
                    else:
                        print("🙎  ", end="")
                elif pos in boxes_map:
                    print(f"{WEIGHT_TO_EMOJI[boxes_map[pos]]}  ", end="")
                elif pos in delivered_boxes_map:
                    print(f"{WEIGHT_TO_EMOJI[delivered_boxes_map[pos]]}  ", end="")
                elif pos in state.targets_positions:
                    print("🟢  ", end="")
                elif pos in self.walls:
                    print("🧱  ", end="")
                else:
                    print("⚪️  ", end="")

            print()
