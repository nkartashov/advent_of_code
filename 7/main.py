import sys
from collections import defaultdict, deque
from sortedcontainers import SortedList, SortedSet



def get_steps():
    enabled_by = defaultdict(set)
    required_for = defaultdict(set)
    for line in sys.stdin:
        left = line[len('Step ')]
        right = line[len('Step C must be finished before step ')]
        enabled_by[left].add(right)
        required_for[right].add(left)
    return enabled_by, required_for 

def find_starting_tasks(required_for):
    result = []
    for dependants in required_for.values():
        for dependant in dependants:
            if len(required_for.get(dependant, [])) == 0:
                result.append(dependant)
    return result

def traverse_in_order(enabled_by, required_for):
    to_visit = SortedSet(find_starting_tasks(required_for))
    result = []
    while to_visit:
        node = to_visit[0]
        del to_visit[0]
        result.append(node)
        new_available = update_dependencies(node, enabled_by, required_for)
        for new_node in new_available:
            to_visit.add(new_node)
    return ''.join(result)

def update_dependencies(node, enabled_by, required_for):
    new_available = []
    for enabled_node in enabled_by.get(node, []):
        required_for[enabled_node].remove(node)
        if len(required_for[enabled_node]) == 0:
            new_available.append(enabled_node)
    return new_available 

def update_earliest_starts(node, task_finishes, enabled_by, earliest_start):
    for enabled_node in enabled_by.get(node, []):
        earliest_start[enabled_node] = max(earliest_start[enabled_node], task_finishes)

def traverse_with_multiple_workers(
    enabled_by, required_for, worker_count=5, task_cost=60
):
    time = 0
    worker_available = SortedList([0] * worker_count)
    earliest_start = defaultdict(int)
    to_visit = SortedSet((0, task) for task in find_starting_tasks(required_for))
    global_finish_time = 0
    while to_visit:
        task_available, node = to_visit[0]
        del to_visit[0]
        time = max(task_available, worker_available[0])
        task_finishes = time + task_cost + ord(node) - ord('A') + 1
        global_finish_time = max(global_finish_time, task_finishes)
        new_available = update_dependencies(node, enabled_by, required_for)
        update_earliest_starts(node, task_finishes, enabled_by, earliest_start)
        for new_node in new_available:
            to_visit.add((earliest_start[new_node], new_node))
        worker_available.pop(0)
        worker_available.add(task_finishes)

    return global_finish_time

assert traverse_in_order({
    'C': ['A', 'F'],
    'A': ['B', 'D'],
    'B': ['E'],
    'D': ['E'],
    'F': ['E'],
    }, {
    'A': ['C'],
    'B': ['A'],
    'D': ['A'],
    'F': ['C'],
    'E': ['B', 'D', 'F'],
}) == 'CABDFE' 

assert traverse_with_multiple_workers({
    'C': ['A', 'F'],
    'A': ['B', 'D'],
    'B': ['E'],
    'D': ['E'],
    'F': ['E'],
    }, {
    'A': ['C'],
    'B': ['A'],
    'D': ['A'],
    'F': ['C'],
    'E': ['B', 'D', 'F'],
}, 2, 0) == 15

def main():
    steps = get_steps()
    # print(traverse_in_order(*steps))
    print(traverse_with_multiple_workers(*steps))

if __name__ == '__main__':
    main()
