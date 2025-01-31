import sys

# Fonction qui lit les entrées de jeu et récupère les paramètres du jeu
def read_input():
    nb_floors, width, nb_rounds, exit_floor, exit_pos, nb_total_clones, nb_additional_elevators, nb_elevators = map(int, input().split())
    elevators = {}
    for _ in range(nb_elevators):
        elevator_floor, elevator_pos = map(int, input().split())
        elevators[elevator_floor] = elevator_pos

    return exit_floor, exit_pos, elevators

# Fonction qui détermine la direction dans laquelle se clone doit aller
def determine_exit_direction(clone_floor, clone_pos, exit_floor, exit_pos, elevators):
    if clone_floor == exit_floor:
        return "RIGHT" if clone_pos < exit_pos else "LEFT" if clone_pos > exit_pos else "WAIT"

    if clone_floor in elevators:
        elevator_pos = elevators[clone_floor]
        if clone_pos == elevator_pos:
            return "WAIT"
        return "RIGHT" if clone_pos < elevator_pos else "LEFT"

    return "WAIT"

# Boucle principale du jeu
def process_game(exit_floor, exit_pos, elevators):
    while True:
        inputs = input().split()
        clone_floor = int(inputs[0])
        clone_pos = int(inputs[1])
        direction = inputs[2]

        exit_direction = determine_exit_direction(clone_floor, clone_pos, exit_floor, exit_pos, elevators)

        if exit_direction == "WAIT":
            print("WAIT")
        else:
            print("WAIT" if direction == exit_direction else "BLOCK")

def main():
    exit_floor, exit_pos, elevators = read_input()
    process_game(exit_floor, exit_pos, elevators)


if __name__ == "__main__":
    main()