# Fonction qui lit les puissances de chevaux et les retourne dans une liste
def get_horses_power(n):
    horses_power = []
    for _ in range(n):
        pi = int(input().strip())
        horses_power.append(pi)
    return horses_power

# Fonction qui trouve la différence minimale entre les puissance de chevaux
def find_minimum_difference(horses_power):
    horses_power.sort()
    minimum = float('inf')
    for index in range(1, len(horses_power)):
        minimum = min(minimum, horses_power[index] - horses_power[index - 1])
    return minimum

def main():
    n = int(input().strip())
    horses_power = get_horses_power(n)
    minimum = find_minimum_difference(horses_power)

    # On affiche la solution
    print(minimum)


if __name__ == "__main__":
    main()