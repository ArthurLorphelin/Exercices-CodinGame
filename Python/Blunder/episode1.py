import sys
import math


# Classe du robot Blunder
class Blunder:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.current_direction = "SOUTH"
        self.breaker_mode = False
        self.direction_order = ["SOUTH", "EAST", "NORTH", "WEST"]
        self.deplacement_order = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.index_direction = 0


# Fonction qui lit les données et les retourne
def read_input():
    height, width = [int(i) for i in input().split()]
    grid = [list(input().strip()) for _ in range(height)]
    return height, width, grid


# Fonction qui cherche le point initial
def find_initial_coordonates(height, width, grid):
    for y in range(height):
        for x in range(width):
            if grid[y][x] == "@":
                return x, y
    return -1, -1


# Fonction qui cherche la sortie et retourne ses coordonnées
def find_exit_coordonates(height, width, grid):
    for y in range(height):
        for x in range(width):
            if grid[y][x] == "$":
                return x, y
    return -1, -1


# Fonction qui cherche et stocke dans une liste les deux téléporteurs
def find_teleporters(height, width, grid):
    teleporters = []
    for y in range(height):
        for x in range(width):
            if grid[y][x] == "T":
                teleporters.append((x, y))
    return teleporters


# Fonction qui regarde si le Blunder est à l'arrivée
def is_Blunder_at_exit(blunder, exit_x, exit_y):
    return True if (blunder.x == exit_x and blunder.y == exit_y) else False


# Fonction qui retourne les prochains incréments pour x et y du Blunder
def get_next_Blunder_coordonates(blunder):
    return blunder.deplacement_order[blunder.index_direction]


# Fonction qui regarde si la prochaine case est un obstacle
def is_next_tile_an_obstacle(grid, blunder):
    next_x, next_y = get_next_Blunder_coordonates(blunder)
    if not blunder.breaker_mode:
        return True if (grid[blunder.y + next_y][blunder.x + next_x] == "#" or grid[blunder.y + next_y][
            blunder.x + next_x] == "X") else False
    else:
        return True if grid[blunder.y + next_y][blunder.x + next_x] == "#" else False


# Fonction qui modifie les paramètres de Blunder si la prochaine case est un obstacle ou non
def modify_properties_for_next_tile(grid, blunder):
    if is_next_tile_an_obstacle(grid, blunder):
        blunder.index_direction = 0
        while is_next_tile_an_obstacle(grid, blunder):
            blunder.index_direction += 1
        blunder.current_direction = blunder.direction_order[blunder.index_direction]
    blunder.x += get_next_Blunder_coordonates(blunder)[0]
    blunder.y += get_next_Blunder_coordonates(blunder)[1]


# Fonction qui vérifie si la case actuelle est un modificateur de trajectoire
def is_current_tile_a_direction_modifier(grid, blunder):
    return True if (grid[blunder.y][blunder.x] == "S" or grid[blunder.y][blunder.x] == "E" or grid[blunder.y][
        blunder.x] == "N" or grid[blunder.y][blunder.x] == "W") else False


# Fonction qui applique les modifications de propriétés d'un modificateur de trajectoire
def modify_properties_if_Blunder_on_a_modifier(grid, blunder):
    for index in range(len(blunder.direction_order)):
        if blunder.direction_order[index][0] == grid[blunder.y][blunder.x]:
            blunder.index_direction = index
            blunder.current_direction = blunder.direction_order[index]


# Fonction qui regarde si la case actuelle est un inverseur de circuits
def is_current_tile_a_circuit_inverter(grid, blunder):
    return True if grid[blunder.y][blunder.x] == "I" else False


# Fonction qui applique les modifications de propriétés d'un iverteur de circuits
def modify_properties_if_Blunder_on_an_inverter(blunder):
    blunder.direction_order = blunder.direction_order[::-1]
    blunder.deplacement_order = blunder.deplacement_order[::-1]
    blunder.index_direction = blunder.direction_order.index(blunder.current_direction)


# Fonction qui regarde si la case actuelle est une bière
def is_current_tile_a_bier(grid, blunder):
    return True if grid[blunder.y][blunder.x] == "B" else False


