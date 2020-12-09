import dataclasses
import heapq
import time


@dataclasses.dataclass
class Spell:
    id: str
    cost: int
    damage: int = dataclasses.field(default=0)
    armor: int = dataclasses.field(default=0)
    heal: int = dataclasses.field(default=0)
    recharge: int = dataclasses.field(default=0)
    timer: int = dataclasses.field(default=0)

    def apply(self, state):
        if self.timer == 0:
            # immediate spell
            state.boss_hp -= self.damage
            state.player_hp += self.heal
        else:
            effect = Effect(
                id=self.id,
                timer=self.timer,
                damage=self.damage,
                armor=self.armor,
                recharge=self.recharge,
            )
            state.effects = (
                (effect,) if state.effects == () else (*state.effects, effect)
            )


@dataclasses.dataclass
class Effect:
    id: str
    timer: int
    damage: int
    armor: int
    recharge: int

    def apply(self, state):
        state.boss_hp -= self.damage
        state.player_mana += self.recharge
        self.timer -= 1

    @property
    def is_active(self):
        return self.timer > 0

    def clone(self):
        return Effect(
            id=self.id,
            timer=self.timer,
            damage=self.damage,
            armor=self.armor,
            recharge=self.recharge,
        )


def all_spells():
    return [
        Spell(id="Magic Missile", cost=53, damage=4),
        Spell(id="Drain", cost=73, damage=2, heal=2),
        Spell(id="Shield", cost=113, armor=7, timer=6),
        Spell(id="Poison", cost=173, damage=3, timer=6),
        Spell(id="Recharge", cost=229, recharge=101, timer=5),
    ]


@dataclasses.dataclass(order=True)
class GameState:
    player_hp: int = dataclasses.field(compare=False)
    player_mana: int = dataclasses.field(compare=False)
    boss_hp: int = dataclasses.field(compare=True)
    boss_damage: int = dataclasses.field(compare=False)
    effects: tuple[Effect, ...] = dataclasses.field(
        default_factory=tuple, compare=False
    )
    mana_spent: int = dataclasses.field(default=0, compare=False)
    path: str = dataclasses.field(default="", compare=False)

    @property
    def player_armor(self):
        return sum(s.armor for s in self.effects if s.is_active)

    def available_spells(self):
        active_spells = set(s.id for s in self.effects)
        return tuple(
            spell
            for spell in all_spells()
            if spell.id not in active_spells and spell.cost <= self.player_mana
        )

    def apply_effects(self):
        effect_wears_out = False
        for effect in self.effects:
            effect.apply(self)
            effect_wears_out = effect_wears_out or not effect.is_active

        if effect_wears_out:
            self.effects = tuple(effect for effect in self.effects if effect.is_active)

    def boss_move(self):
        damage = max(self.boss_damage - self.player_armor, 1)
        self.player_hp -= damage

    def play_move(self, spell: Spell):
        spell.apply(self)
        self.player_mana -= spell.cost
        self.mana_spent += spell.cost

    def clone(self, path):
        return GameState(
            path=self.path + path,
            player_hp=self.player_hp,
            player_mana=self.player_mana,
            boss_hp=self.boss_hp,
            boss_damage=self.boss_damage,
            effects=tuple(e.clone() for e in self.effects),
            mana_spent=self.mana_spent,
        )


def play(hard_mode):
    q = []
    heapq.heapify(q)
    best_win = None

    heapq.heappush(
        q,
        (
            GameState(
                player_hp=50,
                player_mana=500,
                boss_hp=71,
                boss_damage=10,
            )
        ),
    )

    while q:
        state = heapq.heappop(q)

        for spell in state.available_spells():
            if best_win and best_win < state.mana_spent + spell.cost:
                log(
                    state.path,
                    spell.id[0],
                    "abort",
                    best_win,
                    "<",
                    state.mana_spent,
                    "+",
                    spell.cost,
                )
                continue

            s = state.clone(spell.id[0])

            if hard_mode:
                s.player_hp -= 1
                if s.player_hp <= 0:
                    log(state.path, spell.id[0], "loss")
                    continue

            s.play_move(spell)

            if s.boss_hp <= 0:
                best_win = min(s.mana_spent, best_win or 1e8)
                log(state.path, spell.id[0], "win", s.mana_spent)
                continue

            s.apply_effects()

            if s.boss_hp <= 0:
                best_win = min(s.mana_spent, best_win or 1e8)
                log(state.path, spell.id[0], "win", s.mana_spent)
                continue

            s.boss_move()

            if s.player_hp <= 0:
                log(state.path, spell.id[0], "loss")
                continue

            s.apply_effects()
            if s.boss_hp <= 0:
                best_win = min(s.mana_spent, best_win or 1e8)
                log(state.path, spell.id[0], "win", s.mana_spent)
                continue

            heapq.heappush(q, s)

    return best_win


def log(*args):
    # with open("paths.txt", "a") as f:
    #     print(*args, file=f)
    pass


def part_1():
    log()
    start = time.perf_counter()
    best_win = play(hard_mode=False)
    t = time.perf_counter() - start
    assert 1824 == best_win
    print(f" {t:.3} s", end="")


def part_2():
    start = time.perf_counter()
    best_win = play(hard_mode=True)
    t = time.perf_counter() - start
    assert 1937 == best_win
    print(f" {t:.3} s", end="")


if __name__ == "__main__":
    part_1()
