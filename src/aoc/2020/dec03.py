def read_map():
    height = 0
    width = 0

    map = dict()

    with open("input/2020/dec03.txt", "r") as f:
        for y, line in enumerate(f.readlines()):
            y = int(y)
            height = max(height, y)
            for x, c in enumerate(line):
                x = int(x)
                width = max(width, x)
                map[(x, y)] = c == "#"

    return height, width, map


def count_trees(map, h, w, dx, dy):
    x, y = (0, 0)
    trees = 0
    while y <= h:
        if map[(x % w, y)]:
            trees += 1

        x += dx
        y += dy

    return trees


def part_1():
    height, width, map = read_map()
    assert height != 0
    assert width != 0

    assert 268 == count_trees(map, height, width, 3, 1)


def part_2():
    height, width, map = read_map()

    p = 1
    for dx, dy in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
        t = count_trees(map, height, width, dx, dy)
        p *= t

    assert p == 3093068400
