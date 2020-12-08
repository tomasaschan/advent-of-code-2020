with open("input/dec8.txt") as f:
    input = f.read()


def parse(input):
    def parse_line(line):
        instr, ops = line.split(" ", 1)
        return instr, int(ops)

    return list(map(parse_line, input.splitlines()))


def run_program(program):
    def nop(op):
        nonlocal instruction
        instruction += 1

    def acc(op):
        nonlocal accumulator, instruction
        accumulator += op
        instruction += 1

    def jmp(op):
        nonlocal instruction
        instruction += op

    accumulator = 0
    instruction = 0
    seen = set()

    while instruction != len(program):
        (instr, op) = program[instruction]
        seen.add(instruction)
        {"nop": nop, "acc": acc, "jmp": jmp}[instr](op)

        if instruction in seen:
            return accumulator, False

    return accumulator, True


def program_variations(program):
    for i, (ins, _) in enumerate(program):
        if ins == "nop":
            yield [
                (ins, op) if j != i else ("jmp", op)
                for j, (ins, op) in enumerate(program)
            ]
        elif ins == "jmp":
            yield [
                (ins, op) if j != i else ("nop", op)
                for j, (ins, op) in enumerate(program)
            ]


def part_1():
    program = parse(input)
    acc, halted = run_program(program)
    assert not halted
    assert 1801 == acc


def part_2():
    program = parse(input)

    result = 0
    for variation in program_variations(program):
        result, halted = run_program(variation)
        if halted:
            break

    assert 2060 == result
