from typing import Callable, List, NamedTuple, Tuple
from collections import namedtuple

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


DIR_UP = -1, 0
DIR_LEFT = 0, -1
DIR_RIGHT = 0, 1
DIR_DOWN = 1, 0

DIRECTIONS = [DIR_UP, DIR_LEFT, DIR_RIGHT, DIR_DOWN]

def add(pos, dir):
    return (pos[0] + dir[0], pos[1] + dir[1])


OCCUPIED = "#"

class GardenPlot:
    map: Map
    plant: str
    coordinates: List[Tuple[int, int]] = []

    def __init__(self, map: Map, plant: str, pos: Tuple[int, int]):
        self.map = map
        self.plant = plant
        self.coordinates = []
        self._floodfill(pos)
        
    def _floodfill(self, pos):
        if not self.map.in_bounds(pos):
            return
        if self.map[pos] != self.plant:
            return
        
        self.map[pos] = OCCUPIED
        self.coordinates.append(pos)

        for dir in DIRECTIONS:
            self._floodfill(add(pos, dir))

    def is_adjacent_to(self, pos: Tuple[int, int]):
        for coord in self.coordinates:
            if coord in [add(pos, dir) for dir in DIRECTIONS]:
                return True
        return False
    
    def get_area(self):
        return len(self.coordinates)
    
    def get_perimeter(self):
        result = 0
        for coord in self.coordinates:
            for dir in DIRECTIONS:
                check = add(coord, dir)
                if not self.map.in_bounds(check) or self.map[check] != self.plant:
                    result += 1
        return result
    
    def __str__(self):
        return f"{self.plant} = {self.coordinates}"


def main():
    with open("2024/day12/input") as filestream:
        filedata = filestream.read()

    map = Map(filedata)

    # Divide the map into contiguous plant areas
    garden_plots: List[GardenPlot] = []
    for x in range(len(map)):
        for y in range(len(map)):
            # Creating the garden plot flood fills the map and marks occupied plants as #
            plant = map[x, y]
            if plant == OCCUPIED:
                continue
            
            garden_plots.append(GardenPlot(map, plant, (x, y)))
    
    # During division, the map was marked as OCCUPIED, revert it back to plants
    for plots in garden_plots:
        for pos in plots.coordinates:
            map[pos] = plots.plant

    solution = 0
    n = 0
    for plots in garden_plots:
        area = plots.get_area()
        perimeter = plots.get_perimeter()
        print(plots.plant, area, perimeter)
        solution += area * perimeter

        n += 1
    
    print(map)
            
    

    print(solution)



main()