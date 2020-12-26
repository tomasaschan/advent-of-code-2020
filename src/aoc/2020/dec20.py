def puzzle_input(file="input/2020/dec20.txt"):
    with open(file) as f:
        input = f.read()
        return parse(input)


def parse_tile(lines):
    return set(
        (x, y) for y, line in enumerate(lines) for x, c in enumerate(line) if c == "#"
    )


def parse(input: str):
    def gen():
        for tile in input.split("\n\n"):
            lines = tile.splitlines()
            if lines:
                id = int(lines[0].replace("Tile ", "").replace(":", ""))
                yield id, parse_tile(lines[1:])

    return {id: tile for id, tile in gen()}


DIRECTIONS = ("u", "r", "d", "l", "u", "r")


def edge(tile, direction):
    def gen():
        for i in range(10):
            if direction == "u":
                yield (i, 0)
            elif direction == "r":
                yield (9, i)
            elif direction == "d":
                yield (i, 9)
            elif direction == "l":
                yield (0, i)
            else:
                raise Exception("Invalid orientation", direction)

    return "".join("#" if t in tile else "." for t in gen())


def all_edges(tiles):
    edges = {}

    for id, tile in tiles.items():
        for direction in ("u", "d", "l", "r"):
            e = edge(tile, direction)
            if e in edges:
                edges[e].append((id, direction))
            else:
                edges[e] = [(id, direction)]

    return edges


def map_neighbors(tiles):
    edges = all_edges(tiles)
    return {
        tile: {
            dir: id
            for dir in ("u", "d", "l", "r")
            for id in (
                *(id for id, _ in edges.get(edge(tiles[tile], dir), [])),
                *(id for id, _ in edges.get(edge(tiles[tile], dir)[::-1], [])),
            )
            if id != tile
        }
        for tile in tiles
    }


def find_corners(neighbors):
    return [tile for tile, nbs in neighbors.items() if len(nbs) == 2]


def part_1():
    tiles = puzzle_input()
    p = 1
    for c in find_corners(map_neighbors(tiles)):
        p *= c
    assert 15405893262491 == p


def calculate_alginment(tiles):
    neighbors = map_neighbors(tiles)
    corners = find_corners(neighbors)
    upper_left = corners[0]
    while set(neighbors[upper_left].keys()) != set(("r", "d")):
        rotate(tiles, neighbors, upper_left)

    def build_row(left: list[int], above: list[int] = None) -> list[int]:
        if "r" not in neighbors[left[-1]] or len(left) > 15:
            return left

        ths = neighbors[left[-1]]
        nxt = ths["r"]

        while neighbors[nxt].get("l") != left[-1]:
            rotate(tiles, neighbors, nxt)

        if above is None:
            if "u" in neighbors[nxt]:
                flip_v(tiles, neighbors, nxt)
        else:
            abv = above[len(left)]
            if "u" not in neighbors[nxt] or neighbors[nxt]["u"] != abv:
                flip_v(tiles, neighbors, nxt)

        return build_row([*left, nxt], above)

    def build_rows(rows: list[list[int]]) -> list[list[int]]:
        if "d" not in neighbors[rows[-1][0]] or len(rows) > 15:
            return rows

        above = rows[-1][0]
        nxt = neighbors[above]["d"]

        while neighbors[nxt].get("u") != above:
            rotate(tiles, neighbors, nxt)

        if "l" in neighbors[nxt]:
            flip_h(tiles, neighbors, nxt)

        return build_rows([*rows, build_row([nxt], rows[-1])])

    return build_rows([build_row([upper_left])])


def rot(img):
    ymax = max(y for _, y in img)
    return set((ymax - y, x) for (x, y) in img)


def flh(img):
    xmax = max(x for x, _ in img)
    return set((xmax - x, y) for (x, y) in img)


def flv(img):
    ymax = max(y for _, y in img)
    return set((x, ymax - y) for (x, y) in img)


def rotate(tiles, neighbors, tile):
    tiles[tile] = rot(tiles[tile])
    neighbors[tile] = {
        DIRECTIONS[DIRECTIONS.index(dir) + 1]: tile
        for dir, tile in neighbors[tile].items()
    }


def flip_h(tiles, neighbors, tile):
    tiles[tile] = flh(tiles[tile])
    neighbors[tile] = {
        dir if dir in ("u", "d") else DIRECTIONS[DIRECTIONS.index(dir) + 2]: tile
        for dir, tile in neighbors[tile].items()
    }


def flip_v(tiles, neighbors, tile):
    tiles[tile] = flv(tiles[tile])
    neighbors[tile] = {
        dir if dir in ("l", "r") else DIRECTIONS[DIRECTIONS.index(dir) + 2]: tile
        for dir, tile in neighbors[tile].items()
    }


def build_image(tiles, alignment):
    image = set()
    for r, row in enumerate(alignment):
        for y in range(8):
            for c, tile in enumerate(row):
                for x in range(8):
                    if (x + 1, y + 1) in tiles[tile]:
                        image.add((x + c * 8, y + r * 8))
    return image


def bounding_box(image):
    xmin = min(x for x, _ in image)
    xmax = max(x for x, _ in image) + 1
    ymin = min(y for _, y in image)
    ymax = max(y for _, y in image) + 1

    return (xmin, ymin), (xmax, ymax)


def draw_image(image: set[tuple[int, int]]):
    (xmin, ymin), (xmax, ymax) = bounding_box(image)
    for y in range(ymin, ymax):
        for x in range(xmin, xmax):
            print("#" if (x, y) in image else ".", end="")
        print()


def monster_image():
    with open("input/2020/dec20-monster.txt") as f:
        return parse_tile(f.read().splitlines())


def translate(img, x, y):
    return set((i + x, j + y) for (i, j) in img)


def search_for(needle, haystack):
    (hay_xmin, hay_ymin), (hay_xmax, hay_ymax) = bounding_box(haystack)
    (needle_xmin, needle_ymin), (needle_xmax, needle_ymax) = bounding_box(needle)

    def gen():
        for dy in range((hay_ymax - hay_ymin) - (needle_ymax - needle_ymin)):
            for dx in range((hay_xmax - hay_xmin) - (needle_xmax - needle_xmin)):
                xmin = hay_xmin + dx
                ymin = hay_ymin + dy
                xmax = xmin + needle_xmax - needle_xmin
                ymax = ymin + needle_ymax - needle_ymin

                if all(p in haystack for p in translate(needle, dx, dy)):
                    yield ((xmin, ymin), (xmax, ymax))

    return list(gen())


def unmask_monsters(image):
    monster = monster_image()

    def search_transformed():
        for transform in (
            lambda i: i,
            rot,
            lambda i: rot(rot(i)),
            lambda i: rot(rot(rot(i))),
            flh,
            lambda i: rot(flh(i)),
            lambda i: rot(rot(flh(i))),
            lambda i: rot(rot(rot(flh(i)))),
        ):
            transformed = transform(image)
            monsters = search_for(monster, transformed)
            if monsters:
                return (monsters, transformed)
        else:
            raise Exception("no monsters found!")

    monsters, image = search_transformed()

    for (x, y), _ in monsters:
        image = image - translate(monster, x, y)

    return image


def part_2():
    tiles = puzzle_input()
    alignment = calculate_alginment(tiles)
    image: set[tuple[int, int]] = build_image(tiles, alignment)

    assert 2133 == len(unmask_monsters(image))
