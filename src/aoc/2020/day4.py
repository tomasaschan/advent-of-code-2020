import re

with open("input/dec4.txt") as f:
    data = [s.strip() for s in f.readlines()]

rx = re.compile(r"(\w+):([^\s]+)")


def count_valid(validate):
    valid = 0
    password = {}

    for line in data:
        if line == "":
            if validate(password):
                valid += 1
            password = {}

        m = rx.findall(line)
        for m in rx.findall(line):
            password[m[0]] = m[1]

    if validate(password):
        valid += 1

    return valid


def part_1():
    def validate(password):
        return (
            "byr" in password
            and "iyr" in password
            and "eyr" in password
            and "hgt" in password
            and "hcl" in password
            and "ecl" in password
            and "pid" in password
        )

    assert 235 == count_valid(validate)


def part_2():
    def validate(password):
        try:
            assert int(password["byr"]) >= 1920 and int(password["byr"]) <= 2002
            assert int(password["iyr"]) >= 2010 and int(password["iyr"]) <= 2020
            assert int(password["eyr"]) >= 2020 and int(password["eyr"]) <= 2030

            height, unit = re.match(r"^(\d+)(cm|in)", password["hgt"]).groups()
            if unit == "cm":
                assert 150 <= int(height) <= 193
            elif unit == "in":
                assert 59 <= int(height) <= 76
            else:
                raise Exception()

            assert re.match(r"^#[0-9a-f]{6}$", password["hcl"]) is not None
            assert (
                re.match(r"^amb|blu|brn|gry|grn|hzl|oth$", password["ecl"]) is not None
            )

            assert re.match(r"^\d{9}$", password["pid"]) is not None

            return True
        except Exception:
            return False

    assert 194 == count_valid(validate)
