from tqdm import trange
from typing import Set, NamedTuple
import sys

class Rule(NamedTuple):
    pattern: str
    result: str

PATTERN_SIZE = 5

class State:
    def __init__(self, *, state, start_idx, rules):
        self._state = state
        self._start_idx = start_idx
        self._rules = rules

    def tick(self):
        result_list = []
        for i in range(-4, len(self)):
            pattern = ''
            if i < 0:
                pattern = ('.' * abs(i)) + self._state[:PATTERN_SIZE + i]
            elif i + PATTERN_SIZE > len(self):
                has_count = len(self) - i
                pattern = self._state[i: i + has_count] + ('.' * (PATTERN_SIZE - has_count))
            else:
                pattern = self._state[i: i + PATTERN_SIZE]
            next_symbol = self._rules.get(pattern, '.')
            result_list += next_symbol
        self._state = ''.join(result_list)
        self._start_idx -= 2

    def sum_plant_idxs(self):
        result = 0
        for i, val in enumerate(self._state, start=self._start_idx):
            if val == '#':
                result += i
        return result

    def __len__(self):
        return len(self._state)

    @property
    def stripped_state(self):
        return self._state.strip('.')

    def dump_state(self):
        print(self.stripped_state)

assert State(
    state='.#....##....#####...#######....#.#..##.',
    start_idx=-3,
    rules={}
).sum_plant_idxs() == 325

def parse_rule(rule_string):
    pattern, result = [item.strip() for item in rule_string.split('=>')]
    return Rule(pattern, result)

assert parse_rule('##.## => .\n') == Rule('##.##', '.')

def read_input():
    lines = sys.stdin.readlines()
    return parse_input(lines)

def parse_input(lines):
    _, state = lines[0].strip().split('initial state: ')
    rules = [parse_rule(line) for line in lines[2:]]
    return State(
        state=state,
        start_idx=0,
        rules={rule.pattern: rule.result for rule in rules if rule.result != '.'}
    )

def run_generations(state, count=20):
    prev = state.sum_plant_idxs()
    for i in trange(count):
        state.tick()
        new_sum = state.sum_plant_idxs()
        print(f'{i}: {new_sum - prev}')
        prev = new_sum
    return state.sum_plant_idxs()


TEST_INPUT = [
    'initial state: #..#.#..##......###...###\n',
    '\n',
    '...## => #\n',
    '..#.. => #\n',
    '.#... => #\n',
    '.#.#. => #\n',
    '.#.## => #\n',
    '.##.. => #\n',
    '.#### => #\n',
    '#.#.# => #\n',
    '#.### => #\n',
    '##.#. => #\n',
    '##.## => #\n',
    '###.. => #\n',
    '###.# => #\n',
    '####. => #\n',
]

TEST_STATE = parse_input(TEST_INPUT)
result = run_generations(TEST_STATE)
assert TEST_STATE.stripped_state == '#....##....#####...#######....#.#..##'
assert result == 325

def main():
    state = read_input()
    print(run_generations(state, count=50_000_000_000))
    print(2850000002454)

if __name__ == '__main__':
    main()


