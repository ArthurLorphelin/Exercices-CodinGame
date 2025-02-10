from typing import List, Set
import sys

# Pas tous les tous sont passés
# Exercice validé à 70%

# Constantes
MAX_LINKS_BETWEEN_2_NODES: int = 2


# Classe qui représente un nœud dans la grille
class Node:
    def __init__(self, x: int, y: int, nb_links_needed: int):
        self.x: int = x
        self.y: int = y
        self.nb_links_needed: int = nb_links_needed
        self.channels: List[Channel] = []
        self.used_links: List[bool] = [False] * self.nb_links_needed
        self.remaining_links: int = nb_links_needed

    # Fonction qui regarde si le nœud est parfaitement construit
    def is_perfect_node(self) -> bool:
        return self.remaining_links == 0

    # Fonction qui regarde si le nœud a des liens disponibles à établir
    def have_available_links(self) -> bool:
        return self.remaining_links > 0

    # Fonction qui permet d'obtenir l'index du prochain lien libre
    def get_next_available_link_index(self):
        for index, used in enumerate(self.used_links):
            if not used:
                self.used_links[index] = True
                self.remaining_links -= 1
                return index
        return -1

    # Fonction qui permet de libérer un lien déjà créé
    def release_link_index(self, index: int):
        if 0 <= index < len(self.used_links):
            self.used_links[index] = False
            self.remaining_links += 1


# Classe qui représente les canaux de lien entre deux nœuds
class Channel:
    def __init__(self, node1: Node, node2: Node):
        self.nodes: List[Node] = [node1, node2]
        self.max_links_capacity: int = min(MAX_LINKS_BETWEEN_2_NODES, node1.nb_links_needed, node2.nb_links_needed)
        self.intersections: List[Intersection] = []
        self.nb_links_established: int = 0
        self.distance: int = abs(node1.x - node2.x) + abs(node1.y - node2.y)

    # Fonction qui regarde si le canal a la taille pour établir un lien
    def _is_channel_not_full(self) -> bool:
        return self.nb_links_established < self.max_links_capacity

    # Fonction qui regarde si les intersections sont disponibles
    def _are_intersections_available(self) -> bool:
        return all(intersection.is_intersection_not_used(self) for intersection in self.intersections)

    # Fonction qui réserve toutes les intersections pour ce canal
    def _block_intersections(self):
        for intersection in self.intersections:
            intersection.active_channel = self

    # Fonction qui libère toutes les intersections pour ce canal
    def release_intersections(self):
        for intersection in self.intersections:
            intersection.release_channel(self)

    # Fonction qui regarde si les 2 nœuds ont la place d'établir un lien
    def _have_nodes_available_links(self) -> bool:
        return all(node.have_available_links() for node in self.nodes)

    # Fonction qui regarde si toutes les conditions sont réunies pour établir un lien
    def _can_channel_establish_link(self) -> bool:
        return self._is_channel_not_full() and \
               self._are_intersections_available() and \
               self._have_nodes_available_links()

    # Fonction qui crée l'action d'établir un lien
    def create_action(self) -> List['Action']:
        if not self._can_channel_establish_link():
            return []
        # On réserve toutes les intersections pour ce canal
        self._block_intersections()
        actions_made = []
        # On regarde si le premier nœud a la place d'établir un lien, puis le deuxième
        # et si c'est le cas, on crée l'action.
        first_node_available_link_index = self.nodes[0].get_next_available_link_index()
        if first_node_available_link_index >= 0:
            second_node_available_link_index = self.nodes[1].get_next_available_link_index()
            if second_node_available_link_index >= 0:
                new_action = Action(self, self.nb_links_established)
                first_node_link = Link(self.nodes[0], first_node_available_link_index)
                second_node_link = Link(self.nodes[1], second_node_available_link_index)
                new_action.covered_links.extend([first_node_link, second_node_link])
                actions_made.append(new_action)
            # Sinon, on libère le lien qu'on avait réservé
            else:
                self.nodes[0].release_link_index(first_node_available_link_index)
        # On libère les intersections qu'on avait bloquées
        if not actions_made:
            self.release_intersections()
        # On retourne la liste des actions effectuées
        return actions_made


# Classe qui représente une intersection dans la grille
class Intersection:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y
        self.active_channel: Channel = None

    # Fonction qui regarde si l'intersection est dans un canal avec des liens établis
    def is_intersection_not_used(self, current_channel: Channel) -> bool:
        return self.active_channel is None or self.active_channel == current_channel

    # Fonction qui libère le canal en cas de marche arrière
    def release_channel(self, channel: Channel):
        if self.active_channel == channel:
            self.active_channel = None


# Classe qui représente chacun des liens à créer
class Link:
    def __init__(self, node: Node, link_index: int):
        self.node: Node = node
        self.link_index: int = link_index


# Classe qui représente l'action de créer un lien
class Action:
    def __init__(self, channel: Channel, link_index: int):
        self.channel: Channel = channel
        self.link_index: int = link_index
        self.covered_links: List[Link] = []

    # Fonction qui permet d'annuler une action
    def undo(self):
        # On libère les liens établis
        for link in self.covered_links:
            link.node.release_link_index(link.link_index)
        # On libère les intersections réservées
        self.channel.release_intersections()


