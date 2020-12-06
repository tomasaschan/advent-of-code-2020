import re

with open("input/2015/dec25.txt") as f:
    input = f.read()
    row, col = (int(n) for n in re.findall(r"(\d+)", input))


def n(r, c):
    return sum(range(r + c + 1)) + 1 + c


def code(r, c):
    x = 20151125

    for _ in range(n(r, c) - 1):
        x = (x * 252533) % 33554393

    return x


def part_1_example():
    example = [
        [1, 3, 6, 10, 15, 21],
        [2, 5, 9, 14, 20],
        [4, 8, 13, 19],
        [7, 12, 18],
        [11, 17],
        [16],
    ]

    for r in range(0, 6):
        for c in range(0, 6):
            if r + c > 5:
                continue
            assert example[r][c] == n(r, c)

    assert n(0, 0) == 1

    data = [
        [20151125, 18749137, 17289845, 30943339, 10071777, 33511524],
        [31916031, 21629792, 16929656, 7726640, 15514188, 4041754],
        [16080970, 8057251, 1601130, 7981243, 11661866, 16474243],
        [24592653, 32451966, 21345942, 9380097, 10600672, 31527494],
        [77061, 17552253, 28094349, 6899651, 9250759, 31663883],
        [33071741, 6796745, 25397450, 24659492, 1534922, 27995004],
    ]

    assert code(0, 0) == 20151125
    for r in range(0, 6):
        for c in range(0, 6):
            assert code(r, c) == data[r][c]


def part_1():
    assert code(row - 1, col - 1) == 8997277
