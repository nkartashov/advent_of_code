


def ass(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")


def eval_program(state):
    counter = 0
    while state[counter] != 99:
        dest = state[counter + 3]
        a = state[state[counter + 1]]
        b = state[state[counter + 2]]
        if state[counter] == 1:
            state[dest] = a + b
        else:
            state[dest] = a * b
        counter += 4
    return state

ass([2,0,0,0,99], eval_program, [1,0,0,0,99])
ass([30,1,1,4,2,5,6,0,99], eval_program, [1,1,1,4,99,5,6,0,99])

def main():
    with open('in.txt') as infile:
        lines = [line.strip() for line in infile.readlines()]
        states = [[int(code) for code in line.split(',')] for line in lines]
        for state in states:
            state[1] = 12
            state[2] = 2
            print(eval_program(state)[0])


if __name__ == "__main__":
    main()
