import itertools


def read_input():
    with open("./input/dec1.txt", "r") as f:
        for line in f.readlines():
            yield line


def part_1():
    input = list(map(int, read_input()))

    for pair in itertools.combinations(input, 2):
        if pair[0] + pair[1] == 2020:
            assert 388075 == pair[0] * pair[1]


def part_2():
    input = list(map(int, read_input()))

    for pair in itertools.combinations(input, 3):
        if pair[0] + pair[1] + pair[2] == 2020:
            assert 293450526 == pair[0] * pair[1] * pair[2]
