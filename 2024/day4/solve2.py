def yield_lines(file_path: str):
    with open(file_path, 'r') as filestream:
        for line in filestream:
            yield line.strip('\n')


def main():
    lines = list(yield_lines("2024/day4/input"))
    line_len = len(lines)
    
    # Loop through cols and row looking for "A"
    # Avoiding edges as "A" on edges cannot have X-MAS pattern
    solution = 0
    for col in range(1, line_len - 1):
        for row in range(1, line_len - 1):
            # Middle must have A
            if lines[col][row] != "A":
                continue
            if not (\
                # Back diagonal has SAM
                (lines[col-1][row-1] == "S" and \
                lines[col+1][row+1] == "M")
                or \
                # Back diagonal has MAS
                (lines[col-1][row-1] == "M" and \
                lines[col+1][row+1] == "S")
            ):
                continue
            if not (\
                # Forward diagonal has SAM
                (lines[col+1][row-1] == "S" and \
                lines[col-1][row+1] == "M")
                or \
                # Forward diagonal has MAS
                (lines[col+1][row-1] == "M" and \
                lines[col-1][row+1] == "S")
            ):
                continue

            # A in the middle, has SAM/MAS diagonals, must be X-MAS pattern
            solution += 1

    print(solution)

main()