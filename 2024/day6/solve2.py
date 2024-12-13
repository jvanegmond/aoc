import time
from typing import List, Tuple

BLANK = "."
GUARD_LEFT = "←"
GUARD_UP = "↑"
GUARD_RIGHT = "→"
GUARD_DOWN = "↓"
GUARD_CHARS = [GUARD_LEFT, GUARD_UP, GUARD_RIGHT, GUARD_DOWN]

OBSTRUCTION = "#"
ADDED_OBSTRUCTION = "O"
OBSTRUCTIONS = [OBSTRUCTION, ADDED_OBSTRUCTION]
VISITED = "X"

def rotate_guard(guard) -> str:
    """Rotate the guard 90 degrees clockwise"""
    if guard == GUARD_UP:
        return GUARD_RIGHT
    elif guard == GUARD_RIGHT:
        return GUARD_DOWN
    elif guard == GUARD_DOWN:
        return GUARD_LEFT
    elif guard == GUARD_LEFT:
        return GUARD_UP

class Puzzle:

    def __init__(self, puzzle):
        # Set guard initial direction
        puzzle = puzzle.replace("^", GUARD_UP)
        # Parse puzzle
        self._puzzle = list(list(line) for line in puzzle.splitlines())

        # Create copy of puzzle to track visited
        puzzle = puzzle.replace(GUARD_UP, BLANK)
        self._visited = list(list(line) for line in puzzle.splitlines())
        
        # Track initial position
        guard, x, y = self.find(GUARD_CHARS)
        self._visited[x][y] = VISITED

        self.iterations = 0
        self.finished = False

    def find(self, chars: List[str]) -> Tuple[str, int, int]:
        for x in range(len(self._puzzle)):
            for y in range(len(self._puzzle[x])):
                char = self._puzzle[x][y]
                if char in chars:
                    return char, x, y
        return -1, -1

    def step(self):
        if self.finished:
            return
        
        self.iterations += 1

        # Look for guard
        guard, x, y = self.find(GUARD_CHARS)

        if guard == GUARD_UP:
            next_x, next_y = x - 1, y
        elif guard == GUARD_DOWN:
            next_x, next_y = x + 1, y
        elif guard == GUARD_LEFT:
            next_x, next_y = x, y - 1
        elif guard == GUARD_RIGHT:
            next_x, next_y = x, y + 1
        
        if next_y < 0 or next_y >= len(self._puzzle) or next_x < 0 or next_x >= len(self._puzzle):
            self.finished = True
            return

        if self._puzzle[next_x][next_y] in OBSTRUCTIONS:
            self._puzzle[x][y] = rotate_guard(guard)
        else:
            self._puzzle[x][y] = BLANK
            self._puzzle[next_x][next_y] = guard
            self._visited[next_x][next_y] = VISITED

    def run_to_completion(self, max_steps=-1):
        self.started = time.time()
        if max_steps == -1:
            while not self.finished:
                self.step()
        else:
            while not self.finished and self.iterations < max_steps:
                self.step()
        self.elapsed = time.time() - self.started
        

    def __str__(self):
        self.elapsed = time.time() - self.started
        result = "Iteration " + str(self.iterations) + "\tElapsed:" + str(self.elapsed) + ":\n"
        for x in range(len(self._puzzle)):
            result += "".join(self._puzzle[x]) + "\t" + "".join(self._visited[x]) + "\n"
        return result


def main():
    with open("2024/day6/input") as filestream:
        filedata = filestream.read()

    # Get visited squares by simulating once
    puzzle = Puzzle(filedata)
    guard, guard_x, guard_y = puzzle.find(GUARD_CHARS)
    puzzle.run_to_completion()
    visited = puzzle._visited
    print(str(puzzle))

    # For each visited square, put an obstruction there and test it
    solution = 0
    evaluated = 0
    size = len(visited)
    for x in range(size):
        for y in range(size):
            if visited[x][y] == VISITED and (x != guard_x or y != guard_y):
                evaluated += 1
                puzzle = Puzzle(filedata)
                puzzle._puzzle[x][y] = ADDED_OBSTRUCTION
                while not puzzle.finished and puzzle.iterations < 15000:
                    puzzle.step()
                if not puzzle.finished:
                    solution += 1
                    print("Solutions", solution, "evaluated", evaluated)

    print("Solutions =", solution)

main()