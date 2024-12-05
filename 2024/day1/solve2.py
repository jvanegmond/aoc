def yield_lines(file_path: str):
    with open(file_path, 'r') as filestream:
        for line in filestream:
            yield line.strip('\n')


def main():
    # Parse left and right numbers into easily sortable arrays.
    left_numbers = []
    right_numbers = []
    for line in yield_lines("2024/day1/input"):
        line_numbers = [int(n) for n in line.split('   ')]
        left_numbers.append(line_numbers[0])
        right_numbers.append(line_numbers[1])
    left_numbers.sort()
    right_numbers.sort()

    # Count occurrences of left numbers in right numbers list
    solution = 0
    for i in range(len(left_numbers)):
        similarity = right_numbers.count(left_numbers[i])
        solution += left_numbers[i] * similarity

    print(solution)


main()