from typing import List, Tuple
import sys


# Fonction qui calcule la puissance des fusées en fonction de la vitesse verticale
def compute_power(v_speed: float) -> int:
    if v_speed < -30:
        return 4
    elif v_speed < -20:
        return 3
    elif v_speed < -10:
        return 2
    else:
        return 0


# Fonction qui lit et stocke les points de la surface de Mars
def read_surface() -> List[Tuple[int, ...]]:
    surface_n = int(input())
    return [tuple(map(int, input().split())) for _ in range(surface_n)]


# Boucle principale du jeu
def control_lander():
    surface = read_surface()

    while True:
        _, _, _, v_speed, _, _, _ = map(int, input().split())
        power_needed = compute_power(v_speed)

        # On affiche la solution
        print(f"0 {power_needed}")


def main():
    control_lander()


if __name__ == "__main__":
    main()
