from typing import List, Tuple, Set
import sys
import math

# Constants
DIRECTIONS = {
    "SOUTH": (0, 1),
    "EAST": (1, 0),
    "NORTH": (0, -1),
    "WEST": (-1, 0)
}
DIRECTION_ORDER = ["SOUTH", "EAST", "NORTH", "WEST"]
DIRECTION_CHARS = {"S": "SOUTH", "E": "EAST", "N": "NORTH", "W": "WEST"}


# Classe représentant le robot Blunder avec son état et sa position
class Blunder:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y
        self.current_direction: str = "SOUTH"
        self.breaker_mode: bool = False
        self.direction_order: List[str] = DIRECTION_ORDER.copy()
        self.index_direction: int = 0

    # Fonction qui retourne un tuple représentant l'état complet du robot
    def get_state(self, grid_modifications: int):
        return (self.x, self.y, self.current_direction, self.breaker_mode, self.index_direction, grid_modifications)

    # Fonction qui calcule la prochaine position du robot selon sa position actuelle
    def get_next_position(self):
        dx, dy = DIRECTIONS[self.current_direction]
        return self.x + dx, self.y + dy


# Classe principale gérant la logique du jeu
class Game:
    def __init__(self):
        self.height, self.width, self.grid = self._read_input()
        self.blunder: Blunder = self._init_blunder()
        self.exit_pos: Tuple[int, int] = self._find_position("$")
        self.teleporters: List[Tuple[int, int]] = self._find_teleporters()
        self.visited_states: Set[Tuple[int, int, str, bool, int, int]] = set()
        self.grid_modifications: int = 0
        self.moves: List[str] = []

    # Fonction qui lit les données d'entrée
    def _read_input(self) -> Tuple[int, int, List[List[str]]]:
        height, width = map(int, input().split())
        grid = [list(input().strip()) for _ in range(height)]
        return height, width, grid

    # Fonction qui trouve la position initiale du Blunder et crée l'instance
    def _init_blunder(self) -> Blunder:
        x, y = self._find_position("@")
        return Blunder(x, y)

    # Fonction qui trouve la position d'un caractère spécifique dans la grille
    def _find_position(self, char: str) -> Tuple[int, int]:
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == char:
                    return x, y
        return -1, -1

    # Fonction qui trouve toutes les positions des téléporteurs dans la grille et les retourne dans une liste
    def _find_teleporters(self) -> List[Tuple[int, int]]:
        return [(x, y) for y in range(self.height)
                for x in range(self.width) if self.grid[y][x] == "T"]

    # Fonction qui vérifie si une position donnée contient un obstacle
    def is_obstacle(self, x: int, y: int) -> bool:
        cell = self.grid[y][x]
        return cell == "#" or (cell == "X" and not self.blunder.breaker_mode)

    # Fonction qui gère les effets des cases spéciales sur lesquelles se trouve
    def handle_special_tile(self):
        x, y = self.blunder.x, self.blunder.y
        cell = self.grid[y][x]

        # Case modificateur de trajectoire
        if cell in DIRECTION_CHARS:
            self.blunder.current_direction = DIRECTION_CHARS[cell]
            self.blunder.index_direction = DIRECTION_ORDER.index(DIRECTION_CHARS[cell])

        # Case inverseur de circuits
        elif cell == "I":
            self.blunder.direction_order.reverse()
            self.blunder.index_direction = (len(DIRECTION_ORDER) - self.blunder.index_direction - 1)

        # Case Bière
        elif cell == "B":
            self.blunder.breaker_mode = not self.blunder.breaker_mode

        # Case obstacle X en mode casseur
        elif cell == "X" and self.blunder.breaker_mode:
            self.grid[y][x] = " "
            self.grid_modifications += 1

        # Case téléporteur
        elif cell == "T":
            for tx, ty in self.teleporters:
                if (tx, ty) != (x, y):
                    self.blunder.x, self.blunder.y = tx, ty
                    break

    # Fonction qui déplace le Blunder selon les règles du jeu
    def move_blunder(self):
        next_x, next_y = self.blunder.get_next_position()

        # Si la prochaine case est un obstacle, on essaie les directions dans l'ordre
        if self.is_obstacle(next_x, next_y):
            self.blunder.index_direction = 0
            while True:
                self.blunder.current_direction = self.blunder.direction_order[self.blunder.index_direction]
                next_x, next_y = self.blunder.get_next_position()
                if not self.is_obstacle(next_x, next_y):
                    break
                self.blunder.index_direction += 1

        # Lorsque la prochaine case n'est pas un obstacle
        self.blunder.x, self.blunder.y = next_x, next_y
        self.moves.append(self.blunder.current_direction)

    # Fonction qui vérifie si Blunder est arrivé à la sortie
    def is_at_exit(self) -> bool:
        return (self.blunder.x, self.blunder.y) == self.exit_pos

    # Fonction qui vérifie si l'état actuel a déjà été visité (boucle infinie)
    def check_loop(self) -> bool:
        state = self.blunder.get_state(self.grid_modifications)
        if state in self.visited_states:
            return True
        self.visited_states.add(state)
        return False

    # Fonction qui exécute la simulation du jeu
    def run(self) -> str:
        while not self.is_at_exit():
            self.handle_special_tile()

            if self.check_loop():
                return "LOOP"

            self.move_blunder()

        return "\n".join(self.moves)


# Point d'entrée du programme
def main():
    game = Game()
    print(game.run())


if __name__ == "__main__":
    main()
