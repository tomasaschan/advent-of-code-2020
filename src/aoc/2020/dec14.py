import re
from typing import Iterator


INSTRUCTION = re.compile(r"^mem\[(\d+)\] = (\d+)$")
THIRTYSIX_ONES = 0b111111111111111111111111111111111111


def get_instructions():
    with open("input/2020/dec14.txt") as f:
        for line in f:
            if line.startswith("mask = "):
                yield ("mask", line.lstrip("mask =").rstrip())
            else:
                addr, val = INSTRUCTION.match(line.strip()).groups()
                yield ("set", addr, val)


def apply_value_mask(x, mask):
    return (x & int(mask.replace("X", "1"), 2)) | int(mask.replace("X", "0"), 2)


def part_1():
    mem = {}
    mask = None

    for instr in get_instructions():
        if instr[0] == "mask":
            mask = instr[1]
        else:
            addr, val = int(instr[1]), int(instr[2])
            mem[addr] = apply_value_mask(val, mask)

    assert 14954914379452 == sum(mem.values())


def apply_addr_mask(addr: int, mask: str):
    # If the bitmask bit is 0, the memory address bit is unchanged.
    # If the bitmask bit is 1, the memory address bit is overwritten with 1.
    addr = addr | int(mask.replace("X", "0"), 2)

    # If the bitmask bit is X, the corresponding memory address bit is floating.
    def float_bits(addr: int, bits: list[int]) -> Iterator[int]:
        if bits == []:
            yield addr
        else:
            b = bits[0]
            zeroed = (1 << b) ^ THIRTYSIX_ONES
            yield from float_bits(addr & zeroed, bits[1:])
            oned = 1 << b
            yield from float_bits(addr | oned, bits[1:])

    yield from float_bits(addr, [35 - i for i, c in enumerate(mask) if c == "X"])


def part_2():
    mask = ""
    mem = {}
    for instr in get_instructions():
        if instr[0] == "mask":
            mask = str(instr[1])
        else:
            addr, val = int(instr[1]), int(instr[2])
            for masked_addr in apply_addr_mask(addr, mask):
                mem[masked_addr] = val

    assert 3415488160714 == sum(mem.values())
