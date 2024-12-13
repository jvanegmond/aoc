from itertools import count
from typing import Callable


class Map:
    def __init__(self, mapstr: str):
        self.map = list(list(line) for line in mapstr.splitlines())
    
    def __len__(self):
        return len(self.map)

    def __getitem__(self, key):
        x, y = key
        return self.map[x][y]

    def __setitem__(self, key, value):
        x, y = key
        self.map[x][y] = value

    def in_bounds(self, key):
        x, y = key
        return x >= 0 and y >= 0 and x < len(self) and y < len(self)
    
    def __str__(self):
        return "\n".join("".join(line) for line in self.map)


def find(map: Map, query: Callable[[str], bool]):
    for x in range(len(map)):
        for y in range(len(map)):
            if query(map[x, y]):
                yield x, y


def pos_op(op, a, b):
    ax, ay = a
    bx, by = b
    return (op(ax, bx), op(ay, by))

def pos_subtract(a, b):
    subtract = lambda a, b: b - a
    return pos_op(subtract, a, b)

def pos_add(a, b):
    add = lambda a, b: a + b
    return pos_op(add, a, b)

def pos_mult(a, b):
    mult = lambda a, b: a * b
    return pos_op(mult, a, b)


def main():
    with open("2024/day8/input") as filestream:
        filedata = filestream.read()

    map = Map(filedata)
    map_antinodes = Map(filedata)

    frequencies = set(map[x, y] for x,y in find(map, lambda str: str != "."))
    dict_antennas = dict((frequency, list(find(map, lambda str: str == frequency))) for frequency in frequencies)

    for frequency, antennas in dict_antennas.items():
        for antenna in antennas:
            for other_antenna in antennas:
                if antenna == other_antenna:
                    continue

                distance = pos_subtract(antenna, other_antenna)
                
                antinode_a = pos_add(antenna, pos_mult((-1, -1), distance))
                if map.in_bounds(antinode_a):
                    map_antinodes[antinode_a] = "#"

                antinode_b = pos_add(other_antenna, distance)
                if map.in_bounds(antinode_b):
                    map_antinodes[antinode_b] = "#"


    print(map_antinodes)
    solution = sum(1 for _ in find(map_antinodes, lambda str: str == "#"))

    print(solution)


main()