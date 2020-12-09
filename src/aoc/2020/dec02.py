import re
from collections import defaultdict


def read_input():
    with open("./input/2020/dec02.txt", "r") as f:
        for line in f.readlines():
            yield line


rx = re.compile(r"(\d+)-(\d+) (\w): (\w+)")


def part_1():
    valid = 0
    for line in read_input():
        lo, hi, ch, pw = rx.match(line).groups()

        letters = defaultdict(int)
        for letter in pw:
            letters[letter] += 1

        if int(lo) <= letters.get(ch, 0) and letters.get(ch, 0) <= int(hi):
            valid += 1

    assert 622 == valid


def part_2():
    valid = 0
    for line in read_input():
        lo, hi, ch, pw = rx.match(line).groups()
        if (pw[int(lo) - 1] == ch) ^ (pw[int(hi) - 1] == ch):
            valid += 1

    assert 263 == valid
