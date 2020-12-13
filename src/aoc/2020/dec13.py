with open("input/2020/dec13.txt") as f:
    lines = f.read().splitlines()

    assert len(lines) == 2

    earliest_departure = int(lines[0])
    timetable = lines[1].split(",")


def part_1():
    schedule = sorted(map(int, filter(lambda s: s != "x", timetable)))

    departure = earliest_departure
    found_one = None
    while True:
        for bus in schedule:
            if departure % bus == 0:
                found_one = bus
                break
        if found_one:
            break
        departure += 1

    assert 261 == (departure - earliest_departure) * found_one


def bezout(a, b):
    rp, r = a, b
    sp, s = 1, 0
    tp, t = 0, 1

    while r != 0:
        q = rp // r
        rp, r = r, rp - q * r
        sp, s = s, sp - q * s
        tp, t = t, tp - q * t

    return (sp, tp)


def chinese_remainder(requirements):
    if len(requirements) == 0:
        return 0
    if len(requirements) == 1:
        x, n = requirements[0]
        return x % n
    else:
        first, second, rest = requirements[0], requirements[1], requirements[2:]
        x, y = bezout(first[1], second[1])
        a = (first[0] * second[1] * y + second[0] * first[1] * x) % (
            first[1] * second[1]
        )
        return chinese_remainder([(a, first[1] * second[1]), *rest])


def part_2():
    requirements = [(-i, int(s)) for i, s in enumerate(timetable) if s != "x"]

    assert 807435693182510 == chinese_remainder(requirements)
