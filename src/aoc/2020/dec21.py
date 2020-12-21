from collections import defaultdict


def puzzle_input():
    with open("input/2020/dec21.txt") as f:
        input = f.read().splitlines()
        return parse(input)


def parse(input: list[str]):
    def p(line: str):
        ingredients, known_allergens = line.strip(")").split(" (")
        return (
            ingredients.split(" "),
            known_allergens.replace("contains ", "").split(", "),
        )

    return [p(line) for line in input]


def narrow_by_ingredient_lists(foods):
    all_ingredients = set(ingredient for food in foods for ingredient in food[0])

    allergens = defaultdict(lambda: all_ingredients.copy())

    for food in foods:
        for allergen in food[1]:
            allergens[allergen].intersection_update(food[0])

    return allergens


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


def part_1():
    foods = puzzle_input()
    allergens = narrow_by_elimination(narrow_by_ingredient_lists(foods))

    assert 2061 == sum(
        1
        for food in foods
        for ingredient in food[0]
        if ingredient not in allergens.values()
    )


def part_2():
    foods = puzzle_input()
    allergens = narrow_by_elimination(narrow_by_ingredient_lists(foods))

    assert "cdqvp,dglm,zhqjs,rbpg,xvtrfz,tgmzqjz,mfqgx,rffqhl" == ",".join(
        allergens[eng] for eng in sorted(allergens.keys())
    )
