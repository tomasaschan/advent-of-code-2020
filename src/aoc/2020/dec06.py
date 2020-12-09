import string

with open("input/2020/dec06.txt") as f:
    input = f.read()


def groups(input):
    return input.split("\n\n")


def part_1():
    def sets(input):
        for group in groups(input):
            s = set()
            for line in group.split("\n"):
                s.update(line)

            yield s

    assert 6612 == sum(len(s) for s in sets(input))


def part_2():
    c = 0

    for group in groups(input):
        s = set(string.ascii_lowercase)

        for person in group.splitlines():
            s = s.intersection(person)

        c += len(s)

    assert 3268 == c