# Class qui gère la logique principale du jeu
class Game:
    def __init__(self):
        self.width: int = 0
        self.height: int = 0
        self.all_nodes: List[Node] = []
        self.all_intersections: List[Intersection] = []
        self.all_channels: List[Channel] = []
        self.current_solution: List[Action] = []
        self.total_links_needed: int = 0

    # Fonction qui lit les entrées du jeu et initialise toutes les instances de classe Node et Intersection
    def read_input(self):
        self.width = int(input())
        self.height = int(input())
        grid = [list(input().strip()) for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                if grid[y][x] == ".":
                    new_intersection = Intersection(x, y)
                    self.all_intersections.append(new_intersection)
                else:
                    links_needed = int(grid[y][x])
                    new_node = Node(x, y, links_needed)
                    self.all_nodes.append(new_node)
                    self.total_links_needed += links_needed

    # Fonction qui parcourt tous les nœuds et regarde s'il a un voisin à droite, crée le Channel entre ces 2 nœuds
    # et identifie les possibles intersections
    def find_right_neighbor(self, node: Node):
        min_distance = float('inf')
        closest_right_node = None
        # On cherche le voisin de droite le plus proche
        for right_node in self.all_nodes:
            if right_node.x > node.x and right_node.y == node.y:
                distance = right_node.x - node.x
                if distance < min_distance:
                    min_distance = distance
                    closest_right_node = right_node
        # S'il y a un voisin à droite, on crée le canal
        if closest_right_node:
            new_channel = Channel(node, closest_right_node)
            self.all_channels.append(new_channel)
            node.channels.append(new_channel)
            closest_right_node.channels.append(new_channel)
            # Si la distance entre les deux nœuds est supérieure à 1, il y a au moins une Intersection
            if min_distance > 1:
                for intersection in self.all_intersections:
                    if intersection.y == node.y and node.x < intersection.x < closest_right_node.x:
                        new_channel.intersections.append(intersection)

    # Fonction qui regarde tous les nœuds et regarde s'il existe un voisin en dessous, crée le Channel entre ces
    # deux nœuds et identifie les possibles intersections
    def find_bottom_neighbor(self, node: Node):
        min_distance = float('inf')
        closest_bottom_node = None
        # On cherche le voisin du dessous le plus proche
        for bottom_node in self.all_nodes:
            if bottom_node.x == node.x and bottom_node.y > node.y:
                distance = bottom_node.y - node.y
                if distance < min_distance:
                    min_distance = distance
                    closest_bottom_node = bottom_node
        # S'il y a un voisin en dessous, on crée le canal
        if closest_bottom_node:
            new_channel = Channel(node, closest_bottom_node)
            self.all_channels.append(new_channel)
            node.channels.append(new_channel)
            closest_bottom_node.channels.append(new_channel)
            # Si la distance entre les deux nœuds est supérieure à 1, il y a au moins une Intersection
            if min_distance > 1:
                for intersection in self.all_intersections:
                    if intersection.x == node.x and node.y < intersection.y < closest_bottom_node.y:
                        new_channel.intersections.append(intersection)

    # Fonction qui retourne le nœud avec le plus de contraintes
    def _get_most_constrained_nodes(self) -> Node:
        return max((node for node in self.all_nodes if node.have_available_links()),
                   key=lambda node: (node.remaining_links, -sum(1 for channel in node.channels
                                        if channel.nb_links_established < channel.max_links_capacity)),
                   default=None)

    # Fonction qui retourne la liste des canaux triés par score de priorité
    def _get_best_channels(self, node: Node) -> List[Channel]:
        return sorted(
            [channel for channel in node.channels if channel.nb_links_established < channel.max_links_capacity],
            key=lambda channel: (-sum(node.remaining_links for node in channel.nodes),
                                 len(channel.intersections),
                                 channel.distance)
        )

    # Fonction de résolution de l'algorithme backtrack (retour en arrière)
    def _solve_backtrack_algorithm(self) -> bool:
        # On regarde si chaque nœud est parfaitement lié
        if all(node.is_perfect_node() for node in self.all_nodes):
            return True

        # On prend le nœud avec le plus de contraintes
        current_node = self._get_most_constrained_nodes()
        if not current_node:
            return False

        # On regarde tous les canaux qui ne sont pas pleins
        for channel in self._get_best_channels(current_node):
            # On crée l'action pour le canal
            possible_actions = channel.create_action()
            for action in possible_actions:
                channel.nb_links_established += 1
                self.current_solution.append(action)

                # On regarde de manière récursive si on trouve la solution
                if self._solve_backtrack_algorithm():
                    return True

                # Sinon, on annule l'action
                channel.nb_links_established -= 1
                action.undo()
                self.current_solution.pop()

        # On retourne False si aucune solution n'a été trouvée
        return False

    # Fonction qui retourne les solutions trouvées par l'algorithme
    def find_solution(self) -> List[Action]:
        self.all_nodes.sort(key=lambda node: (-node.nb_links_needed, -len(node.channels), node.x + node.y))
        self.current_solution = []
        if self._solve_backtrack_algorithm():
            return self.current_solution
        return []

    # Fonction qui affiche la solution selon le type de sortie demandée
    def print_solution(self, solution: List[Action]):
        if not solution:
            print("No solution found", file=sys.stderr)
            return

        # On affiche le bon format de solution
        for action in solution:
            channel = action.channel
            first_node = channel.nodes[0]
            second_node = channel.nodes[1]
            print(f"{first_node.x} {first_node.y} {second_node.x} {second_node.y} 1")


# Fonction qui permet de gérer le jeu
def main():
    game = Game()
    game.read_input()

    # On cherche tous les voisins à droite et en dessous de chaque nœud et on crée els canaux
    for node in game.all_nodes:
        game.find_right_neighbor(node)
        game.find_bottom_neighbor(node)

    # On cherche et on affiche la solution
    solution = game.find_solution()
    game.print_solution(solution)


if __name__ == "__main__":
    main()
