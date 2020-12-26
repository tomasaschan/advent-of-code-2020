import itertools


def init(seed, n):
    s = {
        seed[i - 1] if i <= len(seed) else i: seed[i] if i < len(seed) else i + 1
        for i in range(1, n)
    }
    s[n if n > len(seed) else seed[-1]] = seed[0]
    return seed[0], s


def cups_from(cups, start, n, skip=0):
    def iter_cups(cups, start):
        current = start
        for _ in range(skip):
            current = cups[current]

        while True:
            yield current
            current = cups[current]

    return list(itertools.islice(iter_cups(cups, start), n))


def play_move(current, cups):
    picked = cups_from(cups, current, 3, skip=1)
    destination = current - 1 if current - 1 > 0 else max(cups.keys())
    while destination in picked:
        destination = destination - 1 if destination - 1 > 0 else max(cups.keys())

    for (s, d) in (
        (current, cups[picked[-1]]),
        (destination, picked[0]),
        (picked[-1], cups[destination]),
    ):
        cups[s] = d

    return cups[current]


def output(cups, start, n):
    return "".join(str(i) for i in cups_from(cups, start, n, skip=1))


def part_1():
    input = "137826495"
    current, cups = init([int(i) for i in input], len(input))

    for _ in range(100):
        current = play_move(current, cups)

    assert "59374826" == output(cups, 1, len(input) - 1)


def part_2():
    input = "137826495"
    current, cups = init([int(i) for i in input], 1_000_000)

    for _ in range(10_000_000):
        current = play_move(current, cups)

    a = cups[1]
    b = cups[a]

    assert 66878091588 == a * b
