from collections import defaultdict


def puzzle_input(tag=""):
    with open(f"input/2020/dec24{'-' + tag if tag else ''}.txt") as f:
        return f.read().splitlines()


def parse(line):
    def gen():
        i = 0
        while i < len(line):
            if line[i] in ("e", "w"):
                yield line[i]
                i += 1
            else:
                assert line[i] in ("s", "n")
                yield line[i : i + 2]
                i += 2

        assert i == len(line)

    return list(gen())


def normalize(path):
    steps = defaultdict(int)

    for step in path:
        steps[step] += 1

    unidirectional = (
        steps["w"] - steps["e"],
        steps["nw"] - steps["se"],
        steps["ne"] - steps["sw"],
    )

    normalized = (
        unidirectional[0] - unidirectional[2],
        unidirectional[1] + unidirectional[2],
    )

    return normalized


def initial_state(input):
    black = set()

    for tile in (normalize(parse(line)) for line in input):
        if tile in black:
            black.remove(tile)
        else:
            black.add(tile)

    return black


def surroundings(w, nw):
    yield (w + 1, nw)  # w
    yield (w, nw + 1)  # nw
    yield (w - 1, nw + 1)  # ne
    yield (w - 1, nw)
    yield (w, nw - 1)  # se
    yield (w + 1, nw - 1)  # sw


def black_surroundings(w, nw, tiles):
    return sum(1 for c in surroundings(w, nw) if c in tiles)


def interesting_tiles(tiles):
    def gen():
        for tile in tiles:
            yield tile
            yield from surroundings(*tile)

    return set(gen())


def evolve(tiles):
    nxt = set()
    for t in interesting_tiles(tiles):
        b = black_surroundings(*t, tiles)
        #   black tile remains black        white tile flips
        if (t in tiles and 1 <= b <= 2) or (t not in tiles and b == 2):
            nxt.add(t)

    return nxt


def part_1():
    input = puzzle_input()
    black = initial_state(input)
    assert 521 == len(black)


def part_2():
    input = puzzle_input()
    tiles = initial_state(input)

    for _ in range(100):
        tiles = evolve(tiles)

    assert 4242 == len(tiles)
