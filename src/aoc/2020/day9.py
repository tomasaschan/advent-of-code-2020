import itertools

with open("input/dec9.txt") as f:
    data = list(map(int, f.readlines()))

example_data = [
    35,
    20,
    15,
    25,
    47,
    40,
    62,
    55,
    65,
    95,
    102,
    117,
    150,
    182,
    127,
    219,
    299,
    277,
    309,
    576,
]


def find_first_invalid(preamble, data):
    for i in range(preamble, len(data)):
        ok = False
        for a, b in itertools.combinations(data[i - preamble : i], 2):
            if a + b == data[i]:
                ok = True
                break
        if not ok:
            return data[i]
    raise Exception("Found no invalid data")


def find_weakness(preamble, data: list[int]):
    first_invalid = find_first_invalid(preamble, data)
    for a in range(len(data)):
        for b in range(a + 1, len(data)):
            s = sum(data[a:b])
            if s == first_invalid:
                return min(data[a:b]) + max(data[a:b])
            if s > first_invalid:
                break


def part_1_example():
    assert 127 == find_first_invalid(5, example_data)


def part_1():
    assert 41682220 == find_first_invalid(25, data)


def part_2_example():
    assert 62 == find_weakness(5, example_data)


def part_2():
    assert 5388976 == find_weakness(25, data)
