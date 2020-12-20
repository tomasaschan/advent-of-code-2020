with open("input/2020/dec18.txt") as f:
    input = f.read().splitlines()


def tokenize(input: str):
    if len(input) == 0:
        return
    if input[0] == "(":
        yield ("OPEN",)
        yield from tokenize(input[1:])
    if input[0] == ")":
        yield ("CLOSE",)
        yield from tokenize(input[1:])
    if input[0].isdigit():
        i = 1
        while i < len(input) and input[i].isdigit():
            i += 1
        yield ("LITERAL", int(input[0:i]))
        yield from tokenize(input[i:])
    if input[0] == " ":
        yield from tokenize(input[1:])
    if input[0] == "*":
        yield ("MUL",)
        yield from tokenize(input[1:])
    if input[0] == "+":
        yield ("ADD",)
        yield from tokenize(input[1:])


def parse_1(tokens):
    # grammar:
    #
    # expression -> binary
    # binary     -> term (("*" | "+") term)*
    # term       -> NUMBER | "(" expression ")"

    current = 0

    def match(*ts):
        nonlocal current
        if current >= len(tokens):
            return False
        for t in ts:
            if tokens[current][0] == t:
                current += 1
                return True

        return False

    def expression():
        return binary()

    def binary():
        expr = term()

        while match("ADD", "MUL"):
            op = tokens[current - 1][0]
            rhs = term()
            expr = (op, expr, rhs)

        return expr

    def term():
        if match("LITERAL"):
            return ("LITERAL", tokens[current - 1][1])

        if match("OPEN"):
            expr = expression()
            assert match("CLOSE")
            return expr

    return expression()


def parse_2(tokens):
    # grammar:
    # expression     -> multiplication
    # multiplication -> factor ("*" factor)*
    # factor         -> term ("+" term)*
    # term           -> NUMBER | "(" expression ")"
    current = 0

    def match(*ts):
        nonlocal current
        if current >= len(tokens):
            return False
        for t in ts:
            if tokens[current][0] == t:
                current += 1
                return True

        return False

    def expression():
        return addition()

    def addition():
        expr = factor()

        while match("MUL"):
            rhs = factor()
            expr = ("MUL", expr, rhs)

        return expr

    def factor():
        expr = term()

        while match("ADD"):
            rhs = term()
            expr = ("ADD", expr, rhs)

        return expr

    def term():
        if match("LITERAL"):
            return ("LITERAL", tokens[current - 1][1])

        if match("OPEN"):
            expr = expression()
            assert match("CLOSE")
            return expr

        raise Exception("unexpected: " + tokens[current])

    return expression()


def evaluate(expr):
    if expr[0] == "LITERAL":
        return expr[1]
    if expr[0] == "ADD":
        return evaluate(expr[1]) + evaluate(expr[2])
    if expr[0] == "MUL":
        return evaluate(expr[1]) * evaluate(expr[2])


def compute_1(input):
    return evaluate(parse_1(list(tokenize(input))))


def compute_2(input):
    return evaluate(parse_2(list(tokenize(input))))


def part_1():
    assert 1408133923393 == sum(compute_1(line) for line in input)


def part_2():
    assert 314455761823725 == sum(compute_2(line) for line in input)
