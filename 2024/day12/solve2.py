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
    
    def get_bounding_box(self):
        min_x, min_y, max_x, max_y = 10000, 10000, 0, 0
        for coord in self.coordinates:
            x, y = coord
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
        return min_x, max_x, min_y, max_y
            
    
    def get_perimeter(self):
        # The perimeter cost is simply the amount of corners
        num_corners = 0
        min_x, max_x, min_y, max_y = self.get_bounding_box()
        for x in range(min_x - 1, max_x + 1):
            for y in range(min_y - 1, max_y + 1):
                for straight_pattern in CORNER_PATTERNS:
                    if is_area_pattern_match(self, (x, y), straight_pattern):
                        num_corners += 1

        
        return num_corners
    
    def __str__(self):
        return f"{self.plant} = {self.coordinates}"

PATTERN_NOT_PLANT = "#"
PATTERN_PLANT = "%"
PATTERN_IGNORE = "?"

CORNER_PATTERNS = [
    # Outer corners
    [[PATTERN_PLANT, PATTERN_NOT_PLANT],[PATTERN_NOT_PLANT, PATTERN_NOT_PLANT]],
    [[PATTERN_NOT_PLANT, PATTERN_PLANT],[PATTERN_NOT_PLANT, PATTERN_NOT_PLANT]],
    [[PATTERN_NOT_PLANT, PATTERN_NOT_PLANT],[PATTERN_PLANT, PATTERN_NOT_PLANT]],
    [[PATTERN_NOT_PLANT, PATTERN_NOT_PLANT],[PATTERN_NOT_PLANT, PATTERN_PLANT]],
    # Inner corners
    [[PATTERN_NOT_PLANT, PATTERN_PLANT],[PATTERN_PLANT, PATTERN_IGNORE]],
    [[PATTERN_PLANT, PATTERN_NOT_PLANT],[PATTERN_IGNORE, PATTERN_PLANT]],
    [[PATTERN_PLANT, PATTERN_IGNORE],[PATTERN_NOT_PLANT, PATTERN_PLANT]],
    [[PATTERN_IGNORE, PATTERN_PLANT],[PATTERN_PLANT, PATTERN_NOT_PLANT]],
]


def is_area_pattern_match(plot: GardenPlot, pos, pattern):
    x, y = pos
    plen = len(pattern)
    for px in range(plen):
        for py in range(plen):
            coord = (x + px, y + py)
            if not plot.map.in_bounds(coord):
                tile = OCCUPIED
            elif coord not in plot.coordinates:
                tile = OCCUPIED
            else:
                tile = plot.map[coord]

            if pattern[px][py] != PATTERN_IGNORE and \
               (pattern[px][py] == PATTERN_NOT_PLANT and tile == plot.plant) or \
               (pattern[px][py] == PATTERN_PLANT and tile != plot.plant):
                return False
    return True


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
    for plots in garden_plots:
        area = plots.get_area()
        perimeter = plots.get_perimeter()
        print("A region of", plots.plant, "plants with price", area, "*", perimeter)
        solution += area * perimeter
    
    print(map)

    print(solution)
    # Not 811853


main()