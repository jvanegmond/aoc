from collections import defaultdict


def blink(stones):
    result = defaultdict(int)

    for stone in stones.keys():
        count = stones[stone]
        if stone == 0:
            result[1] += count
        elif len(str(stone)) % 2 == 0:
            stone = str(stone)
            split = int(len(stone) / 2)
            result[int(stone[0:split])] += count
            result[int(stone[split:])] += count
        else:
            result[stone * 2024] += count
    return result


def main():
    with open("2024/day11/input") as filestream:
        filedata = filestream.read()
    
    stones = list(int(stone) for stone in filedata.split(" "))

    counts = defaultdict(int)
    for stone in stones:
        counts[stone] += 1
    
    for n in range(75):
        print(n)
        counts = blink(counts)
    
    solution = sum(counts.values())
    print(solution)


main()