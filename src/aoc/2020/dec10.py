import functools

with open("input/2020/dec10.txt") as f:
    input = f.readlines()

short = "16,10,15,5,1,11,7,19,6,12,4".split(",")
long = (
    "28,33,18,42,31,14,46,20,48,47,24,23,49,"
    + "45,19,38,39,11,1,32,25,35,8,17,7,9,4,2,34,10,3"
).split(",")


def joltages(lines):
    return sorted(int(line) for line in lines)


def solve_part_1(js):
    ones, threes = 0, 0
    for u, v in zip([0, *js[:-1]], js):
        if v - u == 1:
            ones += 1
        elif v - u == 3:
            threes += 1

    return ones * (threes + 1)


def part_1_examples():
    assert 7 * 5 == solve_part_1(joltages(short))
    assert 22 * 10 == solve_part_1(joltages(long))


def part_1():
    assert 1690 == solve_part_1(joltages(input))


@functools.cache
def ways_to_combine_to(js, target):
    if len(js) == 1:
        return 1
    if target - js[-1] > 3:
        return 0
    if target - js[-1] == 3:
        return ways_to_combine_to(js[:-1], js[-1])
    else:
        return ways_to_combine_to(js[:-1], target) + ways_to_combine_to(js[:-1], js[-1])


def solve_part_2(lines):
    js = tuple([0, *joltages(lines)])
    count = ways_to_combine_to(js, js[-1] + 3)
    return count


def part_2_examples():
    assert 8 == solve_part_2(short)
    assert 19208 == solve_part_2(long)


def part_2():
    assert 5289227976704 == solve_part_2(input)
