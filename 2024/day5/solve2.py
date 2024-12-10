import re
from functools import cmp_to_key


def main():
    with open("2024/day5/input") as filestream:
        filedata = filestream.read()
    
    parts = filedata.split("\n\n")
    order_rules = re.findall(r"(?:(\d+)\|(\d+))", parts[0])
    puzzles = list(part.split(",") for part in parts[1].splitlines())

    def by_order_rules(item1, item2):
        for rule in order_rules:
            left, right = rule
            if left == item1 and right == item2:
                return -1
            if left == item2 and right == item1:
                return 1
        return 0

    solution = 0
    for puzzle in puzzles:
        puzzle_sorted = sorted(puzzle, key=cmp_to_key(by_order_rules))
        if puzzle != puzzle_sorted:
            middle = puzzle_sorted[int(len(puzzle)/2)]
            solution += int(middle)

    print(solution)


main()