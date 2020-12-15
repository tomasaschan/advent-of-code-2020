def take_turns(n, starting):
    spoken = {}

    t = 1
    prev = 0  # default-init; this value will never actually be used
    while t <= n:
        if t <= len(starting):
            s = starting[t - 1]
        elif prev in spoken and spoken[prev][1]:
            s = spoken[prev][0] - spoken[prev][1]
        else:
            s = 0

        spoken[s] = (t, spoken[s][0] if s in spoken else None)
        prev = s
        t += 1

    return [s for s, ts in spoken.items() if ts[0] == n][0]


def part_1_examples():
    print()
    assert 0 == take_turns(10, [0, 3, 6])

    assert 436 == take_turns(2020, [0, 3, 6])
    assert 1 == take_turns(2020, [1, 3, 2])
    assert 10 == take_turns(2020, [2, 1, 3])
    assert 27 == take_turns(2020, [1, 2, 3])
    assert 78 == take_turns(2020, [2, 3, 1])
    assert 438 == take_turns(2020, [3, 2, 1])
    assert 1836 == take_turns(2020, [3, 1, 2])


def part_1():
    assert 257 == take_turns(2020, [0, 14, 6, 20, 1, 4])


def part_2():
    assert 8546398 == take_turns(30000000, [0, 14, 6, 20, 1, 4])
