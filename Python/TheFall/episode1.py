from typing import List, Tuple

# Constantes
TUNNEL_ROOM_TOP_ENTRY = {
    1: (0, 1, "TOP"), 3: (0, 1, "TOP"), 4: (-1, 0, "RIGHT"),
    5: (1, 0, "LEFT"), 7: (0, 1, "TOP"), 9: (0, 1, "TOP"),
    10: (-1, 0, "RIGHT"), 11: (1, 0, "LEFT")
    }
TUNNEL_ROOM_LEFT_ENTRY = {
    1: (0, 1, "TOP"), 2: (1, 0, "LEFT"), 5: (0, 1, "TOP"),
    6: (1, 0, "LEFT"), 8: (0, 1, "TOP"), 9: (0, 1, "TOP"),
    13: (0, 1, "TOP")
}
TUNNEL_ROOM_RIGHT_ENTRY = {
    1: (0, 1, "TOP"), 2: (-1, 0, "RIGHT"), 4: (0, 1, "TOP"),
    6: (-1, 0, "RIGHT"), 7: (0, 1, "TOP"), 8: (0, 1, "TOP"),
    12: (0, 1, "TOP")
}

# Fonction qui lit les entrées et initialise la grille
def read_input() -> List[List[str]]:
    _, height = map(int, input().split())
    grid = [input().split() for _ in range(height)]
    _ = int(input())
    return grid

# Fonction qui détermine la prochaine position en fonction du type de la salle et de l'entrée
def get_next_position(grid: List[List[str]], x: int, y: int, pos: str) -> Tuple[int, int, str]:
    room_type = int(grid[y][x])
    movement_dict = {"TOP": TUNNEL_ROOM_TOP_ENTRY,
                     "LEFT": TUNNEL_ROOM_LEFT_ENTRY,
                     "RIGHT": TUNNEL_ROOM_RIGHT_ENTRY
                     }.get(pos, None)

    if movement_dict and room_type in movement_dict:
        movement_x, movement_y, new_pos = movement_dict[room_type]
        return x + movement_x, y + movement_y, new_pos
    return None

def main():
    grid = read_input()

    while True:
        user_x, user_y, pos = input().split()
        user_x, user_y = int(user_x), int(user_y)

        next_position = get_next_position(grid, user_x, user_y, pos)
        if next_position:
            user_x, user_y, pos = next_position
            print(f"{user_x} {user_y}")
        else:
            break


if __name__ == "__main__":
    main()
