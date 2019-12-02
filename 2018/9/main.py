import sys
from llist import dllist
import tqdm

def read_input():
    items = sys.stdin.readline().strip().split()
    return int(items[0]), int(items[-2])

def get_insertion_node(circle, current_node):
    return (current_node.next or circle.first).next

def get_removal_node(circle, current_node):
    for _ in range(7):
        current_node = current_node.prev or circle.last
    return current_node

def get_current_after_removal(circle, node_to_remove):
    if node_to_remove.next is None:
        return circle.first
    return node_to_remove.next

def guess_high_score(player_count, last_marble):
    scores = [0] * player_count
    circle = dllist([0, 1])
    current_node = circle.nodeat(1)
    for current_marble in tqdm.tqdm(range(2, last_marble + 1)):
        current_player = current_marble % player_count
        if current_marble % 23 == 0:
            scores[current_player] += current_marble
            node_to_remove = get_removal_node(circle, current_node)
            current_node = get_current_after_removal(circle, node_to_remove)
            scores[current_player] += circle.remove(node_to_remove)
        else:
            current_node = get_insertion_node(circle, current_node)
            current_node = circle.insert(current_marble, current_node)
    return max(scores)

assert guess_high_score(9, 25) == 32
assert guess_high_score(10, 1618) == 8317
assert guess_high_score(13, 7999) == 146373
assert guess_high_score(17, 1104) == 2764
assert guess_high_score(21, 6111) == 54718
assert guess_high_score(30, 5807) == 37305

def main():
    player_count, last_marble = read_input()
    print(guess_high_score(player_count, last_marble))
    print(guess_high_score(player_count, last_marble * 100))

if __name__ == '__main__':
    main()
