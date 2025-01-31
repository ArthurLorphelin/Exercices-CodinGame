import sys

def main():
    # Boucle de jeu
    while True:
        mountain_max_h = 0
        mountain_max_h_index = 0

        for index in range(8):
            mountain_h = int(input())

            # On compare par rapport au max de la hauteur des précédentes montagnes
            if mountain_h > mountain_max_h:
                mountain_max_h = mountain_h
                mountain_max_h_index = index

        # On affiche le résultat
        print(mountain_max_h_index)


if __name__ == "__main__":
    main()
