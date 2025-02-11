from typing import List
from collections import deque

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
        self.connected_gateway: List[Gateway] = []
        self.links: List[Link] = []


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
                    node.connected_gateway.append(new_gateway)

    # Fonction qui permet de trouver un nœud à partir de son index
    def _find_node_by_index(self, index: int) -> Node:
        for node in self.all_nodes:
            if node.index == index:
                return node
        return None

    # Fonction qui permet de trouver une passerelle de sortie à partir de son index
    def _find_gateway_by_index(self, index: int) -> Gateway:
        for gateway in self.all_gateways:
            if gateway.index == index:
                return gateway
        return None

    # Fonction qui lit les entrées d'un tour de jeu et détermine quel lien à détruire
    def process_turn(self):
        # On récupère la position du Botnet pour ce tour
        index_node_botnet = int(input())
        botnet_node = self._find_node_by_index(index_node_botnet)

        # On récupère tous les chemins qui mènent à une passerelle de sortie
        all_paths = self._compute_all_paths_to_gateways(botnet_node)
        path_to_cut = self._find_correct_path(all_paths)
        link_to_destroy = path_to_cut[-1]
        self._print_link_to_destroy(link_to_destroy)

    # Fonction qui utilise un algorithme BFS pour trouver tous les chemins menant à une passerelle de sortie
    def _compute_all_paths_to_gateways(self, botnet_node: Node) -> List[List[Link]]:
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
                    for gateway in node.connected_gateway:
                        if not link.is_destroyed and (
                                link.index_node1 == gateway.index
                                or link.index_node2 == gateway.index):
                            gateway_path = current_path + [link]
                            all_paths_to_gateway.append(gateway_path)

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

    # Fonction qui calcule combien de chemins différents existe pour un nœud pour atteindre une passerelle de sortie
    def _calculate_number_of_paths_to_gateway(self, botnet_node: Node) -> int:
        count = 0
        visited = set()
        queue = deque([(botnet_node, [])])

        while queue:
            current_node, path = queue.popleft()
            if current_node.index in visited:
                continue
            visited.add(current_node.index)

            # On compte le nombre de connexions directes à des passerelles de sortie
            for link in current_node.links:
                if not link.is_destroyed:
                    other_index = link.index_node1 if current_node.index != link.index_node1 else link.index_node2
                    if other_index in self.all_gateways_index:
                        count += 1
                        continue

                    next_node = self._find_node_by_index(other_index)
                    queue.append((next_node, path + [link]))
        return count

    # Fonction qui regarde si chaque nœud du chemin n'a qu'une seule option pour atteindre une passerelle de sortie
    def _is_critical_path(self, path: List[Link]) -> bool:
        for link in path[:-1]:
            for index in [link.index_node1, link.index_node2]:
                if index not in self.all_gateways_index:
                    node = self._find_node_by_index(index)
                    if self._calculate_number_of_paths_to_gateway(node) == 1:
                        return True
        return False

    # Fonction qui retourne le chemin le plus court parmi toutes les possibilités
    def _find_correct_path(self, all_paths: List[List[Link]]) -> List[Link]:
        if not all_paths:
            return []

        # On trie la liste de chemins par ordre de taille croissant et on retourne le premier élément s'il est de
        # taille 1
        all_paths.sort(key=len)
        if len(all_paths[0]) == 1:
            return all_paths[0]

        # On recherche le chemin le plus critique
        most_critical_path = all_paths[0]
        highest_criticality = -1
        for path in all_paths:
            path_complexity = self._calculate_path_complexity(path)
            path_criticality = path_complexity / len(path)
            if (path_criticality > highest_criticality or (
                    path_criticality == highest_criticality and len(path) < len(most_critical_path))):
                most_critical_path = path
                highest_criticality = path_criticality
        return most_critical_path

    # Fonction qui calcule la complexité pour un chemin
    def _calculate_path_complexity(self, path: List[Link]) -> int:
        complexity = 0
        visited_nodes = set()

        # On regarde pour chaque lien et nœud de ce lien
        for link in path:
            for node_index in [link.index_node1, link.index_node2]:
                if node_index not in self.all_gateways_index and node_index not in visited_nodes:
                    visited_nodes.add(node_index)
                    node = self._find_node_by_index(node_index)

                    # On crée un compteur pour les connexions actives à une passerelle de sortie
                    gateway_connexions = 0
                    for node_link in node.links:
                        if not node_link.is_destroyed:
                            other_index = node_link.index_node1 if node.index != node_link.index_node1 \
                                else node_link.index_node2
                            if other_index in self.all_gateways_index:
                                gateway_connexions += 1
                    complexity += gateway_connexions
        return complexity

    # Fonction qui affiche la sortie pour un tour de jeu et on met à jour l'état du lien et du nœud
    def _print_link_to_destroy(self, link_to_destroy: Link):
        link_to_destroy.is_destroyed = True
        for index in [link_to_destroy.index_node1, link_to_destroy.index_node2]:
            if index not in self.all_gateways_index:
                node = self._find_node_by_index(index)
                node.connected_gateway = [gateway for gateway in node.connected_gateway if
                                          gateway.index != link_to_destroy.index_node2
                                          and gateway.index != link_to_destroy.index_node2]
        print(f"{link_to_destroy.index_node1} {link_to_destroy.index_node2}")


# Fonction d'agencement de toute la logique
def main():
    game = Game()
    game.read_input()

    while True:
        game.process_turn()


if __name__ == "__main__":
    main()
