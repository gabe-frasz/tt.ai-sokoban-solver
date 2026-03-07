from dataclasses import dataclass, field


@dataclass(frozen=True)
class State:
    agent_position: tuple[int, int]  # (x, y)
    holding: int | None  # box weight or None
    boxes: frozenset[tuple[tuple[int, int], int]]  # ((x, y), weight)
    targets_positions: frozenset[tuple[int, int]]  # (x, y)

    # Same as boxes, but ignored by hash since it's just a printable helper
    delivered_boxes: frozenset[tuple[tuple[int, int], int]] = field(
        default_factory=frozenset, compare=False, hash=False
    )


class Node:
    def __init__(
        self,
        state: State,
        parent=None,
        vertex: str = "",
        cost: float = 0.0,
        heuristic: float = 0.0,
    ):
        self.state = state
        self.parent = parent
        self.vertex = vertex
        self.cost = cost
        self.heuristic = heuristic
        self.total = cost + heuristic

    def __lt__(self, other):
        if self.total == other.total:
            return self.heuristic < other.heuristic
        return self.total < other.total
