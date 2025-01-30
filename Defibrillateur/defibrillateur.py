import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

EARTH_RADIUS = 6371

class Defibrilateur:
    def __init__(self, information):
        splitted_information = information.split(";")
        self.id_number = splitted_information[0]
        self.name = splitted_information[1]
        self.address = splitted_information[2]
        self.telephone_number = splitted_information[3]
        self.longitude = convert_degrees_to_radians(splitted_information[4])
        self.latitude = convert_degrees_to_radians(splitted_information[5])

    # Getter de la longitude du défibrilateur
    def get_longitude(self):
        return self.longitude

    # Getter de la latitude du défibrilateur
    def get_latitude(self):
        return self.latitude

    # Getter du name du défibrilateur
    def get_name(self):
        return self.name

# Fonction qui convertit une valeur de degrés à radians
def convert_degrees_to_radians(coordinates):
    coordinates_degrees = float(coordinates.replace(",", "."))
    return math.radians(coordinates_degrees)

# Fonction qui calcule la distance entre un défibrilateur et un user
def calculate_distance(defibrilateur, user_longitude, user_latitude):
    x_axis_distance = calculate_x_axis_distance(defibrilateur, user_longitude, user_latitude)
    y_axis_distance = calculate_y_axis_distance(defibrilateur, user_latitude)
    total_distance = math.sqrt(math.pow(x_axis_distance, 2) + math.pow(y_axis_distance, 2)) * EARTH_RADIUS
    return total_distance

# Fonction qui calcule la distance sur l'axe x entre un défibrilateur et un user
def calculate_x_axis_distance(defibrilateur, user_longitude, user_latitude):
    return (defibrilateur.get_longitude() - user_longitude) * math.cos((defibrilateur.get_latitude() + user_latitude) / 2)

# Fonction qui calcule la distance sur l'axe y entre un défibrilateur et un user
def calculate_y_axis_distance(defibrilateur, user_latitude):
    return (defibrilateur.get_latitude() - user_latitude)

def main():
    user_longitude = convert_degrees_to_radians(input().strip())
    user_latitude = convert_degrees_to_radians(input().strip())

    # On instancie la liste de défibrillateurs
    n = int(input().strip())
    defibrillateurs = []
    for _ in range(n):
        defibrilateur_info = input().strip()
        new_defibrilateur = Defibrilateur(defibrilateur_info)
        defibrillateurs.append(new_defibrilateur)
    
    # On parcourt la liste de défibrillateurs à la recherche du défibrillateur le plus proche
    minimum = float('inf')
    index_minimum = 0
    distances = []
    for index_defibrillateur in range(n):
        distance = calculate_distance(defibrillateurs[index_defibrillateur], user_longitude, user_latitude)
        distances.append(distance)
        
        # On stocke l'index de la distance minimale
        if distance < minimum:
            minimum = distance
            index_minimum = index_defibrillateur

    # On affiche le nom du défibrilateur le plus proche
    print(defibrillateurs[index_minimum].get_name())

if __name__ == "__main__":
    main()
