from typing import Iterator


def parse(input, dimensions):
    assert dimensions == 3 or dimensions == 4
    s = set()
    for y, line in enumerate(input.splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                s.add((x, y, 0) if dimensions == 3 else (x, y, 0, 0))

    return s


def get_puzzle_input(dimensions):
    with open("input/2020/dec17.txt") as f:
        return parse(f.read(), dimensions)


def surroundings(*coords: int) -> Iterator[tuple[int, ...]]:
    assert len(coords) == 3 or len(coords) == 4

    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            for k in (-1, 0, 1):
                if len(coords) == 3:
                    yield (coords[0] + i, coords[1] + j, coords[2] + k)
                else:
                    for l in (-1, 0, 1):  # noqa: E741
                        yield (
                            coords[0] + i,
                            coords[1] + j,
                            coords[2] + k,
                            coords[3] + l,
                        )


def active_surroundings(s: set[tuple[int, ...]], *c: int) -> int:
    return sum(1 for p in surroundings(*c) if p in s and p != c)


def points_of_interest(s: set[tuple[int, ...]]) -> set[tuple[int, ...]]:
    def _all():
        for p in s:
            yield from surroundings(*p)

    return set(_all())


def evolve(s: set[tuple[int, ...]]) -> set[tuple[int, ...]]:
    nxt = set()
    for c in points_of_interest(s):
        if c in s and 2 <= active_surroundings(s, *c) <= 3:
            nxt.add(c)
        elif c not in s and active_surroundings(s, *c) == 3:
            nxt.add(c)

    return nxt


def part_1():
    s = get_puzzle_input(dimensions=3)
    for _ in range(6):
        s = evolve(s)

    assert 384 == len(s)


def part_2():
    s = get_puzzle_input(dimensions=4)
    for _ in range(6):
        s = evolve(s)

    assert 2012 == len(s)
