import sys
import math

MIN_SIZE_LANDING_ZONE = 1000
MAX_HORIZONTAL_SPEED = 20
MAX_VERTICAL_SPEED = 40
MAX_TILT_HIGH = 45
MAX_TILT_LOW = 15
ALTITUDE_THRESHOLD = 1000
ALTITUDE_TO_OBSTACLE_THRESHOLD = 500


# Fonction qui trouve l'altitude maximale de la surface entre le rover et la zone d'atterrissage
def find_next_highest_obstacle(x_position, landing_zone_start, landing_zone_end, surface):
    highest_obstacle_altitude = 0
    for x_obstacle, y_obstacle in surface:
        if min(x_position, landing_zone_end) <= x_obstacle <= max(x_position, landing_zone_start):
            highest_obstacle_altitude = max(highest_obstacle_altitude, y_obstacle)
    return highest_obstacle_altitude

# Fonction qui regarde si le rover est au-dessus de la zone d'atterrissage
def is_rover_above_landing_zone(x_position, landing_zone_start, landing_zone_end):
    return landing_zone_start <= x_position <= landing_zone_end

# Fonction qui regarde si le rover est à gauche de la zone d'atterrissage
def is_rover_to_the_left_of_landing_zone(x_position, landing_zone_start):
    return x_position < landing_zone_start

# Fonction qui regarde si le rover est à droite de la zone d'atterrissage
def is_rover_to_the_right_of_landing_zone(x_position, landing_zone_end):
    return x_position > landing_zone_end

# Fonction qui calcule l'altitude restante
def calculate_rover_altitude(y_position, altitude_landing_zone):
    return y_position - altitude_landing_zone

# Fonction pour ajuster l'angle et se diriger vers la zone d'atterrissage en fonction de l'altitude
def adjust_rotate_to_reach_landing_zone(y_position, x_position, landing_zone_start, landing_zone_end, altitude_landing_zone, current_rotate, next_obstacle_altitude):
    rover_altitude = calculate_rover_altitude(y_position, altitude_landing_zone)
    max_tilt = 0
    if rover_altitude < ALTITUDE_THRESHOLD or (next_obstacle_altitude != 0 and y_position - next_obstacle_altitude  < ALTITUDE_TO_OBSTACLE_THRESHOLD):
        max_tilt = MAX_TILT_LOW
    else:
        max_tilt = MAX_TILT_HIGH
    if is_rover_to_the_left_of_landing_zone(x_position, landing_zone_start):
        return max(current_rotate - 15, -max_tilt)
    elif is_rover_to_the_right_of_landing_zone(x_position, landing_zone_end):
        return min(current_rotate + 15, max_tilt)
    else:
        return current_rotate

# Fonction qui calcule l'angle de direction actuel du rover
def calculate_current_angle_radian(horizontal_speed, vertical_speed):
    return math.atan2(horizontal_speed, vertical_speed)

# Fonction qui calcule le point d'impact actuel du rover si les données ne change pas
def find_impact_point_x_coordonates(x_position, y_position, altitude_landing_zone, horizontal_speed, vertical_speed):
    current_angle = calculate_current_angle_radian(horizontal_speed, vertical_speed)
    return x_position + ((y_position - altitude_landing_zone) * math.tan(current_angle))

# Fonction qui regarde si le rover peut atterrir dans la zone d'atterrissage une fois au-dessus de celle-ci
def will_rover_land_in_zone(x_position, y_position, altitude_landing_zone, horizontal_speed, vertical_speed, landing_zone_start, landing_zone_end):
    x_impact_point = find_impact_point_x_coordonates(x_position, y_position, altitude_landing_zone, horizontal_speed, vertical_speed)
    return landing_zone_start <= x_impact_point <= landing_zone_end

# Fonction qui regarde si toutes les conditions d'atterrissage sont réunies
def is_optimal_conditions_to_land(x_position, y_position, altitude_landing_zone, horizontal_speed, vertical_speed, landing_zone_start, landing_zone_end, current_rotate):
    is_good_trajectory = will_rover_land_in_zone(x_position, y_position, altitude_landing_zone, horizontal_speed, vertical_speed, landing_zone_start, landing_zone_end)
    return is_good_trajectory and current_rotate == 0 and abs(horizontal_speed) < MAX_HORIZONTAL_SPEED and abs(vertical_speed) < MAX_VERTICAL_SPEED

# Fonction pour ajuster le rotate du rover afin d'avoir une vitesse inférieure à 20m/s
def adjust_rotate_opposite_direction(x_position, y_position, altitude_landing_zone, horizontal_speed, current_rotate, next_obstacle_altitude, landing_zone_start, landing_zone_end):
    rover_altitude = calculate_rover_altitude(y_position, altitude_landing_zone)
    max_tilt = 0
    if (rover_altitude < ALTITUDE_THRESHOLD or (next_obstacle_altitude != 0 and next_obstacle_altitude > y_position - ALTITUDE_TO_OBSTACLE_THRESHOLD)) and not is_rover_above_landing_zone(x_position, landing_zone_start, landing_zone_end):
        max_tilt = MAX_TILT_LOW
    else:
        max_tilt = MAX_TILT_HIGH
    if horizontal_speed > 0:
        return min(current_rotate + 15, max_tilt)
    elif horizontal_speed < 0:
        return max(current_rotate - 15, -max_tilt)
    else:
        return current_rotate

