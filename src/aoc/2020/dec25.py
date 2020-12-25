def puzzle_input(file=""):
    with open(f"input/2020/dec25{'-' + file if file else ''}.txt") as f:
        return [int(line) for line in f.read().splitlines()]


def transform(n, sn):
    return (n * sn) % 20201227


def find_loop_number(pubkey):
    n = 0
    k = 1
    while k != pubkey:
        n += 1
        k = transform(k, 7)

    return n


def find_private_key(pubkey, n):
    key = 1
    for _ in range(n):
        key = transform(key, pubkey)

    return key


def part_1():
    door, card = puzzle_input()

    door_n = find_loop_number(door)
    door_priv_key = find_private_key(card, door_n)

    assert 11288669 == door_priv_key
