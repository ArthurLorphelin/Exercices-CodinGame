import sys

def main():
    n = int(input().strip())
    temperature_list = list(map(int, input().split())) if n > 0 else []

    # On vérifie si la liste est vide
    if not temperature_list:
        print(0)
        return
    
    # On trouve la témpérature la plus proche de 0
    temp_closest_to_zero = temperature_list[0]
    for temp in temperature_list:
        if (abs(temp) < abs(temp_closest_to_zero)) or (abs(temp) == abs(temp_closest_to_zero) and temp > temp_closest_to_zero):
            temp_closest_to_zero = temp

    # On affiche le résultat
    print(temp_closest_to_zero)


if __name__ == "__main__":
    main()
