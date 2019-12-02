import sys

from typing import NamedTuple, List

class TreeNode(NamedTuple):
    children: List['TreeNode']
    metadata: List[int]

    def get_value(self):
        if not self.children:
            return sum(self.metadata)
        return sum(self.children[meta - 1].get_value() for meta in self.metadata if (meta - 1) < len(self.children))

def tree_reader_helper(values, start=0):
    child_count = values[start]
    metadata_count = values[start + 1]
    start += 2
    children = []
    for _ in range(child_count):
        child, start = tree_reader_helper(values, start)
        children.append(child)
    return TreeNode(children, values[start: start + metadata_count]), start + metadata_count

def read_tree():
    values = list(map(int, sys.stdin.readline().strip().split()))
    result, _ = tree_reader_helper(values)
    return result

def sum_metadata(tree_node):
    result = sum(tree_node.metadata)
    for child in tree_node.children:
        result += sum_metadata(child)
    return result

assert sum_metadata(tree_reader_helper([
    2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2
])[0]) == 138

def main():
    tree_node = read_tree()
    print(sum_metadata(tree_node))
    print(tree_node.get_value())

if __name__ == '__main__':
    main()
