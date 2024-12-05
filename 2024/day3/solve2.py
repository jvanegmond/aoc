import re
from pprint import pprint


def main():
    with open("2024/day3/input") as filestream:
        filedata = filestream.read()
    
    matches = re.findall(r"(do\(\)|don't\(\)|mul\((\d+),(\d+)\))", filedata)

    solution = 0
    enabled = True
    for match in matches:
        if match[0].startswith("don't"):
            enabled = False
        elif match[0].startswith("do"):
            enabled = True
        elif match[0].startswith("mul") and enabled:
            solution += int(match[1]) * int(match[2])

    print(solution)

main()