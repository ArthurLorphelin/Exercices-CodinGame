import sys
import math

# Constantes
MIN_SIZE_LANDING_ZONE = 1000
MAX_HORIZONTAL_SPEED = 20
MAX_VERTICAL_SPEED = 40
MAX_TILT_HIGH = 45
MAX_TILT_LOW = 15
ALTITUDE_THRESHOLD = 1000
ALTITUDE_TO_OBSTACLE_THRESHOLD = 500


# Fonction qui lit et stocke les points de la surface de Mars
def read_input():
    surface_n = int(input())
    return [tuple(map(int, input().split())) for _ in range(surface_n)]


# Fonction qui détecte et retourne les coordonnées de la zone d'atterrissage
def find_landing_zone(surface):
    for index in range(1, len(surface) - 1):
        if surface[index - 1][1] == surface[index][1]:
            start, end, altitude = surface[index - 1][0], surface[index][0], surface[index][1]
            if end - start >= MIN_SIZE_LANDING_ZONE:
                return start, end, altitude


# Fonction qui trouve l'altitude maximale de la surface entre le rover et la zone d'atterrissage
def find_next_highest_obstacle(x_position, landing_zone_start, landing_zone_end, surface):
    return max(
        (y for x, y in surface if min(x_position, landing_zone_end) <= x <= max(x_position, landing_zone_start)),
        default=0
    )


# Fonction qui calcule l'altitude restante du rover
def calculate_rover_altitude(y_position, altitude_landing_zone):
    return y_position - altitude_landing_zone


# Fonction qui ajuste l'angle du rover pour se diriger vers la zone d'atterrissage en fonction de l'altitude
def adjust_rotate_to_reach_landing_zone(y_position, x_position, landing_zone_start, landing_zone_end,
                                        altitude_landing_zone, current_rotate, next_obstacle_altitude):
    rover_altitude = calculate_rover_altitude(y_position, altitude_landing_zone)
    max_tilt = MAX_TILT_LOW if rover_altitude < ALTITUDE_THRESHOLD or (
                next_obstacle_altitude and y_position - next_obstacle_altitude < ALTITUDE_TO_OBSTACLE_THRESHOLD) else MAX_TILT_HIGH

    if x_position < landing_zone_start:
        return max(current_rotate - 15, -max_tilt)
    elif x_position > landing_zone_end:
        return min(current_rotate + 15, max_tilt)
    return current_rotate


# Fonction qui ajuste l'angle pour réduire la vitesse horizontale excessive
def adjust_rotate_opposite_direction(x_position, y_position, altitude_landing_zone, horizontal_speed, current_rotate,
                                     next_obstacle_altitude, landing_zone_start, landing_zone_end):
    rover_altitude = calculate_rover_altitude(y_position, altitude_landing_zone)
    max_tilt = MAX_TILT_LOW if (rover_altitude < ALTITUDE_THRESHOLD or (
                next_obstacle_altitude and next_obstacle_altitude > y_position - ALTITUDE_TO_OBSTACLE_THRESHOLD)) and not (
                landing_zone_start <= x_position <= landing_zone_end) else MAX_TILT_HIGH

    if horizontal_speed > 0:
        return min(current_rotate + 15, max_tilt)
    elif horizontal_speed < 0:
        return max(current_rotate - 15, -max_tilt)
    return current_rotate


# Fonction qui réduit progressivement l'angle de rotation à zero
def adjust_rotate_to_zero(current_rotate):
    return min(current_rotate + 15, 0) if current_rotate < 0 else max(current_rotate - 15,
                                                                      0) if current_rotate > 0 else 0


# Fonction qui calcule la puissance nécessaire pour ralentir la descente en conditions optimales
def compute_power_in_optimal_conditions(vertical_speed):
    return 4 if vertical_speed < -30 else 3 if vertical_speed < -20 else 2 if vertical_speed < -10 else 0


