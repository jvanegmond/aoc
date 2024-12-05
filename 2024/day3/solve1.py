import re
from pprint import pprint


def main():
    with open("2024/day3/input") as filestream:
        filedata = filestream.read()
    
    matches = re.findall(r"mul\((\d+),(\d+)\)", filedata)

    solution = 0
    for match in matches:
        solution += int(match[0]) * int(match[1])

    print(solution)


main()