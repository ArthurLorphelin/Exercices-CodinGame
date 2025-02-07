from dataclasses import dataclass
from typing import List, Optional, Set, Dict, Tuple
from enum import Enum
import sys
from collections import deque


# Classe qui représente les directions de mouvement possible pour les entités (clones) de jeu
class MovementDirection(Enum):
    LEFT = 0
    RIGHT = 1


# Classe qui représente une entité de jeu (clone) avec son état et ses possibilités
@dataclass
class GameEntity:
    x: int
    y: int
    remaining_clones: int
    remaining_elevators: int
    direction: MovementDirection
    action_history: str  # Les actions qui ont permis d'arriver à cet état


# Class principale du jeu qui gère la logique et la gestion de l'état
class Game:
    def __init__(self):
        # Dimension de la grille
        self.width: int = 0
        self.height: int = 0

        # Compteurs de ressource
        self.total_clones: int = 0
        self.total_elevators: int = 0

        # Suivi de l'état du jeu
        self.action_queues: List[deque] = []
        self.remaining_turns = 0
        self.visited_states: Dict[Tuple, bool] = {}

        # État de l'environnement (ascenseurs)
        self.elevator_positions: Set[Tuple[int, int]] = set()

        # Coordonnées de la sortie
        self.exit_x: int = 0
        self.exit_y: int = 0

    # Fonction qui lit les paramètres d'entrée et initialize l'état de jeu
    def read_input(self):
        params = [int(i) for i in input().split()]
        self.height = params[0]
        self.width = params[1]
        self.remaining_turns = params[2] + 1
        self.exit_y = params[3]
        self.exit_x = params[4]
        self.total_clones = params[5]
        self.total_elevators = params[6]

        # Initialisation du set de la position des ascenseurs
        elevator_count = params[7]
        for _ in range(elevator_count):
            y, x = map(int, input().split())
            self.elevator_positions.add((x, y))

    # Fonction qui met à jour l'état du jeu en fonction de l'action choisie
    def apply_action(self, action: str):
        if action == "ELEVATOR":
            self.total_clones -= 1
            self.total_elevators -= 1
        elif action == "BLOCK":
            self.total_clones -= 1

    # Fonction qui vérifie si la position horizontale respecte les contraintes de la grille
    def is_valid_position(self, x: int) -> bool:
        return 0 <= x < self.width

    # Fonction qui marque un état de jeu comme visité dans le cache
    def mark_state_visited(self, x: int, y: int, clones: int, elevators: int, direction: int):
        state = (x, y, clones, elevators, direction)
        if state not in self.visited_states:
            self.visited_states[state] = True

    # Fonction qui évalue et met en file d'attente tous les mouvements possibles pour l'état actuel du jeu
    def evaluate_possible_moves(self, entity: GameEntity, current_time: int):
        can_create_block_action = entity.remaining_clones > 0
        can_place_elevator_action = (
                entity.remaining_elevators > 0 and can_create_block_action and entity.y < self.exit_y)

        # On calcule les directions de mouvement
        move_direction = -1 if entity.direction == MovementDirection.LEFT else 1
        next_position = entity.x + move_direction
        opposite_position = entity.x - move_direction
        current_position = (entity.x, entity.y)

        # On évalue la faisabilité de chaque action possible
        self._try_blocking_action(entity, current_time, current_position, can_create_block_action, opposite_position)
        self._try_elevator_action(entity, current_time, current_position, can_place_elevator_action)
        self._try_elevator_movement(entity, current_time, current_position)
        self._try_horizontal_movement(entity, current_time, current_position, next_position)

    # Fonction qui évalue la faisabilité de l'action "BLOCK"
    def _try_blocking_action(self, entity: GameEntity, time: int, current_position: Tuple[int, int], can_block: bool,
                             target_position: int):
        if (current_position not in self.elevator_positions and self.is_valid_position(
                target_position) and time < self.remaining_turns - 5 and can_block):
            new_state = (target_position, entity.y, entity.remaining_clones - 1, entity.remaining_elevators,
                         1 - entity.direction.value)
            if new_state not in self.visited_states:
                action = "BLOCK" if time == 0 else entity.action_history
                self.action_queues[time + 4].append(
                    GameEntity(target_position, entity.y, entity.remaining_clones - 1, entity.remaining_elevators,
                               MovementDirection(1 - entity.direction.value), action))
                self.mark_state_visited(*new_state)

    # Fonction qui évalue la faisabilité de l'action "ELEVATOR"
    def _try_elevator_action(self, entity: GameEntity, time: int, current_position: Tuple[int, int], can_place: bool):
        if current_position not in self.elevator_positions and time < self.remaining_turns - 5 and can_place:
            new_state = (
                entity.x, entity.y + 1, entity.remaining_clones - 1, entity.remaining_elevators - 1,
                entity.direction.value)
            if new_state not in self.visited_states:
                action = "ELEVATOR" if time == 0 else entity.action_history
                self.action_queues[time + 4].append(
                    GameEntity(entity.x, entity.y + 1, entity.remaining_clones - 1, entity.remaining_elevators - 1,
                               entity.direction, action))
                self.mark_state_visited(*new_state)

    # Fonction qui évalue la faisabilité de prendre un ascenseur
    def _try_elevator_movement(self, entity: GameEntity, time: int, current_position: Tuple[int, int]):
        if current_position in self.elevator_positions and time < self.remaining_turns - 2:
            new_state = (
                entity.x, entity.y + 1, entity.remaining_clones, entity.remaining_elevators, entity.direction.value)
            if new_state not in self.visited_states:
                action = "WAIT" if time == 0 else entity.action_history
                self.action_queues[time + 1].append(
                    GameEntity(entity.x, entity.y + 1, entity.remaining_clones, entity.remaining_elevators,
                               entity.direction, action))
                self.mark_state_visited(*new_state)

    # Fonction qui évalue la faisabilité d'un mouvement horizontal
    def _try_horizontal_movement(self, entity: GameEntity, time: int, current_position: Tuple[int, int],
                                 target_position: int):
        if (current_position not in self.elevator_positions and self.is_valid_position(
                target_position) and time < self.remaining_turns - 2):
            new_state = (
                target_position, entity.y, entity.remaining_clones, entity.remaining_elevators, entity.direction.value)
            if new_state not in self.visited_states:
                action = "WAIT" if time == 0 else entity.action_history
                self.action_queues[time + 1].append(
                    GameEntity(target_position, entity.y, entity.remaining_clones, entity.remaining_elevators,
                               entity.direction, action))
                self.mark_state_visited(*new_state)

    # Fonction qui détermine le prochain mouvement optimal en utilisant BFS (Breadth-First Search)
    def determine_next_move(self, current_state: GameEntity) -> str:
        self.visited_states = {}
        self.action_queues = [deque() for _ in range(self.remaining_turns)]

        # On initialise avec l'état actuel du jeu
        self.action_queues[0].append(current_state)
        self.mark_state_visited(current_state.x, current_state.y, current_state.remaining_clones,
                                current_state.remaining_elevators, current_state.direction.value)

        # On cherche un chemin pour atteindre la sortie
        for time in range(self.remaining_turns):
            while self.action_queues[time]:
                current = self.action_queues[time].popleft()

                # On regarde si la sortie a été atteinte
                if current.y == self.exit_y and current.x == self.exit_x:
                    return current.action_history

                self.evaluate_possible_moves(current, time)
        return "WAIT"

    # Fonction qui traite un seul tour du jeu
    def process_turn(self):
        # On lit les entrées d'un tour de jeu
        inputs = input().split()
        y, x = int(inputs[0]), int(inputs[1])
        direction = inputs[2]

        # S'il n'y a pas de clone dans la grille
        if x == -1:
            print("WAIT", flush=True)
            return

        # On crée un état actuel du jeu
        direction_value = (MovementDirection.LEFT if direction == "LEFT" else MovementDirection.RIGHT)
        current_state = GameEntity(x, y, self.total_clones, self.total_elevators, direction_value, "WAIT")

        # On obtient et exécute le prochain mouvement
        move = self.determine_next_move(current_state)
        self.apply_action(move)
        print(move, flush=True)
        self.remaining_turns -= 1


# Boucle principale du jeu
def main():
    game = Game()
    game.read_input()

    while True:
        game.process_turn()


if __name__ == "__main__":
    main()
