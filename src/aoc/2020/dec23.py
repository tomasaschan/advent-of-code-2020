import datetime

from typing import Optional


class Node:
    def __init__(self, value):
        self.value = value
        self.next: Optional["Node"] = None

    def __str__(self) -> str:
        s = str(self.value)
        n = self.next
        while n.value != self.value:
            s += f" -> {n.value}"
            n = n.next

        return s


def parse(input):
    parsed = [int(c) for c in input]

    head = Node(parsed[0])
    cur = head
    nodes = {parsed[0]: head}
    for i in parsed[1:]:
        n = Node(i)
        nodes[i] = n
        cur.next = n
        cur = n

    cur.next = head

    return head, min(parsed), max(parsed), nodes


def extract_three(current):
    first_picked = current.next
    last_picked = first_picked.next.next

    current.next = last_picked.next
    return first_picked


def find_destination(current, lo, hi, picked, nodes):
    target = current.value - 1 if current.value > lo else hi
    while target in picked:
        target = target - 1 if target > lo else hi

    return nodes[target]


def insert_three_after(destination, three):
    three.next.next.next = destination.next
    destination.next = three


def play_round(current, lo, hi, nodes):
    picked = extract_three(current)
    destination = find_destination(
        current,
        lo,
        hi,
        set((picked.value, picked.next.value, picked.next.next.value)),
        nodes,
    )
    if destination.value == 1:
        print(
            f"putting {picked.value}, {picked.next.value} and {picked.next.next.value} after {destination.value}"
        )

    insert_three_after(destination, picked)

    return current.next


def order_after_1(nodes):
    current = nodes[1].next
    s = ""
    while current.value != 1:
        s += str(current.value)
        current = current.next
    return s


def extend(head, hi, nodes):
    v = hi
    current = head.next
    while current.next.value != head.value:
        current = current.next
    while v <= 1_000_000:
        if (v + 1) % 100_000 == 0:
            print(datetime.datetime.now(), "Creating node", v + 1)
        n = Node(v + 1)
        nodes[v + 1] = n
        current.next = n
        current = n
        v += 1

    current.next = head
    return head


def part_1():
    input = "137826495"
    current, lo, hi, nodes = parse(input)

    for _ in range(100):
        current = play_round(current, lo, hi, nodes)

    assert "59374826" == order_after_1(nodes)


def part_2():
    example_input = "389125467"
    my_input = "137826495"
    input = example_input
    current, lo, hi, nodes = parse(input)
    current = extend(current, hi, nodes)

    for n in nodes:
        assert n == nodes[n].value

    for i in range(10_000_002):
        if (i + 1) % 1_000_000 == 0:
            print(datetime.datetime.now(), "Playing round", i + 1)
        current = play_round(current, lo, hi, nodes)
