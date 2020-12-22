from collections import deque


def puzzle_input():
    with open("input/2020/dec22.txt") as f:
        player1, player2 = f.read().split("\n\n")

    return (
        deque(int(card) for card in player1.splitlines()[1:]),
        deque(int(card) for card in player2.splitlines()[1:]),
    )


def score(deck):
    return sum(
        card * multiplier for card, multiplier in zip(deck, range(len(deck), 0, -1))
    )


def part_1():
    player1, player2 = puzzle_input()

    while player1 and player2:
        p1, p2 = player1.popleft(), player2.popleft()

        if p1 > p2:
            player1.extend((p1, p2))
        elif p2 > p1:
            player2.extend((p2, p1))
        else:
            raise Exception("draw!")

    assert 34255 == score(player1 or player2)


def serialize(game, a, b):
    return f"{game}:" + ",".join(map(str, a)) + "|" + ",".join(map(str, b))


def play_recursive(player1, player2):
    games: set[int] = set()
    seen = set()

    def recurse(a, b, game=1):
        games.add(game)
        round = 1

        while a and b:
            stringed = serialize(game, a, b)
            if stringed in seen:
                return True, score(a)
            else:
                seen.add(stringed)

            x, y = a.popleft(), b.popleft()

            if len(a) >= x and len(b) >= y:
                suba, subb = a.copy(), b.copy()
                while len(suba) > x:
                    suba.pop()
                while len(subb) > y:
                    subb.pop()
                (a_wins, _) = recurse(suba, subb, game=max(games) + 1)
                if a_wins:
                    a.extend((x, y))
                else:
                    b.extend((y, x))
            else:
                if x > y:
                    a.extend((x, y))
                else:
                    b.extend((y, x))
            round += 1

        return len(a) > 0, score(a or b) if game == 1 else None

    _, s = recurse(player1, player2)

    return s


def part_2():
    player1, player2 = puzzle_input()

    assert 33369 == play_recursive(player1, player2)
