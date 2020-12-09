import re
import queue

from collections import defaultdict

with open("input/2020/dec07.txt") as f:
    input = f.read()

CONTAINER_RX = re.compile(r"^(.+?) bags?")
CONTAINED_RX = re.compile(r"(\d+) (.+?) bags?")


def parse_line(line):
    container = CONTAINER_RX.match(line).groups()[0]
    contained = [(int(m[0]), m[1]) for m in CONTAINED_RX.findall(line)]
    return container, contained


def part_1():
    edges = defaultdict(list)

    for line in input.splitlines():
        container, contained = parse_line(line)

        for _, color in contained:
            edges[color].append(container)

    q = queue.Queue()
    q.put("shiny gold")

    seen = set()

    while not q.empty():
        bag = q.get()

        for container in edges[bag]:
            q.put(container)
            seen.add(container)

    assert len(seen) == 254


def part_2():
    edges = defaultdict(list)

    for line in input.splitlines():
        container, contained = parse_line(line)

        for (count, color) in contained:
            edges[container].append((count, color))

    q = queue.Queue()
    q.put((1, "shiny gold"))

    count = 0

    while not q.empty():
        (c, bag) = q.get()
        count += c
        for cnt, color in edges[bag]:
            q.put((cnt * c, color))

    assert count - 1 == 6006
