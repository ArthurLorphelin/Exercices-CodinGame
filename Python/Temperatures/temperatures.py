# Fonction qui lit les températures et les retourne dans une liste
def get_temperature_list(n):
    return list(map(int, input().split())) if n > 0 else []


# Fonction qui trouve la température la plus proche de zéro
def find_closest_temperature(temperature_list):
    if not temperature_list:
        return 0

    temp_closest_to_zero = temperature_list[0]
    for temp in temperature_list:
        if (abs(temp) < abs(temp_closest_to_zero)) or (
                abs(temp) == abs(temp_closest_to_zero) and temp > temp_closest_to_zero):
            temp_closest_to_zero = temp

    return temp_closest_to_zero


def main():
    n = int(input().strip())
    temperature_list = get_temperature_list(n)
    temp_closest_to_zero = find_closest_temperature(temperature_list)

    # On affiche le résultat
    print(temp_closest_to_zero)


if __name__ == "__main__":
    main()