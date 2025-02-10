from typing import Tuple
import sys
import math


# Classe qui représente Batman
class Batman:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y
        self.previous_position: Tuple[int, int] = None
        self.x_min: int = 0
        self.x_max: int = 0
        self.y_min: int = 0
        self.y_max: int = 0


# Classe qui gère la logique principale du jeu
class Game:
    def __init__(self):
        self.height: int = 0
        self.width: int = 0
        self.max_jumps: int = 0
        self.batman: Batman = None

    # Fonction qui lit les entrées de jeu et l'initialise
    def read_input(self):
        self.width, self.height = map(int, input().split())
        self.max_jumps = int(input())
        batman_x, batman_y = map(int, input().split())
        self.batman = Batman(batman_x, batman_y)

        # On initialise les coordonnées max de Batman
        self.batman.x_min = 0
        self.batman.x_max = self.width - 1
        self.batman.y_min = 0
        self.batman.y_max = self.height - 1

    # Fonction qui permet de gérer un tour du jeu
    def process_turn(self):
        bomb_direction = input()
        print(f"Direction : {bomb_direction}", file=sys.stderr)

        # On recherche les nouvelles limites de la grille et on calcule les coordonnées du prochain saut
        self._update_search_boundaries(bomb_direction)
        next_x = (self.batman.x_min + self.batman.x_max) // 2
        next_y = (self.batman.y_min + self.batman.y_max) // 2

        # On stocke les nouvelles positions de Batman
        self.batman.previous_position = (self.batman.x, self.batman.y)
        self.batman.x = next_x
        self.batman.y = next_y

        # On affiche la solution
        self._print_next_position()

    # Fonction qui met à jour les limites de recherche de la bombe
    def _update_search_boundaries(self, direction: str):
        if 'U' in direction:
            self.batman.y_max = self.batman.y - 1
        if 'R' in direction:
            self.batman.x_min = self.batman.x + 1
        if 'D' in direction:
            self.batman.y_min = self.batman.y + 1
        if 'L' in direction:
            self.batman.x_max = self.batman.x - 1

    # Fonction qui affiche les prochaines coordonnées de Batman
    def _print_next_position(self):
        print(f"{self.batman.x} {self.batman.y}")


# Fonction qui gère tout
def main():
    game = Game()
    game.read_input()

    while True:
        game.process_turn()


if __name__ == "__main__":
    main()
