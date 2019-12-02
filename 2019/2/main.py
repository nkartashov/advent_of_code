import copy


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

def guess_input(state, want):
    for noun in range(0, 100):
        for verb in range(0, 100):
            to_test = copy.deepcopy(state)
            to_test[1] = noun
            to_test[2] = verb
            result = eval_program(to_test)[0]
            if result == want:
                return 100 * noun + verb


def main():
    with open('in.txt') as infile:
        state = [int(code) for code in infile.read().strip().split(',')]
        state[1] = 12
        state[2] = 2
        print(eval_program(copy.deepcopy(state))[0])
        print(guess_input(state, 19690720))


if __name__ == "__main__":
    main()
