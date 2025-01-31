# Fonction qui retourne la montagne la plus haute et son index
def get_max_height_index():
    mountain_max_h = 0
    mountain_max_index = 0

    for index in range(8):
        mountain_h = int(input().strip())
        if mountain_h > mountain_max_h:
            mountain_max_h = mountain_h
            mountain_max_index = index
    return mountain_max_index

def main():
    while True:
        mountain_max_index = get_max_height_index()
        print(mountain_max_index)


if __name__ == "__main__":
    main()