from typing import List, NamedTuple, Set, Tuple
from enum import Enum
from collections import defaultdict
from copy import deepcopy

def ass(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")

class ValidRange(NamedTuple):
    name: str
    ranges: List[Tuple[int, int]]

    def is_valid(self, value):
        return any(l <= value <= r for l, r in self.ranges)


def parse_valid_range(line: str) -> ValidRange:
    name, rest = line.split(':')
    range_strings = [part.split('-') for part in rest.strip().split(' or ')]
    ranges = []
    for l, r in range_strings:
        ranges.append((int(l), int(r)))
    return ValidRange(name=name, ranges=ranges)

ass(ValidRange(name='class', ranges=[(1, 3), (5, 7)]), parse_valid_range, 'class: 1-3 or 5-7')


def find_invalid_values(tickets, ranges):
    result = 0
    for ticket in tickets:
        for x in ticket:
            if not any(r.is_valid(x) for r in ranges):
                result += x
    return result

def filter_out_invalid_tickets(tickets, ranges):
    result = []
    for ticket in tickets:
        result.append(ticket)
        for x in ticket:
            if not any(r.is_valid(x) for r in ranges):
                result.pop()
                break
    return result


TEST_RANGES = [
    ValidRange(name='class', ranges=[(1, 3), (5, 7)]),
    ValidRange(name='row', ranges=[(6, 11), (33, 44)]),
    ValidRange(name='seat', ranges=[(13, 40), (45, 50)]),
]

TEST_TICKETS = [
    [7, 1, 14],
    [7, 3, 47],
    [40, 4, 50],
    [55, 2, 20],
    [38, 6, 12],
]

ass(71, find_invalid_values, TEST_TICKETS, TEST_RANGES)

class Value(NamedTuple):
    value: int
    ticket_idx: int
    field_idx: int

def collate_all_values(tickets):
    result = []
    for ticket_idx, ticket in enumerate(tickets):
        for field_idx, value in enumerate(ticket):
            result.append(Value(value=value, ticket_idx=ticket_idx, field_idx=field_idx))
    return result        

class RangeEvent(Enum):
    START = 0
    END = 1

class RangePoint(NamedTuple):
    value: int
    field_idx: int
    event: RangeEvent

def find_possible_fields(tickets, ranges):
    all_values = collate_all_values(tickets)
    points = [[] for i in range(1000)]
    for field_idx, r in enumerate(ranges):
        for l, r in r.ranges:
            points[l].append(RangePoint(value=l, field_idx=field_idx, event=RangeEvent.START))
            points[r].append(RangePoint(value=r, field_idx=field_idx, event=RangeEvent.END))
    for value in all_values:
        points[value.value].append(value)

    def sorter(value):
        if isinstance(value, Value):
            return 1
        if value.event == RangeEvent.START:
            return 0
        return 2

    for point_collection in points:
        point_collection.sort(key=sorter)

    position_to_possible_fields = {i: {j for j, _ in enumerate(ranges)} for i, _ in enumerate(ranges)}
    current_fields = set()
    for point_collection in points:
        for point in point_collection:
            if isinstance(point, RangePoint):
                if point.event == RangeEvent.START:
                    current_fields.add(point.field_idx)
                else:
                    current_fields.remove(point.field_idx)
            else:
                position_to_possible_fields[point.field_idx] &= current_fields
    return position_to_possible_fields

ass({0: {0, 1}, 1: {0}, 2: {2}}, find_possible_fields, filter_out_invalid_tickets(TEST_TICKETS, TEST_RANGES), TEST_RANGES)

# Returns a map field idx -> position idx
def reconcile_field_assignments(position_to_possible_fields):
    final_assignments = dict()

    ordered_assignments = list(position_to_possible_fields.items())
    ordered_assignments.sort(key=lambda x: len(x[1]))
    for position, possible_fields in ordered_assignments:
        possible_fields = possible_fields - set(final_assignments)
        (field_idx, ) = possible_fields
        final_assignments[field_idx] = position
    return final_assignments

ass({0: 1, 1: 0, 2: 2}, reconcile_field_assignments, {0: {0, 1}, 1: {0}, 2: {2}})

def find_solution(final_assignments, ticket):
    result = 1
    for i in range(6):
        result *= ticket[final_assignments[i]]
    return result


def main():
    tickets = None
    with open('in.txt') as infile:
        tickets = [[int(x) for x in line.strip().split(',')] for line in infile.readlines()]
    ranges = None
    with open('valid_ranges.txt') as infile:
        ranges = [parse_valid_range(line.strip()) for line in infile.readlines()]
    print(find_invalid_values(tickets, ranges))

    own_ticket = tickets[0]
    tickets = filter_out_invalid_tickets(tickets[1:], ranges)
    position_to_possible_fields = find_possible_fields(tickets, ranges)
    final_assignments = reconcile_field_assignments(position_to_possible_fields)
    print(find_solution(final_assignments, own_ticket))



if __name__ == "__main__":
    main()
