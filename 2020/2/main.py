from typing import NamedTuple, List
from collections import Counter


# assert(find_three_summing_to_target([1, 1, 1], 3) == (1, 1, 1))

def safe_get(l, idx):
    if idx >= len(l):
        return None
    return l[idx]


class PasswordPolicy(NamedTuple):
    letter: str
    low: int
    high: int

    def is_valid(self, password: str) -> bool:
        counts = Counter(password)
        return self.low <= counts.get(self.letter, 0) <= self.high 

    def is_valid_positions(self, password: str) -> bool:
        contains_count = 0
        for pos in (self.low - 1, self.high - 1):
            if safe_get(password, pos) == self.letter:
                contains_count += 1
        return contains_count == 1

def parse_policy(line) -> PasswordPolicy:
        frequencies, letter, password = line.split()
        low, high = (int(f) for f in frequencies.split('-'))
        return PasswordPolicy(letter=letter[:-1], low=low, high=high)

assert(parse_policy("1-3 a: abcde").is_valid_positions("abcde"))

assert(parse_policy("1-3 a: abcde") == PasswordPolicy(letter="a", low=1, high=3))

def parse_policies(lines) -> List[PasswordPolicy]:
    return [parse_policy(line) for line in lines]

def validate_policies(lines, policies: List[PasswordPolicy]) -> int:
    result = 0
    for line, policy in zip(lines, policies):
        _, _, password = line.split()
        if policy.is_valid(password):
            result += 1
    return result

def validate_policies_positions(lines, policies: List[PasswordPolicy]) -> int:
    result = 0
    for line, policy in zip(lines, policies):
        _, _, password = line.split()
        if policy.is_valid_positions(password):
            result += 1
    return result

def main():
    with open('in.txt') as infile:
        lines = [line.strip() for line in infile.readlines()]
        policies = parse_policies(lines)
        print(validate_policies(lines, policies))
        print(validate_policies_positions(lines, policies))


if __name__ == "__main__":
    main()
