with open("input/2020/dec11.txt") as f:
    input = f.read().splitlines()


def prep(state):
    """
    surround the map with empty spaces (.) so i don't have to worry about out-of-bounds
    """
    ncols = len(state[0]) + 2

    return (
        [
            [c for c in ("." * ncols)],
            *([".", *(c for c in line), "."] for line in state),
            [c for c in ("." * ncols)],
        ],
        [
            [c for c in ("." * ncols)],
            *([".", *(c for c in line), "."] for line in state),
            [c for c in ("." * ncols)],
        ],
    )


def evolve(apply_rules, state, next):
    def empty(c):
        return c == "." or c == "L"

    for y in range(1, len(state) - 1):
        for x in range(1, len(state[0]) - 1):
            if state[y][x] == ".":
                continue

            next[y][x] = apply_rules(x, y, state)


# def foo():

#             if state[y][x] == "L" and all(map(empty, surroundings)):
#                 updated[y][x] = "#"

#                 updated[y][x] = "L"

#     return updated


def stringify(state):
    """
    turns out strings are _much_ faster to compare for equality than arrays
    """
    return "\n".join("".join(line) for line in state)


def occupied_seats(state):
    """
    count occupied seats
    """
    return sum(1 if c == "#" else 0 for line in state for c in line)


def solve(apply_rules, a, b):
    evolve(apply_rules, a, b)

    while occupied_seats(a) != occupied_seats(b):
        a, b = b, a
        evolve(apply_rules, a, b)

    return occupied_seats(a)


def part_1():
    def empty(c):
        return c == "." or c == "L"

    def apply_rules(x, y, state):
        surroundings = (
            state[y - 1][x - 1],  # nw
            state[y - 1][x],  # n
            state[y - 1][x + 1],  # ne
            state[y][x + 1],  # e
            state[y + 1][x + 1],  # se
            state[y + 1][x],  # s
            state[y + 1][x - 1],  # sw
            state[y][x - 1],  # w
        )
        if state[y][x] == ".":
            return "."
        if state[y][x] == "L":
            return "#" if all(map(empty, surroundings)) else "L"
        if state[y][x] == "#":
            return "L" if sum(1 if s == "#" else 0 for s in surroundings) >= 4 else "#"

    a, b = prep(input)

    assert 2316 == solve(apply_rules, a, b)


def part_2():
    def apply_rules(x, y, state):
        def seats_in_los():
            for (dx, dy) in [
                (-1, -1),
                (0, -1),
                (1, -1),
                (-1, 0),
                (1, 0),
                (-1, 1),
                (0, 1),
                (1, 1),
            ]:
                i, j = x + dx, y + dy
                while (
                    0 < i < len(state[0]) - 1
                    and 0 < j < len(state) - 1
                    and state[j][i] == "."
                ):
                    i, j = i + dx, j + dy
                yield state[j][i]

        if state[y][x] == ".":
            return "."
        if state[y][x] == "L":
            return (
                "#" if sum(1 if s == "#" else 0 for s in seats_in_los()) == 0 else "L"
            )
        if state[y][x] == "#":
            return (
                "L" if sum(1 if s == "#" else 0 for s in seats_in_los()) >= 5 else "#"
            )

    a, b = prep(input)
    assert 2128 == solve(apply_rules, a, b)