# Fonction qui calcule la puissance en approche finale d'atterrissage
def compute_power_approaching_landing_zone(vertical_speed, current_rotate, y_position, next_obstacle_altitude):
    if y_position - next_obstacle_altitude >= ALTITUDE_TO_OBSTACLE_THRESHOLD:
        return compute_power_in_optimal_conditions(
            vertical_speed) if current_rotate == 0 else 4 if vertical_speed < -20 or abs(current_rotate) > 20 else 3
    return 4


# Fonction qui prédit si le rover va atterrir dans la zone d'atterrissage en fonction de sa trajectoire actuelle
def will_rover_land_in_zone(x_position, y_position, altitude_landing_zone, horizontal_speed, vertical_speed,
                            landing_zone_start, landing_zone_end):
    impact_x = x_position + (
                (y_position - altitude_landing_zone) * math.tan(math.atan2(horizontal_speed, vertical_speed)))
    return landing_zone_start <= impact_x <= landing_zone_end


# Fonction qui vérifie que toutes les conditions d'atterrissage sont réunies
def is_optimal_conditions_to_land(x_position, y_position, altitude_landing_zone, horizontal_speed, vertical_speed,
                                  landing_zone_start, landing_zone_end, current_rotate):
    return will_rover_land_in_zone(x_position, y_position, altitude_landing_zone, horizontal_speed, vertical_speed,
                                   landing_zone_start, landing_zone_end) and current_rotate == 0 and abs(
        horizontal_speed) < MAX_HORIZONTAL_SPEED and abs(vertical_speed) < MAX_VERTICAL_SPEED


# Fonction de la boucle principale du jeu, du contrôle du rover
def control_lander(surface):
    landing_zone_start, landing_zone_end, altitude_landing_zone = find_landing_zone(surface)

    while True:
        x, y, h_speed, v_speed, _, rotate, _ = map(int, input().split())
        next_obstacle_altitude = find_next_highest_obstacle(x, landing_zone_start, landing_zone_end, surface)

        if not (landing_zone_start <= x <= landing_zone_end):
            if abs(h_speed) <= MAX_HORIZONTAL_SPEED:
                rotate = adjust_rotate_to_reach_landing_zone(y, x, landing_zone_start, landing_zone_end,
                                                             altitude_landing_zone, rotate, next_obstacle_altitude)
            elif abs(h_speed) >= 2 * MAX_HORIZONTAL_SPEED:
                rotate = adjust_rotate_opposite_direction(x, y, altitude_landing_zone, h_speed, rotate,
                                                          next_obstacle_altitude, landing_zone_start, landing_zone_end)
            else:
                rotate = adjust_rotate_to_zero(rotate)
            power = compute_power_approaching_landing_zone(v_speed, rotate, y, next_obstacle_altitude)

        else:
            if is_optimal_conditions_to_land(x, y, altitude_landing_zone, h_speed, v_speed, landing_zone_start,
                                             landing_zone_end, rotate):
                rotate, power = 0, compute_power_in_optimal_conditions(v_speed)
            else:
                if abs(h_speed) > MAX_HORIZONTAL_SPEED or (rotate > 0 and h_speed > 0) or (rotate < 0 and h_speed < 0):
                    rotate = adjust_rotate_opposite_direction(x, y, altitude_landing_zone, h_speed, rotate,
                                                              next_obstacle_altitude, landing_zone_start,
                                                              landing_zone_end)
                elif not will_rover_land_in_zone(x, y, altitude_landing_zone, h_speed, v_speed, landing_zone_start,
                                                 landing_zone_end):
                    rotate = adjust_rotate_to_reach_landing_zone(y, x, landing_zone_start, landing_zone_end,
                                                                 altitude_landing_zone, rotate, next_obstacle_altitude)
                elif rotate != 0:
                    rotate = adjust_rotate_to_zero(rotate)
            power = compute_power_approaching_landing_zone(v_speed, rotate, y, next_obstacle_altitude)

        # On affiche la solution
        print(f"{rotate} {power}")


def main():
    surface = read_input()
    control_lander(surface)


if __name__ == "__main__":
    main()