import itertools


weapons = [(8, 4, 0), (10, 5, 0), (25, 6, 0), (40, 7, 0), (74, 8, 0)]
armors = [(0, 0, 0), (13, 0, 1), (31, 0, 2), (53, 0, 3), (75, 0, 4), (102, 0, 5)]
rings = [(25, 1, 0), (50, 2, 0), (100, 3, 0), (20, 0, 1), (40, 0, 2), (80, 0, 3)]


def cost(item):
    return item[0]


def damage(item):
    return item[1]


def armor(item):
    return item[2]


def get_gear(*, reverse):
    def gear_combos():
        for weapon in weapons:
            for armor in armors:
                for r in range(3):
                    for ring_choice in itertools.combinations(rings, r):
                        yield [weapon, armor, *ring_choice]

    return sorted(
        gear_combos(),
        key=lambda combo: sum(cost(item) for item in combo),
        reverse=reverse,
    )


def play_game(items):
    boss_hp = 109
    boss_damage = 8
    boss_armor = 2

    player_hp = 100
    player_damage = sum(map(damage, items))
    player_armor = sum(map(armor, items))

    def both_alive():
        return player_hp > 0 and boss_hp > 0

    def player_turn():
        nonlocal boss_hp
        boss_hp -= max(player_damage - boss_armor, 1)

    def boss_turn():
        nonlocal player_hp
        player_hp -= max(boss_damage - player_armor, 1)

    player_in_turn = True

    while both_alive():
        if player_in_turn:
            player_turn()
        else:
            boss_turn()

        player_in_turn = not player_in_turn

    return player_hp > 0


def part_1():
    def solve():
        for selection in get_gear(reverse=False):
            if play_game(selection):
                return sum(map(cost, selection))

    assert solve() == 111


def part_2():
    def solve():
        for selection in get_gear(reverse=True):
            if not play_game(selection):
                return sum(map(cost, selection))

    assert solve() == 188
