import sys

def main():
    light_x, light_y, thor_x, thor_y = map(int, input().split())

    # Boucle du jeu
    while True:
        remaining_turns = int(input())
        direction = ""

        # On détermine si la direction est verticale
        if thor_y > light_y:
            thor_y -= 1
            direction += "N"
        elif thor_y < light_y:
            thor_y += 1
            direction += "S"

        # On détermine si la direction est horizontale
        if thor_x > light_x:
            thor_x -= 1
            direction += "W"
        elif thor_x < light_x:
            thor_x += 1
            direction += "E"

        # On affiche la direction
        print(direction)


if __name__ == "__main__":
    main()
