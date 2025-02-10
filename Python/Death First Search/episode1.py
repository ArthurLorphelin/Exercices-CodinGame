from typing import List, Set
from collections import deque
import sys
import math


# Classe qui représente un lien entre deux nœuds
class Link:
    def __init__(self, index_node1: int, index_node2: int):
        self.index_node1: int = index_node1
        self.index_node2: int = index_node2
        self.is_destroyed: bool = False


# Classe qui représente un nœud dans la carte de sous-réseau
class Node:
    def __init__(self, index: int):
        self.index: int = index
        self.connected_gateway: Gateway | None = None
        self.links: List[Link] = []
        self.distance: int = 0


# Classe qui représente une passerelle de sortie
class Gateway:
    def __init__(self, index: int):
        self.index: int = index
        self.links: List[Link] = []
        self.is_reachable: bool = True


# Classe qui représente le jeu
class Game:
    def __init__(self):
        self.nb_nodes: int = 0
        self.nb_links: int = 0
        self.nb_gateways: int = 0
        self.all_nodes: List[Node] = []
        self.all_links: List[Link] = []
        self.all_gateways_index: List[int] = []
        self.all_gateways: List[Gateway] = []

    # Fonction qui lit et stocke les entrées d'initialisation
    def read_input(self):
        self.nb_nodes, self.nb_links, self.nb_gateways = map(int, input().split())
        # On initialise les nœuds et on retire le nombre de passerelles de sortie au nombre de nœuds
        self._initialize_nodes()
        self.nb_nodes -= self.nb_gateways

        # On initialise les liens
        for _ in range(self.nb_links):
            index_node1, index_node2 = map(int, input().split())
            self._initialize_links(index_node1, index_node2)

        # On initialize les passerelles de sortie
        for _ in range(self.nb_gateways):
            index_gateway = int(input())
            self._initialize_gateways(index_gateway)
        print(self.all_gateways, file=sys.stderr)

    # Fonction qui instancie tous les nœuds
    def _initialize_nodes(self):
        for index_node in range(self.nb_nodes):
            new_node = Node(index_node)
            self.all_nodes.append(new_node)

    # Fonction qui instancie les liens et les ajoute aux nœuds
    def _initialize_links(self, index_node1: int, index_node2: int):
        new_link = Link(index_node1, index_node2)
        self.all_links.append(new_link)
        node1 = self.all_nodes[index_node1]
        node2 = self.all_nodes[index_node2]
        node1.links.append(new_link)
        node2.links.append(new_link)

    # Fonction qui instancie les passerelles de sortie
    def _initialize_gateways(self, index_gateway: int):
        # On crée la passerelle de sortie et on lui attribue les liens du nœud du même index
        new_gateway = Gateway(index_gateway)
        self.all_gateways.append(new_gateway)
        self.all_gateways_index.append(index_gateway)
        node_to_delete = self._find_node_by_index(index_gateway)
        new_gateway.links = node_to_delete.links.copy()

        # On ajoute la passerelle de sortie à tous les nœuds qui ont un lien direct avec elle
        for link in new_gateway.links:
            for index_node in [link.index_node1, link.index_node2]:
                if index_node != index_gateway:
                    node = self._find_node_by_index(index_node)
                    node.connected_gateway = new_gateway

    # Fonction qui permet de trouver un nœud à partir de son index
    def _find_node_by_index(self, index: int) -> Node | None:
        for node in self.all_nodes:
            if node.index == index:
                return node
        return None

    # Fonction qui lit les entrées d'un tour de jeu et détermine quel lien à détruire
    def process_turn(self):
        index_node_botnet = int(input())
        botnet_node = self._find_node_by_index(index_node_botnet)
        print(botnet_node.connected_gateway, file=sys.stderr)
        all_paths = self._calculate_distance_between_Botnet_and_gateway(botnet_node)
        shortest_path = self._find_shortest_path(all_paths)
        link_to_destroy = shortest_path[-1]
        self._print_link_to_destroy(link_to_destroy)

    # Fonction qui calcule la distance minimale entre le nœud de Botnet et une passerelle de sortie
    # grâce à un algorithme BFS
    def _calculate_distance_between_Botnet_and_gateway(self, botnet_node: Node) -> List[List[Link]]:
        all_paths_to_gateway = []
        paths = {botnet_node: []}
        queue = deque([botnet_node])
        visited = {botnet_node}

        while queue:
            node = queue.popleft()
            current_path = paths[node]

            # On regarde si le nœud est adjacent à une passerelle de sortie
            if node.connected_gateway:
                for link in node.links:
                    if not link.is_destroyed and (
                            link.index_node1 == node.connected_gateway.index
                            or link.index_node2 == node.connected_gateway.index):
                        gateway_path = current_path + [link]
                        all_paths_to_gateway.append(gateway_path)
                        continue

            # On regarde pour chaque lien du nœud s'il est arrivé à une passerelle de sortie
            for link in node.links:
                if not link.is_destroyed:
                    new_index = link.index_node1 if link.index_node1 != node.index else link.index_node2

                    # Sinon, on regarde si le nœud a déjà été visité
                    new_node = None
                    for next_node in self.all_nodes:
                        if next_node.index == new_index:
                            new_node = next_node
                            break

                    if new_node and new_node not in visited:
                        queue.append(new_node)
                        visited.add(new_node)
                        paths[new_node] = current_path + [link]

        # On retourne tous les chemins qui mènent aux passerelles de sortie
        return all_paths_to_gateway

    # Fonction qui retourne le chemin le plus court parmi toutes les possibilités
    def _find_shortest_path(self, all_paths: List[List[Link]]) -> List[Link]:
        shortest_path = []
        shortest_path_length = float('inf')
        for path in all_paths:
            if len(path) < shortest_path_length:
                shortest_path = path
                shortest_path_length = len(path)
        return shortest_path

    # Fonction qui affiche la sortie pour un tour de jeu et on met à jour l'état du lien
    def _print_link_to_destroy(self, link_to_destroy: Link):
        link_to_destroy.is_destroyed = True
        print(f"{link_to_destroy.index_node1} {link_to_destroy.index_node2}")


# Fonction d'agencement de toute la logique
def main():
    game = Game()
    game.read_input()

    while True:
        game.process_turn()


if __name__ == "__main__":
    main()
