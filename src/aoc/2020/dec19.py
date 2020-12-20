import re


def parse_rules(lines):
    def parse_rule(line):
        id, rule = line.split(": ")
        return id, [o.split(" ") for o in rule.split(" | ")]

    return {id: rule for id, rule in map(parse_rule, lines)}


def puzzle_input():
    with open("input/2020/dec19.txt") as f:
        input = f.read().split("\n\n")
        rules = parse_rules(input[0].splitlines())
        messages = input[1].splitlines()

    return rules, messages


def build_rx(rules, rule, modify=False):
    if rule.startswith('"'):
        return rule.strip('"')

    if modify and rule == "8":
        return "(?:" + build_rx(rules, "42", modify) + ")+"
    elif modify and rule == "11":
        return (
            "(?:"
            + "|".join(
                (
                    build_rx(rules, "42", modify)
                    + f"{{{d}}}"
                    + build_rx(rules, "31", modify)
                    + f"{{{d}}}"
                )
                for d in range(1, 20)  # my input only needs 6
            )
            + ")"
        )
    else:
        return (
            "(?:"
            + "|".join(
                "".join(build_rx(rules, part, modify) for part in option)
                for option in rules[rule]
            )
            + ")"
            if len(rules[rule]) > 1
            else "".join(build_rx(rules, part, modify) for part in rules[rule][0])
        )


def part_1():
    rules, messages = puzzle_input()
    rx = build_rx(rules, "0", None)
    assert 222 == sum(1 for msg in messages if re.fullmatch(rx, msg))


def part_2():
    rules, messages = puzzle_input()
    rx = build_rx(rules, "0", True)
    assert 339 == sum(1 for msg in messages if re.fullmatch(rx, msg))
