def blink(stones):

    result = []
    for stone in stones:
        if stone == 0:
            result.append(1)
        elif len(str(stone)) % 2 == 0:
            stone = str(stone)
            split = int(len(stone) / 2)
            result.append(int(stone[0:split]))
            result.append(int(stone[split:]))
        else:
            result.append(stone * 2024)
    return result


def main():
    with open("2024/day11/input") as filestream:
        filedata = filestream.read()
    
    stones = list(int(stone) for stone in filedata.split(" "))
    
    for n in range(25):
        print(n)
        stones = blink(stones)
    
    solution = len(stones)
    print(solution)


main()