# Fonction qui applique les modifications de propriétés d'une bière
def modify_properties_if_Blunder_on_a_bier(blunder):
    blunder.breaker_mode = True if not blunder.breaker_mode else False


# Fonction qui regarde si la case actuelle est un obstacle X
def is_current_tile_an_X_obstacle_with_breaker_mode(grid, blunder):
    return True if (blunder.breaker_mode and grid[blunder.y][blunder.x] == "X") else False


# Fonction qui applique les modifications de la grille si on est sur un obstacle X en mode casseur
def modify_properties_if_Blunder_breaker_mode_on_obstacle_X(grid, blunder):
    grid[blunder.y][blunder.x] = " "
    return grid


# Fonction qui regarde si la case actuelle est un téléporteur
def is_current_tile_a_teleporter(grid, blunder):
    return True if grid[blunder.y][blunder.x] == "T" else False


# Fonction qui applique les modifications de propriétés d'un téléporteur
def modify_properties_if_Blunder_on_a_teleporter(grid, blunder, teleporters):
    for index in range(len(teleporters)):
        if teleporters[index][0] != blunder.x or teleporters[index][1] != blunder.y:
            blunder.x = teleporters[index][0]
            blunder.y = teleporters[index][1]
            break


# Fonction qui stocke la solution
def append_solution(solution, bundler):
    if len(solution) != 0:
        solution += "\n"
    solution += bundler.current_direction
    return solution


# Fonction qui regarde si on est dans le cas d'une boucle infini
def is_infinite_loop(blunders_path_list, blunder, grid_modifications):
    for blunder_info in blunders_path_list:
        if blunder.x == blunder_info[0] and blunder.y == blunder_info[1] and blunder.current_direction == blunder_info[
            2] and blunder.breaker_mode == blunder_info[3] and blunder.index_direction == blunder_info[
            4] and grid_modifications == blunder_info[5]:
            return True
    return False


# Boucle principale du jeu
def main():
    # On instancie toutes les variables dont on a besoin
    height, width, grid = read_input()
    blunder_x, blunder_y = find_initial_coordonates(height, width, grid)
    blunder = Blunder(blunder_x, blunder_y)
    exit_x, exit_y = find_exit_coordonates(height, width, grid)
    teleporters = find_teleporters(height, width, grid)
    blunders_path_list = []
    solution = ""
    grid_modifications = 0

    while not is_Blunder_at_exit(blunder, exit_x, exit_y):
        # On regarde sur quel type de case est le Blunder et on applique les propriétés voulues
        if is_current_tile_a_direction_modifier(grid, blunder):
            modify_properties_if_Blunder_on_a_modifier(grid, blunder)
        elif is_current_tile_a_circuit_inverter(grid, blunder):
            modify_properties_if_Blunder_on_an_inverter(blunder)
        elif is_current_tile_a_bier(grid, blunder):
            modify_properties_if_Blunder_on_a_bier(blunder)
        elif is_current_tile_an_X_obstacle_with_breaker_mode(grid, blunder):
            grid = modify_properties_if_Blunder_breaker_mode_on_obstacle_X(grid, blunder)
            grid_modifications += 1
        elif is_current_tile_a_teleporter(grid, blunder):
            modify_properties_if_Blunder_on_a_teleporter(grid, blunder, teleporters)

        # On regarde si on n'est pas dans une boucle infinie, sinon on ajoute le blunder au chemin
        if is_infinite_loop(blunders_path_list, blunder, grid_modifications):
            solution = "LOOP"
            break
        else:
            blunder_info = [blunder.x, blunder.y, blunder.current_direction, blunder.breaker_mode,
                            blunder.index_direction, grid_modifications]
            blunders_path_list.append(blunder_info)

        # On regarde si le Blunder peut se déplacer en continuant sa direction actuelle
        modify_properties_for_next_tile(grid, blunder)

        # On stocke la direction dans la solution
        solution = append_solution(solution, blunder)

    # On affiche la solution finale
    print(solution)


if __name__ == "__main__":
    main()
