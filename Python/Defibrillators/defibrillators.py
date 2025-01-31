import sys
import math

EARTH_RADIUS = 6371

class Defibrillator:
    def __init__(self, information):
        splitted_information = information.split(";")
        self.id_number = splitted_information[0]
        self.name = splitted_information[1]
        self.address = splitted_information[2]
        self.telephone_number = splitted_information[3]
        self.longitude = self.convert_degrees_to_radians(splitted_information[4])
        self.latitude = self.convert_degrees_to_radians(splitted_information[5])

    # Fonction qui convertit une valeur de degrés à radians
    @staticmethod
    def convert_degrees_to_radians(coordinates):
        coordinates_degrees = float(coordinates.replace(",", "."))
        return math.radians(coordinates_degrees)

# Fonction qui calcule la distance entre un défibrillateur et un utilisateur
def calculate_distance(defibrillator, user_longitude, user_latitude):
    x_axis_distance = calculate_x_axis_distance(defibrillator, user_longitude, user_latitude)
    y_axis_distance = calculate_y_axis_distance(defibrillator, user_latitude)
    return math.sqrt(math.pow(x_axis_distance, 2) + math.pow(y_axis_distance, 2)) * EARTH_RADIUS

# Fonction qui calcule la distance sur l'axe x entre un défibrillateur et un utilisateur
def calculate_x_axis_distance(defibrillator, user_longitude, user_latitude):
    return (defibrillator.longitude - user_longitude) * math.cos((defibrillator.latitude + user_latitude) / 2)

# Fonction qui calcule la distance sur l'axe y entre un défibrillateur et un utilisateur
def calculate_y_axis_distance(defibrillator, user_latitude):
    return defibrillator.latitude - user_latitude

# Fonction qui trouve le défibrillateur le plus proche de l'utilisateur
def find_nearest_defibrillator(user_longitude, user_latitude, defibrillators):
    return min(defibrillators, key=lambda d: calculate_distance(d, user_longitude, user_latitude))

def main():
    user_longitude = Defibrillator.convert_degrees_to_radians(input().strip())
    user_latitude = Defibrillator.convert_degrees_to_radians(input().strip())

    # On instancie la liste de défibrillateurs
    n = int(input().strip())
    defibrillators = [Defibrillator(input().strip()) for _ in range(n)]
    
    nearest_defibrillator = find_nearest_defibrillator(user_longitude, user_latitude, defibrillators)
    print(nearest_defibrillator.name)

if __name__ == "__main__":
    main()
