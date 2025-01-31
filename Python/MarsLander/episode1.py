import sys

def compute_power(v_speed):
    """Calcule la puissance des fusées en fonction de la vitesse verticale."""
    if v_speed < -30:
        return 4
    elif v_speed < -20:
        return 3
    elif v_speed < -10:
        return 2
    else:
        return 0

def main():
    # Lecture des points de la surface de Mars
    surface_n = int(input())  # Nombre de points formant la surface
    surface = []
    for _ in range(surface_n):
        land_x, land_y = map(int, input().split())
        surface.append((land_x, land_y))  # Stockage des coordonnées de la surface

    # Boucle du jeu
    while True:
        x, y, h_speed, v_speed, fuel, rotate, power = map(int, input().split())

        # Calcul de la puissance nécessaire pour ralentir la descente
        power_needed = compute_power(v_speed)

        # La solution est toujours un angle de 0 (pas de rotation nécessaire pour le niveau 1)
        solution = f"0 {power_needed}"

        # Affichage de la solution
        print(solution)

if __name__ == "__main__":
    main()
