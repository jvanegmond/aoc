from enum import Enum
from typing import Any, List, NamedTuple


EMPTY_SPACE = -1


class LayoutType(Enum):
    FILE = 1
    EMPTY = 2


class DiskLayout(NamedTuple):
    type: LayoutType
    length: int
    value: int

    def __str__(self):
        if self.value == EMPTY_SPACE:
            val = "."
        else:
            val = str(self.value)
        return "".join([val] * self.length)


def swap(disk: List[Any], idxa: int, idxb: int) -> None:
    temp = disk[idxa]
    disk[idxa] = disk[idxb]
    disk[idxb] = temp


def main():
    with open("2024/day9/input") as filestream:
        filedata = filestream.read()

    # Parse dense layout
    file_index = 0
    disk_format: List[DiskLayout] = []
    for empty_idx, empty_block in enumerate(list(filedata)):
        if empty_idx % 2 == 0:
            disk_format.append(DiskLayout(LayoutType.FILE, int(empty_block), file_index))
            file_index += 1
        else:
            disk_format.append(DiskLayout(LayoutType.EMPTY, int(empty_block), EMPTY_SPACE))

    # Keep moving the last file block into the first available empty block
    seek_backward_idx = len(disk_format) - 1
    while True:
        # Search the last file block
        file_idx, file_block = seek_backward_idx, disk_format[seek_backward_idx]
        
        seek_backward_idx -= 1
        if seek_backward_idx == 0:
            break

        if file_block.type != LayoutType.FILE:
            continue
        
        # Search the first available empty block of sufficient size
        # that is to the left of the file
        for empty_idx, empty_block in enumerate(disk_format):
            if empty_idx >= file_idx:
                break

            if empty_block.type == LayoutType.EMPTY and empty_block.length >= file_block.length:
                
                # If they are identical in size, we can simply swap them
                if empty_block.length == file_block.length:
                    swap(disk_format, empty_idx, file_idx)
                else:
                    remainder = empty_block.length - file_block.length

                    # If the empty block is larger than the file, we need to:
                    # - Copy the file into the position of the empty space
                    disk_format[empty_idx] = file_block

                    # - Fill the remaining space (consolidate with next layout, or add a new one)
                    next_layout = disk_format[empty_idx + 1]
                    if next_layout.type == LayoutType.EMPTY:
                        next_layout = DiskLayout(LayoutType.EMPTY, next_layout.length + remainder, EMPTY_SPACE )
                    else:
                        disk_format.insert(empty_idx + 1, DiskLayout(LayoutType.EMPTY, remainder, EMPTY_SPACE))
                        file_idx += 1

                    # - Set the old file position to empty
                    disk_format[file_idx] = DiskLayout(LayoutType.EMPTY, file_block.length, EMPTY_SPACE)
                
                break

    # Convert from disk dense layout to individual blocks
    disk_blocks: List[int] = []
    for empty_block in disk_format:
        disk_blocks += [empty_block.value] * empty_block.length


    # Calculate checksum
    checksum = 0
    for empty_idx, block in enumerate(disk_blocks):
        if block == EMPTY_SPACE:
            continue
        checksum += empty_idx * int(block)


    solution = checksum
    print(solution)


main()