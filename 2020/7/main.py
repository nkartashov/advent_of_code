from typing import List, NamedTuple
from collections import defaultdict

BAG = " bag"
BAGS = " bags"
CONTAIN = "contain"
NO_OTHER_BAGS = "no other bags" 
SHINY_GOLD = 'shiny gold'

def parse_bag_color_string(color_string):
    color_string = color_string.strip()
    if color_string.endswith(BAG):
        return color_string[:-len(BAG)]
    return color_string[:-len(BAGS)]

assert(parse_bag_color_string("dark olive bag") == "dark olive")
assert(parse_bag_color_string("dark orange bags") == "dark orange")
assert(parse_bag_color_string("dark orange bags ") == "dark orange")

def parse_numbered_bag_string(s):
    count_string, rest = s.split(' ', 1)
    count = int(count_string)
    return (count, parse_bag_color_string(rest))

assert(parse_numbered_bag_string("2 vibrant plum bags") == (2, 'vibrant plum'))
assert(parse_numbered_bag_string("1 shiny gold bag") == (1, 'shiny gold'))


def parse_children_bag_strings(children_string):
    if children_string == NO_OTHER_BAGS:
        return []
    return [parse_numbered_bag_string(child_string.strip()) for child_string in children_string.split(',')]

assert(parse_children_bag_strings("1 dark olive bag, 2 vibrant plum bags") == [(1, "dark olive"), (2, 'vibrant plum')])
assert(parse_children_bag_strings("1 shiny gold bag") == [(1, "shiny gold")])
assert(parse_children_bag_strings("no other bags") == [])


def parse_bag_rule(rule):
    parent_string, children_string = rule.split(CONTAIN)
    # Remove the full stop.
    children_string = children_string[:-1]
    return (parse_bag_color_string(parent_string.strip()), parse_children_bag_strings(children_string.strip())) 

assert(parse_bag_rule('light red bags contain 1 bright white bag, 2 muted yellow bags.') == (
    'light red', [(1, 'bright white'), (2, 'muted yellow')]
))
assert(parse_bag_rule('bright white bags contain 1 shiny gold bag.') == (
    'bright white', [(1, 'shiny gold')]
))
assert(parse_bag_rule('dotted black bags contain no other bags.') == (
    'dotted black', []
))

def parse_bag_rules(lines):
    return [parse_bag_rule(line) for line in lines]

def setup_traversal(bag_rules):
    reverse_nodes = defaultdict(list)
    for parent, children in bag_rules:
        for _, child_color in children:
            reverse_nodes[child_color].append(parent)
    return reverse_nodes

def traverse_nodes(reverse_nodes):
    visited = set()
    return sum(traverse_helper(child, reverse_nodes, visited) for child in reverse_nodes[SHINY_GOLD])

def traverse_helper(current, reverse_nodes, visited):
    if current in visited:
        return 0
    visited.add(current)
    return 1 + sum(traverse_helper(child, reverse_nodes, visited) for child in reverse_nodes[current])


TEST_LINES = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.""".split('\n')

assert(traverse_nodes(setup_traversal(parse_bag_rules(TEST_LINES))) == 4)


def main():
    with open('in.txt') as infile:
        lines = [line.strip() for line in infile.readlines()]
        bag_rules = parse_bag_rules(lines)
        print(traverse_nodes(setup_traversal(bag_rules)))


if __name__ == "__main__":
    main()
