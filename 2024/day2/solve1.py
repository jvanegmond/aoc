from typing import Generator


def yield_lines(file_path: str) -> Generator[str, None, None]:
    with open(file_path, 'r') as filestream:
        for line in filestream:
            yield line.strip('\n')


def main():
    solution = 0

    for line in yield_lines("2024/day2/input"):
        line_numbers = [int(n) for n in line.split(' ')]

        # Check for direction and jumps
        safe = 1
        direction = line_numbers[0] - line_numbers[1]
        for n in range(len(line_numbers) - 1):
            diff = line_numbers[n] - line_numbers[n + 1]
            
            if diff == 0 or abs(diff) > 3:
                safe = 0
            elif direction < 0 and diff > 0:
                safe = 0
            elif direction > 0 and diff < 0:
                safe = 0
        
        solution += safe

    print(solution)


main()