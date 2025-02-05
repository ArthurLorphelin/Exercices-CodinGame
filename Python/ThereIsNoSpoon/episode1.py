from typing import List, Tuple

import sys

# Fonction qui lit les entrées et stocke la liste sous forme de liste de listes
def read_input() -> Tuple[int, int, List[List[str]]]:
    width = int(input())
    height = int(input())
    grid = [list(input().strip()) for _ in range(height)]
    return width, height, grid

# Fonction qui trouve le voisin à droite du nœud
def find_right_neighbor(grid: List[List[str]], x: int, y: int, width: int) -> Tuple[int, int]:
    for neighbor_x in range(x+1, width):
        if grid[y][neighbor_x] == '0':
            return neighbor_x, y
    return -1, -1

# Fonction qui trouve le voisin en dessous du nœud
def find_bottom_neighbor(grid: List[List[str]], x: int, y: int, height: int) -> Tuple[int, int]:
    for neighbor_y in range(y+1, height):
        if grid[neighbor_y][x] == '0':
            return x, neighbor_y
    return -1, -1

# Fonction qui parcourt la grille et affiche les coordonnées des nœuds et de leurs prochains voisins
def process_grid(width: int, height: int, grid: List[List[str]]):
    for y in range(height):
        for x in range(width):
            if grid[y][x] == '0':
                right_x, right_y = find_right_neighbor(grid, x, y, width)
                bottom_x, bottom_y = find_bottom_neighbor(grid, x, y, height)
                print(f"{x} {y} {right_x} {right_y} {bottom_x} {bottom_y}")

def main():
    width, height, grid = read_input()
    process_grid(width, height, grid)

if __name__ == "__main__":
    main()