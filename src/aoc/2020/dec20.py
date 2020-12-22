def puzzle_input(file="input/2020/dec20.txt"):
    with open(file) as f:
        input = f.read()
        return parse(input)


def parse(input: str):
    def parse_tile(lines):
        return set(
            (x, y)
            for y, line in enumerate(lines)
            for x, c in enumerate(line)
            if c == "#"
        )

    def gen():
        for tile in input.split("\n\n"):
            lines = tile.splitlines()
            if lines:
                id = int(lines[0].replace("Tile ", "").replace(":", ""))
                yield id, parse_tile(lines[1:])

    return {id: tile for id, tile in gen()}


def edge(tile, direction):
    def gen():
        for i in range(10):
            if direction == 1:
                yield (i, 0) in tile
            elif direction == 2:
                yield (9, i) in tile
            elif direction == 3:
                yield (i, 9) in tile
            elif direction == 4:
                yield (0, i) in tile
            else:
                raise Exception("Invalid orientation", direction)

    return "".join("#" if t else "." for t in gen())


def all_edges(tiles):
    edges = {}

    for id, tile in tiles.items():
        for direction in range(1, 5):
            e = edge(tile, direction)
            if e in edges:
                edges[e].append((id, direction))
            # elif e[::-1] in edges:
            #     edges[e[::-1]].append((id, -direction))
            else:
                edges[e] = [(id, direction)]

    return edges


def map_neighbors(tiles):
    edges = all_edges(tiles)
    return {
        tile: [
            id
            for dir in range(1, 5)
            for id in (
                *(id for id, _ in edges.get(edge(tiles[tile], dir), [])),
                *(id for id, _ in edges.get(edge(tiles[tile], dir)[::-1], [])),
            )
            if id != tile
        ]
        for tile in tiles
    }


def find_corners(tiles):
    neighbors = map_neighbors(tiles)

    return [tile for tile, nbs in neighbors.items() if len(nbs) == 2]


def part_1():
    tiles = puzzle_input()

    p = 1
    for c in find_corners(tiles):
        p *= c
    assert 15405893262491 == p
