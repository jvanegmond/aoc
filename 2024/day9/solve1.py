from typing import Callable, List

class Cursor:
    FORWARD = 1
    BACKWARD = -1

    def __init__(self, disk: List[str], direction: int, query: Callable[[str], bool]):
        self.direction = direction
        self.disk = disk
        self.query = query

        if self.direction == Cursor.FORWARD:
            self.cursor = 0
        elif self.direction == Cursor.BACKWARD:
            self.cursor = len(self.disk) - 1

    def _cursor_in_bounds(self) -> bool:
        return self.cursor >= 0 and self.cursor < len(self.disk)

    def _advance_cursor(self) -> None:
        self.cursor += self.direction

    def next(self) -> int:
        while self._cursor_in_bounds():
            cursor_copy = self.cursor
            self._advance_cursor()
            if self.query(self.disk[cursor_copy]):
                return cursor_copy
        return None


def swap(disk: List[str], idxa: int, idxb: int) -> None:
    temp = disk[idxa]
    disk[idxa] = disk[idxb]
    disk[idxb] = temp


def main():
    with open("2024/day9/input") as filestream:
        disk_dense_layout = filestream.read()

    EMPTY_SPACE = "."

    # Convert from disk dense layout to individual blocks
    file_index = 0
    disk_blocks = []
    for idx, disk_space_length in enumerate(list(disk_dense_layout)):
        if idx % 2 == 0:
            disk_blocks += [str(file_index)] * int(disk_space_length)
            file_index += 1
        else:
            disk_blocks += [EMPTY_SPACE] * int(disk_space_length)
    

    # Keep swapping first empty space with last block till ordened
    seek_forward_empty = Cursor(disk_blocks, Cursor.FORWARD, lambda block: block == EMPTY_SPACE)
    seek_backward_occupied = Cursor(disk_blocks, Cursor.BACKWARD, lambda block: block != EMPTY_SPACE)
    while True:
        empty = seek_forward_empty.next()
        occupied = seek_backward_occupied.next()

        # If the first empty slot is beyond the last occupied slot, this means
        # we have completed organized the disk and we are done.
        if empty > occupied:
            break
        
        swap(disk_blocks, empty, occupied)
        

    # Calculate checksum
    checksum = 0
    for idx, block in enumerate(disk_blocks):
        if block == ".":
            continue
        checksum += idx * int(block)


    solution = checksum
    print(solution)


main()