from collections import defaultdict


def parse(input):
    s = defaultdict(bool)
    x, y = 0, 0
    for y, line in enumerate(input.splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                s[(x, y, 0, 0)] = True

    return s, (0, 0, 0, 0), (x, y, 0, 0)


def get_puzzle_input():
    with open("input/2020/dec17.txt") as f:
        return parse(f.read())


def surroundings(x, y, z, w, dimensions=3):
    assert dimensions == 3 or dimensions == 4
    assert (w == 0) if (dimensions == 3) else True

    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            for k in (-1, 0, 1):
                if dimensions == 3:
                    if i != 0 or j != 0 or k != 0:
                        yield (x + i, y + j, z + k, 0)
                else:
                    for l in (-1, 0, 1):  # noqa: E741
                        if i != 0 or j != 0 or k != 0 or l != 0:  # noqa: E741
                            yield (x + i, y + j, z + k, w + l)


def active_surroundings(s, dimensions, x, y, z, w):
    return sum(1 for p in surroundings(x, y, z, w, dimensions) if s[p])


def frame_of_view(lo, hi, extra=0, dimensions=3):
    assert dimensions == 3 or dimensions == 4
    xlo, ylo, zlo, wlo = lo
    xhi, yhi, zhi, whi = hi
    for z in range(zlo - extra, zhi + 1 + extra):
        for y in range(ylo - extra, yhi + 1 + extra):
            for x in range(xlo - extra, xhi + 1 + extra):
                if dimensions == 3:
                    yield (x, y, z, 0)
                else:
                    for w in range(wlo - extra, whi + 1 + extra):
                        yield (x, y, z, w)


def evolve(s, lo, hi, dimensions=3):
    nxt = defaultdict(bool)
    xlo, ylo, zlo, wlo = lo
    xhi, yhi, zhi, whi = hi

    for c in frame_of_view(lo, hi, extra=1, dimensions=dimensions):
        if s[c]:
            a = 2 <= active_surroundings(s, dimensions, *c) <= 3
        else:
            a = active_surroundings(s, dimensions, *c) == 3

        nxt[c] = a

        if a:
            xlo = min(c[0], xlo)
            ylo = min(c[1], ylo)
            zlo = min(c[2], zlo)
            wlo = min(c[3], wlo)
            xhi = max(c[0], xhi)
            yhi = max(c[1], yhi)
            zhi = max(c[2], zhi)
            whi = max(c[0], whi)

    return nxt, (xlo, ylo, zlo, wlo), (xhi, yhi, zhi, whi)


def draw_state(s, lo, hi):
    xlo, ylo, zlo = lo
    xhi, yhi, zhi = hi
    for z in range(zlo, zhi + 1):
        print(f"z={z}")
        for y in range(ylo, yhi + 1):
            for x in range(xlo, xhi + 1):
                print("#" if s[(x, y, z)] else ".", end="")
            print()
        print()


def part_1():
    s, lo, hi = get_puzzle_input()
    for _ in range(6):
        s, lo, hi = evolve(s, lo, hi, dimensions=3)

    assert 384 == sum(1 for v in s.values() if v)


def part_2():
    s, lo, hi = get_puzzle_input()
    for _ in range(6):
        s, lo, hi = evolve(s, lo, hi, dimensions=4)

    assert 2012 == sum(1 for v in s.values() if v)
