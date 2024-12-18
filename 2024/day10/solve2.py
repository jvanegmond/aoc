from collections import defaultdict
from typing import Callable, List, Set, Tuple


class Map:
    def __init__(self, mapstr: str):
        self.map = list(list(int(ch) if ch.isdecimal() else -1 for ch in list(line)) for line in mapstr.splitlines())
    
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
        return "\n".join("".join("." if num == -1 else str(num) for num in line) for line in self.map)


def find(map: Map, query: Callable[[str], bool]):
    for x in range(len(map)):
        for y in range(len(map)):
            if query(map[x, y]):
                yield x, y


DIR_UP = -1, 0
DIR_LEFT = 0, -1
DIR_RIGHT = 0, 1
DIR_DOWN = 1, 0


def add(pos, dir):
    return (pos[0] + dir[0], pos[1] + dir[1])


def walk_up(map: Map, pos: Tuple[int, int], result: defaultdict[Tuple[int, int], int]):
    cur_elevation = map[pos]

    for next_step in [add(pos, DIR_UP), add(pos, DIR_LEFT), add(pos, DIR_RIGHT), add(pos, DIR_DOWN)]:
        if not map.in_bounds(next_step):
            continue

        next_elevation = map[next_step] 
        if cur_elevation == 8 and next_elevation == 9:
            result[next_step] += 1

        diff_elevation = next_elevation - cur_elevation
        if diff_elevation == 1 and next_elevation != 9:
            walk_up(map, next_step, result)


def main():
    with open("2024/day10/input") as filestream:
        topographical_layout = filestream.read()
    
    map = Map(topographical_layout)
    trailheads = list(find(map, lambda loc: loc == 0))

    solution = 0
    for trailhead in trailheads:
        results = defaultdict(lambda: 0)
        walk_up(map, trailhead, results)
        
        solution += sum(results.values())
    
    print(solution)


main()