from typing import List, NamedTuple, Tuple, Dict
from enum import Enum

from copy import deepcopy


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")


class File(NamedTuple):
    name: str
    size: int
    is_directory: bool
    children: Dict[str, "File"]

    def __eq__(self, other: "File") -> bool:
        return (
            self.name == other.name
            and self.size == other.size
            and self.children == other.children
        )

    @property
    def total_size(self: "File") -> int:
        if not self.is_directory:
            return self.size
        return sum(ch.total_size for ch in self.children.values())


PROMPT = "$ "
CD = "cd"
LS = "ls"
UP = ".."
ROOT = "/"
DIR = "dir"

MAX_SIZE = 100000


def parse_tree(lines: List[str]) -> File:
    root = File(name=ROOT, size=0, is_directory=True, children={})
    stack = [root]
    i = 0
    while i < len(lines):
        assert lines[i].startswith(PROMPT)
        line = lines[i][len(PROMPT) :]
        if line.startswith(CD):
            dir_name = line.split()[1]
            if dir_name == UP:
                stack.pop()
            elif dir_name == ROOT:
                stack = stack[:1]
            else:
                assert dir_name in stack[-1].children
                stack.append(stack[-1].children[dir_name])
            i += 1
            continue

        assert line.startswith(LS)
        assert stack
        i += 1
        while i < len(lines) and not lines[i].startswith(PROMPT):
            child_line = lines[i]
            parts = child_line.split()
            is_dir = parts[0] == DIR
            stack[-1].children[parts[1]] = File(
                name=parts[1],
                size=int(parts[0]) if not is_dir else 0,
                is_directory=is_dir,
                children={},
            )
            i += 1

    return root


def solve1(lines: List[str]) -> int:
    root = parse_tree(lines)
    result = [0]

    def go(node: File) -> int:
        if not node.is_directory:
            return node.size

        total_size = 0
        for ch in node.children.values():
            total_size += go(ch)

        if total_size < MAX_SIZE:
            result[0] += total_size

        return total_size

    go(root)
    return result[0]


TEST_LINES = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k""".split(
    "\n"
)

assrt(95437, solve1, TEST_LINES)

TOTAL_SIZE = 70000000
NEED_SIZE = 30000000


def solve2(lines: List[str]) -> int:
    root = parse_tree(lines)
    used_size = root.total_size
    result = [used_size]
    free = TOTAL_SIZE - used_size
    assert free < NEED_SIZE
    min_size = NEED_SIZE - free

    def go(node: File) -> int:
        if not node.is_directory:
            return node.size

        total_size = 0
        for ch in node.children.values():
            total_size += go(ch)

        if total_size >= min_size:
            result[0] = min(result[0], total_size)

        return total_size

    go(root)
    return result[0]


assrt(24933642, solve2, TEST_LINES)


def main():
    with open("in.txt") as infile:
        lines = [line.strip() for line in infile.readlines()]
        print(solve1(lines))
        print(solve2(lines))


if __name__ == "__main__":
    main()
