import functools

with open("input/2015/dec24.txt") as f:
    packages = sorted((int(line.strip()) for line in f.readlines()), reverse=True)
    assert len(set(packages)) == len(packages)


def valid_groups(w, packages):

    best_len = len(packages) + 1  # every package candidate will be better than this

    def groups_including(partial, rest):
        nonlocal best_len
        pw = sum(partial)
        if len(partial) > best_len or pw + sum(rest) < w:
            return
        if pw == w:
            best_len = min(len(partial), best_len)
            yield partial

        if pw < w:
            for p in rest:
                if pw + p <= w:
                    nxt = [*partial, p]
                    yield from groups_including(nxt, [r for r in rest if r < p])

    return list(groups_including([], packages))


def entanglement(packages):
    return functools.reduce(lambda a, b: a * b, packages, 1)


def best_entanglement(w, packages):
    return entanglement(
        sorted(valid_groups(w, packages), key=lambda g: (len(g), entanglement(g)))[0]
    )


def best_partitioning(n, packages):
    group_w = sum(packages) // n
    assert n * group_w == sum(packages)
    return best_entanglement(group_w, packages)


def part_1():
    assert 11266889531 == best_partitioning(3, packages)


def part_2():
    assert 77387711 == best_partitioning(4, packages)
