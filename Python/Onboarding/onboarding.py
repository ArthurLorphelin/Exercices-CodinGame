# Fonction qui lit et retourne les informations sur les ennemis et leur distance
def get_enemy_info():
    enemy_1 = input()
    distance_1 = int(input())
    enemy_2 = input()
    distance_2 = int(input())
    return enemy_1, distance_1, enemy_2, distance_2

# Fonction qui retourne le nom de l'ennemi le plus proche
def find_closest_enemy(enemy_1, distance_1, enemy_2, distance_2):
    return enemy_1 if distance_1 < distance_2 else enemy_2

# Boucle principale du jeu
def main():
    while True:
        enemy_1, distance_1, enemy_2, distance_2 = get_enemy_info()

        # On affiche la solution
        closest_enemy = find_closest_enemy(enemy_1, distance_1, enemy_2, distance_2)
        print(closest_enemy)


if __name__ == "__main__":
    main()