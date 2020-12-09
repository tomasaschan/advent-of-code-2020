def read_program():
    with open("input/2015/dec23.txt") as input:
        program = []
        for line in input.readlines():
            program.append(tuple(map(lambda s: s.strip(","), line.strip().split(" "))))

        return program


def run(state, program):
    while 0 <= state["i"] and state["i"] < len(program):
        if program[state["i"]][0] == "hlf":
            state[program[state["i"]][1]] //= 2
        elif program[state["i"]][0] == "tpl":
            state[program[state["i"]][1]] *= 3
        elif program[state["i"]][0] == "inc":
            state[program[state["i"]][1]] += 1
        elif program[state["i"]][0] == "jmp":
            state["i"] += int(program[state["i"]][1])
            continue
        elif program[state["i"]][0] == "jie":
            if int(state[program[state["i"]][1]]) % 2 == 0:
                state["i"] += int(program[state["i"]][2])
                continue
        elif program[state["i"]][0] == "jio":
            if int(state[program[state["i"]][1]]) == 1:
                state["i"] += int(program[state["i"]][2])
                continue
        else:
            raise Exception(f"unknown instruction {program[state['i']]}")
        state["i"] += 1

    return state


def part_1():
    program = read_program()
    end_state = run({"a": 0, "b": 0, "i": 0}, program)

    assert 184 == end_state["b"]


def part_2():
    program = read_program()
    end_state = run({"a": 1, "b": 0, "i": 0}, program)

    assert 231 == end_state["b"]
