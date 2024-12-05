def yield_lines(file_path: str):
    with open(file_path, 'r') as filestream:
        for line in filestream:
            yield line.strip('\n')


def yield_horizontal_characters(lines):
    for line in lines:
        yield list(line)


def yield_vertical_characters(lines):
    line_length = len(lines[0])
    for n in range(line_length):
        yield [line[n] for line in lines]


def yield_diagonal_characters(lines):
    # This only works when line length and number of lines is identical
    line_len = len(lines)

    # Look first for "/ forward"-diagonals, start at column -line_len and seek down + right
    for start_col in range(-1 * line_len, line_len, 1):
        diagonal = []
        for n in range(line_len):
            row_num = n
            col_num = start_col + n
            if row_num < 0 or row_num >= line_len or col_num < 0 or col_num >= line_len:
                continue
            diagonal.append(lines[row_num][col_num])
        if len(diagonal) >= 4: # May contain XMAS
            yield diagonal
    
    # Then "\ back"-diagonals, start at column 0 and seek down + left
    for start_col in range(0, line_len * 2, 1):
        diagonal = []
        for n in range(0, -1 * line_len, -1):
            row_num = -1 * n
            col_num = start_col + n
            if row_num < 0 or row_num >= line_len or col_num < 0 or col_num >= line_len:
                continue
            diagonal.append(lines[row_num][col_num])
        if len(diagonal) >= 4: # May contain XMAS
            yield diagonal


def yield_characters(lines):
    for horizontal in yield_horizontal_characters(lines):
        yield horizontal
    
    for vertical in yield_vertical_characters(lines):
        yield vertical
    
    for diagonal in yield_diagonal_characters(lines):
        yield diagonal


def main():
    file_lines = list(yield_lines("2024/day4/input"))

    # Get all horizontal, vertical and diagonal lines
    puzzle_lines = yield_characters(file_lines)

    # Count occurences of XMAS and backwards SAMX
    solution = 0
    for line in puzzle_lines:
        line = "".join(line)
        solution += line.count("XMAS") + line.count("SAMX")

    print(solution)

main()