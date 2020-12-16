with open("input/2020/dec16.txt") as f:
    input = f.read()


def parse(input):
    rules, mine, nearby = input.split("\n\n")

    def parse_range(r):
        a, b = r.split("-")
        return int(a), int(b)

    def parse_rule(line):
        name, rngs = line.split(": ")
        return (name, [parse_range(r) for r in rngs.split(" or ")])

    def parse_ticket(line):
        return [int(n) for n in line.split(",")]

    return (
        {key: ranges for key, ranges in map(parse_rule, rules.split("\n"))},
        parse_ticket(mine.split("\n")[1]),
        [parse_ticket(line) for line in nearby.split("\n")[1:] if line != ""],
    )


def part_1():
    rules, _, nearby = parse(input)

    s = 0
    for ticket in nearby:
        for number in ticket:
            if not any(
                rule[0] <= number <= rule[1]
                for validation in rules.values()
                for rule in validation
            ):
                s += number

    assert 18227 == s


def is_valid(ticket, rules):
    for number in ticket:
        if not any(
            rule[0] <= number <= rule[1]
            for validation in rules.values()
            for rule in validation
        ):
            return False
    return True


def narrow_by_ticket(candidates, ticket, rules):
    for i, n in enumerate(ticket):
        for name, ranges in rules.items():
            if all(not r[0] <= n <= r[1] for r in ranges):
                if i in candidates[name]:
                    candidates[name].remove(i)
    return candidates


def narrow_by_elimination(candidates):
    seen = set()

    while any(len(indices) > 1 for indices in candidates.values()):
        name = next(
            n for n, ixs in candidates.items() if len(ixs) == 1 and n not in seen
        )

        seen.add(name)
        i = list(candidates[name])[0]
        for n in candidates.keys():
            if n != name and i in candidates[n]:
                candidates[n].remove(i)

    return {name: list(ixs)[0] for name, ixs in candidates.items()}


def part_2():
    rules, mine, nearby = parse(input)

    valid = [ticket for ticket in nearby if is_valid(ticket, rules)]

    candidates = {name: set(range(len(valid[0]))) for name in rules.keys()}
    for ticket in valid:
        narrow_by_ticket(candidates, ticket, rules)

    mapping = narrow_by_elimination(candidates)

    answer = 1
    for name, ix in mapping.items():
        if name.startswith("departure"):
            answer *= mine[ix]

    assert 2355350878831 == answer
