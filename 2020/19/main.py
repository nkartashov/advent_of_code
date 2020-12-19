from typing import List, NamedTuple, Set, Tuple, Dict
from enum import Enum
from collections import defaultdict
from copy import deepcopy
from itertools import product
from functools import lru_cache

def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")

def set_sum(args):
    result = set()
    for arg in args:
        result = result | arg
    return result

class MatchContext(NamedTuple):
    rules: Dict[int, 'Rule']
    cache: Dict[int, Set[int]] = dict()

class Rule(NamedTuple):
    alternatives: List['Rule'] = []
    sequence: List['Rule'] = []
    ref_id: int = None
    literal: str = None

    def does_match(self, ctx: MatchContext, expression: str) -> bool:
        return len(expression) in self.match(expression, ctx)

    # Returns a set of indices where the match ended if successful, or empty set
    # otherwise.
    def match(self, expression: str, ctx: MatchContext, start: int = 0) -> Set[int]:
        if self.alternatives:
            return self._match_alternatives(expression, ctx, start)

        if self.sequence:
            return self._match_sequence(expression, ctx, start)

        if self.ref_id is not None:
            return ctx.rules[self.ref_id].match(expression, ctx, start)
        
        if expression[start:].startswith(self.literal):
            return {start + len(self.literal)}

        return set()

    def _match_alternatives(self, expression: str, ctx: MatchContext, start: int) -> Set[int]:
        return set_sum([alt.match(expression, ctx, start) for alt in self.alternatives])

    def _match_sequence(self, expression: str, ctx: MatchContext, start: int) -> Set[int]:
        matches = {start}
        for seq in self.sequence:
            matches = set_sum([seq.match(expression, ctx, match) for match in matches])
        return matches


def parse_rule(rule_string: str) -> Rule:
    rule_id_string, rest = rule_string.split(':')
    rule_id = int(rule_id_string)
    rest = rest.strip()
    alternatives = rest.split('|')
    if len(alternatives) > 1:
        return rule_id, Rule(alternatives=[parse_rule_alternative(alt) for alt in alternatives])
    
    return rule_id, parse_rule_alternative(rest)


def parse_rule_alternative(rule_definition: str) -> Rule:
    sequence = rule_definition.split()
    if len(sequence) > 1:
        return Rule(sequence=[parse_rule_alternative(seq) for seq in sequence])
    
    if rule_definition.startswith('"'):
        return Rule(literal=rule_definition[1:-1])
    return Rule(ref_id=int(rule_definition))

assrt((4, Rule(literal="a")), parse_rule, '4: "a"')

REF_2 = Rule(ref_id=2)
REF_3 = Rule(ref_id=3)

assrt((1, Rule(alternatives=[Rule(sequence=[REF_2, REF_3]), Rule(sequence=[REF_3, REF_2])])), parse_rule, "1: 2 3 | 3 2")

def count_matching(rule: Rule, ctx: MatchContext, expressions: List[str]) -> int:
    return sum([1 for expression in expressions if rule.does_match(ctx, expression)])

def main():
    lines = None
    with open('in.txt') as infile:
        lines = [line.strip() for line in infile.readlines()]
    rules = {}
    with open('rules.txt') as infile:
        for line in infile.readlines():
            rule_id, rule = parse_rule(line.strip())
            rules[rule_id] = rule
    ctx = MatchContext(rules=rules)
    print(count_matching(ctx.rules[0], ctx, lines))


if __name__ == "__main__":
    main()
