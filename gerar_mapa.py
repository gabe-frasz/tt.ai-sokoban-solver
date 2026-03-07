import argparse
import random

BOXES = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
WALL = "🧱"
TARGET = "🟢"
AGENT = "🙎"
FLOOR = "⚪️"


def generate_map(width: int, height: int, output_file: str):
    total_area = width * height

    # Max number of boxes set to 9 or 25% of the map area
    max_allowed_boxes = min(9, total_area * 0.25)
    boxes_quantity = random.randint(1, max(1, max_allowed_boxes))

    # Walls occupy at most 15% of the map area to avoid blocking the agent
    walls_quantity = int(total_area * 0.15)

    available_positions = [(x, y) for y in range(height) for x in range(width)]
    random.shuffle(available_positions)

    gridmap = {}

    agent_position = available_positions.pop()
    gridmap[agent_position] = AGENT

    for _ in range(boxes_quantity):
        gridmap[available_positions.pop()] = TARGET

    for i in range(boxes_quantity):
        box_position = available_positions.pop()
        gridmap[box_position] = BOXES[i]

    placed_walls = 0
    while placed_walls < walls_quantity and available_positions:
        wall_position = available_positions.pop()
        wx, wy = wall_position

        # Doesn't place walls on the borders of the map to try to leave a "corridor" open
        if 0 < wx < width - 1 and 0 < wy < height - 1:
            gridmap[wall_position] = WALL
            placed_walls += 1

    with open(output_file, "w", encoding="utf-8") as f:
        for y in range(height):
            line = []
            for x in range(width):
                # If there's something in the gridmap, get the emoji. Else, it's floor.
                symbol = gridmap.get((x, y), FLOOR)
                line.append(symbol)
            f.write(" ".join(line) + "\n")

    print(
        f"✅ Mapa {width}x{height} gerado com {boxes_quantity} caixas e {placed_walls} paredes em '{output_file}'"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cria mapas aleatórios de Sokoban")
    parser.add_argument(
        "--largura",
        type=int,
        default=0,
        help="Largura do gridmap (se omitido, será aleatório)",
    )
    parser.add_argument(
        "--altura",
        type=int,
        default=0,
        help="Altura do gridmap (se omitido, será aleatório)",
    )
    parser.add_argument(
        "--saida", type=str, default="entrada.txt", help="Nome do arquivo gerado"
    )

    args = parser.parse_args()

    # If user doesn't pass a valid value, choose between 4 and 48
    final_width = args.largura if args.largura >= 4 else random.randint(4, 48)
    final_height = args.altura if args.altura >= 4 else random.randint(4, 48)

    generate_map(final_width, final_height, args.saida)
