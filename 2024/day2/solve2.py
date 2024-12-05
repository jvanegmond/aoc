def yield_lines(file_path: str):
    with open(file_path, 'r') as filestream:
        for line in filestream:
            yield line.strip('\n')

def is_safe(line_numbers):
    # Check for direction and jumps
    direction = line_numbers[0] - line_numbers[1]
    for n in range(len(line_numbers) - 1):
        diff = line_numbers[n] - line_numbers[n + 1]
        
        if diff == 0 or abs(diff) > 3:
            return False
        elif direction < 0 and diff > 0:
            return False
        elif direction > 0 and diff < 0:
            return False

    return True

def main():
    solution = 0

    for line in yield_lines("2024/day2/example"):
        line_numbers = [int(n) for n in line.split(' ')]

        if is_safe(line_numbers):
            solution += 1
        else:
            # Remove one level at a time and check if it is safe
            for n in range(len(line_numbers)):
                one_removed = line_numbers.copy()
                one_removed.pop(n)
                if is_safe(one_removed):
                    solution += 1 
                    break

    print(solution)


main()
