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
        for antenna_a in antennas:
            for antenna_b in antennas:
                if antenna_a == antenna_b:
                    continue

                distance = pos_subtract(antenna_a, antenna_b)

                antinode_a = antenna_a
                while True:
                    antinode_a = pos_add(antinode_a, pos_mult((-1, -1), distance))
                    if not map.in_bounds(antinode_a):
                        break
                    map[antinode_a] = "#"
                
                antinode_b = antenna_b
                while True:
                    antinode_b = pos_add(antinode_b, distance)
                    if not map.in_bounds(antinode_b):
                        break
                    map[antinode_b] = "#"


    print(map)
    solution = sum(1 for _ in  find(map, lambda str: str != "."))

    print(solution)


main()