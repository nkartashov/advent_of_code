

import math







def fuel(mass):
    return math.floor(mass / 3) - 2

def total_fuel(mass):
    result = 0
    while True:
        add_fuel = fuel(mass)
        if add_fuel <= 0:
            break
        result += add_fuel
        mass = add_fuel
    return result

def main():
    with open('in.txt') as infile:
        values = [int(line.strip()) for line in infile.readlines()]
        results = [total_fuel(mass) for mass in values]
        print(sum(results))


if __name__ == "__main__":
    main()