# Fonction pour ajuster le rotate du rover à 0 au-dessus de la zone d'atterrissage
def adjust_rotate_to_zero(current_rotate):
    if current_rotate < 0:
        return min(current_rotate + 15, 0)
    elif current_rotate > 0:
        return max(current_rotate - 15, 0)
    else:
        return 0

# Fonction qui calcule le power lorsque le rover est en position optimale pour atterrir
def compute_power_in_optimal_conditions(vertical_speed):
    if vertical_speed < -30:
        return 4
    elif vertical_speed < -20:
        return 3
    elif vertical_speed < -10:
        return 2
    else:
        return 0

# Fonction qui calcule le power en approche finale d'atterrissage
def compute_power_approaching_landing_zone(vertical_speed, current_rotate, y_position, next_obstacle_altitude):
    if y_position - next_obstacle_altitude >= ALTITUDE_TO_OBSTACLE_THRESHOLD:
        if current_rotate == 0:
            return compute_power_in_optimal_conditions(vertical_speed)
        else:
            if vertical_speed < -20 or abs(current_rotate) > 20:
                return 4
            else: 
                return 3
    else : 
        return 4

def main():
    # Lecture des points de la surface de Mars
    surface_n = int(input())  # Nombre de points formant la surface
    surface = []
    for _ in range(surface_n):
        land_x, land_y = map(int, input().split())
        surface.append((land_x, land_y))  # Stockage des coordonnées de la surface

    # Recherche de la zone d'atterrissage
    landing_zone_start = None
    landing_zone_end = None
    altitude_landing_zone = None
    for index in range(1, surface_n - 1):
        # On vérifie si les points sont dans une zone plane
        if surface[index-1][1] == surface[index][1]:
            landing_zone_start = surface[index-1][0]
            landing_zone_end = surface[index][0]
            altitude_landing_zone = surface[index][1]
            # Si la zone d'atterrissage est suffisamment grande, on sort de la boucle
            if landing_zone_end - landing_zone_start >= MIN_SIZE_LANDING_ZONE:
                break

    # Boucle du jeu
    while True:
        x, y, h_speed, v_speed, fuel, rotate, power = map(int, input().split())

        # On regarde quel est le prochain obstacle
        next_obstacle_altitude = find_next_highest_obstacle(x, landing_zone_start, landing_zone_end, surface)

        # Si le rover n'est pas au-dessus de la zone d'atterrissage
        if not is_rover_above_landing_zone(x, landing_zone_start, landing_zone_end):
            if abs(h_speed) <= MAX_HORIZONTAL_SPEED:
                rotate = adjust_rotate_to_reach_landing_zone(y, x, landing_zone_start, landing_zone_end, altitude_landing_zone, rotate, next_obstacle_altitude)
            elif abs(h_speed) >= 2 * MAX_HORIZONTAL_SPEED:
                rotate = adjust_rotate_opposite_direction(x, y, altitude_landing_zone, h_speed, rotate, next_obstacle_altitude, landing_zone_start, landing_zone_end)
            else:
                rotate = adjust_rotate_to_zero(rotate)
            power = compute_power_approaching_landing_zone(v_speed, rotate, y, next_obstacle_altitude)
        
        else: 
            # Si rotate vaut 0, que le rover va atterrir dans les conditions actuelles et que la vitesse horizontale est inférieure à 20m/s
            if is_optimal_conditions_to_land(x, y, altitude_landing_zone, h_speed, v_speed, landing_zone_start, landing_zone_end, rotate):
                rotate = 0
                power = compute_power_in_optimal_conditions(v_speed)

            else:
                # Si la vitesse est supérieure à 20m/s ou dans la direction opposée de la poussée
                if abs(h_speed) > MAX_HORIZONTAL_SPEED or (rotate > 0 and h_speed > 0) or (rotate < 0 and h_speed < 0):
                    rotate = adjust_rotate_opposite_direction(x,y, altitude_landing_zone, h_speed, rotate, next_obstacle_altitude, landing_zone_start, landing_zone_end)

                # Si le rover va sortir de la zone d'atterrissage s'il continue sa trajectoire
                elif not will_rover_land_in_zone(x, y, altitude_landing_zone, h_speed, v_speed, landing_zone_start, landing_zone_end):
                    rotate = adjust_rotate_to_reach_landing_zone(y, x, landing_zone_start, landing_zone_end, altitude_landing_zone, rotate, next_obstacle_altitude)

                # Si l'angle de rotation est différent de 0
                elif rotate != 0:
                    rotate = adjust_rotate_to_zero(rotate)

            power = compute_power_approaching_landing_zone(v_speed, rotate, y, next_obstacle_altitude)

        # On affiche la solution : rotate power
        solution = f"{rotate} {power}"
        print(solution)


if __name__ == "__main__":
    main()
