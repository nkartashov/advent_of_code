from enum import Enum
from typing import NamedTuple


class CommandType(Enum):
    FORWARD = 'forward'
    UP = 'up'
    DOWN = 'down'

class Command(NamedTuple):
    command_type: CommandType
    value: int


def read_commands():
    result = []
    with open('in.txt') as infile:
        for line in infile.readlines():
            t, v = line.strip().split()
            result.append(Command(command_type=CommandType(t), value=int(v)))
    return result

def compute_end(commands):
    depth = 0
    position = 0
    for command in commands:
        if command.command_type == CommandType.DOWN:
            depth += command.value
        if command.command_type == CommandType.UP:
            depth -= command.value
        if command.command_type == CommandType.FORWARD:
            position += command.value
    return depth * position

def compute_end_with_aim(commands):
    aim = 0
    depth = 0
    position = 0
    for command in commands:
        if command.command_type == CommandType.DOWN:
            aim += command.value
        if command.command_type == CommandType.UP:
            aim -= command.value
        if command.command_type == CommandType.FORWARD:
            position += command.value
            depth += aim * command.value
    return depth * position

def main():
    commands = read_commands()
    print(compute_end(commands))
    print(compute_end_with_aim(commands))
    


if __name__ == "__main__":
    main()
