def main():
    # Boucle du jeu
    while True:
        enemy_1 = input()
        distance_1 = int(input())
        enemy_2 = input()
        distance_2 = int(input())

        # On affiche le nom de l'ennemi le plus proche
        print(enemy_1 if distance_1 < distance_2 else enemy_2)


if __name__ == "__main__":
    main()