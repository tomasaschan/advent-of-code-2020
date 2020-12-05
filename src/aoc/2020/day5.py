with open("input/dec5.txt") as f:
    data = f.readlines()


def binary_search(spec, size, dn, up):
    lo, hi = 0, size - 1

    for s in spec:
        if s == up:
            lo = hi - (hi - lo) // 2
        elif s == dn:
            hi = lo + (hi - lo) // 2
        else:
            raise Exception("invalid spec, up, dn:", spec, up, dn)

    assert lo == hi

    return lo


def get_seat(binary_spec):
    row_spec = binary_spec[:7]
    assert len(row_spec) == 7
    col_spec = binary_spec[7:]
    assert len(col_spec) == 3

    row = binary_search(row_spec, 128, "F", "B")
    col = binary_search(col_spec, 8, "L", "R")
    return row, col


def seat_id(spec):
    row, col = get_seat(spec)
    return row * 8 + col


def part_1_examples():
    assert get_seat("FBFBBFFRLR") == (44, 5)
    assert seat_id("FBFBBFFRLR") == 357


def part_1():
    assert 915 == max(seat_id(spec.strip()) for spec in data)

    assert 915 == max(
        int(
            spec.strip()
            .replace("F", "0")
            .replace("B", "1")
            .replace("L", "0")
            .replace("R", "1"),
            2,
        )
        for spec in data
    )


def part_2():
    ids = sorted([seat_id(spec.strip()) for spec in data])
    id = None
    for i in range(len(ids)):
        if i == 0:
            continue

        if ids[i - 1] + 2 == ids[i]:
            id = ids[i] - 1
            break

    assert 699 == id
