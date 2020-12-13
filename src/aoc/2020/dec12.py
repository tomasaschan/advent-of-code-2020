with open("input/2020/dec12.txt") as f:
    input = f.read().splitlines()


cw = ["N", "E", "S", "W"]
ccw = ["N", "W", "S", "E"]


def move(state, instruction):
    if instruction[0] == "N":
        return (state[0], state[1] + int(instruction[1:]), state[2])
    elif instruction[0] == "S":
        return (state[0], state[1] - int(instruction[1:]), state[2])
    elif instruction[0] == "E":
        return (state[0] + int(instruction[1:]), state[1], state[2])
    elif instruction[0] == "W":
        return (state[0] - int(instruction[1:]), state[1], state[2])
    elif instruction[0] == "L":
        return (
            state[0],
            state[1],
            ccw[(ccw.index(state[2]) + int(instruction[1:]) // 90) % 4],
        )
    elif instruction[0] == "R":
        return (
            state[0],
            state[1],
            cw[(cw.index(state[2]) + int(instruction[1:]) // 90) % 4],
        )
    elif instruction[0] == "F":
        return move(state, state[2] + instruction[1:])


def move_waypoint(position, waypoint, instruction):
    if instruction[0] == "N":
        return position, (waypoint[0], waypoint[1] + int(instruction[1:]))
    if instruction[0] == "S":
        return position, (waypoint[0], waypoint[1] - int(instruction[1:]))
    if instruction[0] == "E":
        return position, (waypoint[0] + int(instruction[1:]), waypoint[1])
    if instruction[0] == "W":
        return position, (waypoint[0] - int(instruction[1:]), waypoint[1])
    if instruction[0] == "L":
        wpx, wpy = waypoint
        for _ in range(int(instruction[1:]) // 90):
            wpx, wpy = -wpy, wpx
        return position, (wpx, wpy)
    if instruction[0] == "R":
        wpx, wpy = waypoint
        for _ in range(int(instruction[1:]) // 90):
            wpx, wpy = wpy, -wpx
        return position, (wpx, wpy)
    if instruction[0] == "F":
        x, y = position
        for _ in range(int(instruction[1:])):
            x += waypoint[0]
            y += waypoint[1]
        return (x, y), waypoint

    raise Exception(f"Unknown instruction: {instruction}")


def part_1():
    state = (0, 0, "E")

    for instruction in input:
        state = move(state, instruction)

    assert 445 == abs(state[0]) + abs(state[1])


def part_2():
    pos = (0, 0)
    wp = (10, 1)
    for instruction in input:
        pos, wp = move_waypoint(pos, wp, instruction)

    assert 0 == abs(pos[0]) + abs(pos[1])


def part_2_example():
    pos, wp = (0, 0), (10, 1)
    for instruction in """F10
N3
F7
L270
F11""".splitlines():
        print(pos, wp)
        print(instruction)
        pos, wp = move_waypoint(pos, wp, instruction)
    print(pos, wp)
    assert 286 == abs(pos[0]) + abs(pos[1])
