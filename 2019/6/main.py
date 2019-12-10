from typing import NamedTuple, List, Optional
from copy import deepcopy

def ass(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")

class Node(NamedTuple):
    name: str
    # xD
    m_parent: List['Node']
    children: List['Node']

    @property
    def parent(self):
        # T_T
        return self.m_parent[0]

def build_nodes(orbits):
    nodes = dict()
    for parent, child in orbits:
        if parent not in nodes:
            nodes[parent] = Node(name=parent, m_parent=[None], children=[])
        if child not in nodes:
            nodes[child] = Node(name=child, m_parent=[None], children=[])
        nodes[child].m_parent[0] = nodes[parent]
        nodes[parent].children.append(nodes[child])
    return {name for name, n in nodes.items() if n.parent is None}, nodes


def traverse(root: Node, visited=set(), depth=0):
    if root.name in visited:
        print('One planet orbits multiple')
    visited.add(root.name)
    result = depth
    for child in root.children:
        result += traverse(child, visited, depth + 1)
    return result

def find_path_to_root(node: Node):
    result = []
    while node.parent is not None:
        result.append(node.parent.name)
        node = node.parent
    return list(reversed(result))

def tree_distance(node1: Node, node2: Node):
    path_to_root1 = find_path_to_root(node1)
    path_to_root2 = find_path_to_root(node2)
    i = 0
    while i < min(len(path_to_root1), len(path_to_root2)):
        if path_to_root1[i] != path_to_root2[i]:
            break
        i += 1
    return len(path_to_root1) - i + len(path_to_root2) - i
        

def main():
    with open('in.txt') as infile:
        orbits = [line.strip().split(')') for line in infile.readlines()]
        sources, nodes = build_nodes(orbits)
        print(sum(traverse(nodes[source]) for source in sources))
        print(tree_distance(nodes['YOU'], nodes['SAN']))


if __name__ == "__main__":
    main()
