from typing import Tuple

# Fonction qui lit et retourne les positions initiales de l'éclair et de Thor
def get_initial_positions() -> Tuple[int, int, int, int]:
    light_x, light_y, thor_x, thor_y = map(int, input().split())
    return light_x, light_y, thor_x, thor_y

# Fonction qui détermine le mouvement de Thor vers l'éclair et retourne la direction
def move_thor(thor_x: int, thor_y: int, light_x: int, light_y: int) -> Tuple[int, int, str]:
    direction = ""

    # Déplacement vertical
    if thor_y > light_y:
        thor_y -= 1
        direction += "N"
    elif thor_y < light_y:
        thor_y += 1
        direction += "S"

    # Déplacement horizontal
    if thor_x > light_x:
        thor_x -= 1
        direction += "W"
    elif thor_x < light_x:
        thor_x += 1
        direction += "E"

    return thor_x, thor_y, direction

# Boucle principale du jeu
def main():
    light_x, light_y, thor_x, thor_y = get_initial_positions()

    while True:
        remaining_turns = int(input())
        thor_x, thor_y, direction = move_thor(thor_x, thor_y, light_x, light_y)

        # On affiche la solution
        print(direction)

if __name__ == "__main__":
    main()