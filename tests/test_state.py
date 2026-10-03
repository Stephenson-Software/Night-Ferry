import json
import os
import re

from tak.saves import validateAgainstSchema

from nightferry import facts, flags
from nightferry.game import describeSlot, slotMetadata
from nightferry.state import (
    CAPTAIN_COMES_DOWN,
    DOCKING,
    HANNE_WAKES,
    SALOON_DARK,
    WORLD_SEED,
    State,
    formatClock,
)
from nightferry.scenes.saloon import SALOON_SIGHTS
from nightferry.scenes.deck import SEA


def test_a_fresh_crossing_validates_and_round_trips():
    state = State()
    data = state.toDict()
    validateAgainstSchema(data, "schemas/save.json")
    again = State.fromDict(json.loads(json.dumps(data)))
    assert again.toDict() == data


def test_a_full_state_round_trips_through_the_schema():
    state = State()
    state.minute = 340
    state.learn(facts.CABIN_SIX)
    state.flags[flags.KEPT_INGRIDS_SECRET] = True
    state.ending = "kept_crossing"
    state.draw(SEA)
    data = json.loads(json.dumps(state.toDict()))
    validateAgainstSchema(data, "schemas/save.json")
    assert State.fromDict(data).toDict() == state.toDict()


def test_the_clock_reads_like_a_ships_clock():
    assert formatClock(0) == "8:00 pm"
    assert formatClock(20) == "8:20 pm"
    assert formatClock(4 * 60) == "12:00 am"
    assert formatClock(SALOON_DARK) == "1:00 am"
    assert formatClock(DOCKING) == "6:00 am"
    state = State()
    assert state.hoursToDock == 10
    state.minute = 20
    assert state.hoursToDock == 10
    state.minute = 60
    assert state.hoursToDock == 9
    state.minute = DOCKING - 20
    assert state.hoursToDock == 1


def test_the_nights_people_are_where_the_hour_puts_them():
    state = State()
    assert not state.hanneAsleep and not state.fennInHisCabin
    state.minute = SALOON_DARK
    assert state.hanneAsleep and state.fennInHisCabin and state.hanneAsleepForAnHour
    state.minute = HANNE_WAKES - 40
    assert state.hanneAsleep and not state.hanneAsleepForAnHour
    state.minute = HANNE_WAKES
    assert not state.hanneAsleep and state.lightInSight
    state.minute = CAPTAIN_COMES_DOWN
    assert not state.lightPassed


def test_learning_records_the_time_and_refuses_unknown_facts():
    state = State()
    state.minute = 100
    assert state.learn(facts.CABIN_SIX) is True
    assert state.learn(facts.CABIN_SIX) is False
    assert state.learnedAt(facts.CABIN_SIX) == "9:40 pm"
    try:
        state.learn("the_kraken")
    except ValueError:
        pass
    else:
        raise AssertionError("unknown fact accepted")


def test_loading_drops_facts_the_game_no_longer_has():
    data = State().toDict()
    data["facts"] = [facts.CABIN_SIX, "retired_fact"]
    data["factMinutes"] = {facts.CABIN_SIX: 20, "retired_fact": 40}
    state = State.fromDict(data)
    assert state.facts == [facts.CABIN_SIX]
    assert state.factMinutes == {facts.CABIN_SIX: 20}


def test_each_draw_is_a_function_of_the_seed_and_its_index_only():
    first = State()
    a = [first.draw(SALOON_SIGHTS) for _ in range(6)]
    reloaded = State.fromDict(State().toDict())
    for _ in range(3):
        reloaded.draw(SEA)  # a different population, the same indices
    b = [reloaded.draw(SALOON_SIGHTS) for _ in range(3)]
    assert a[3:] == b
    assert first.rngDraws == 6
    assert WORLD_SEED == 2007
    # A population that is not a power of two, a hundred long: still
    # position-faithful across a save and load.
    big = list(range(100))
    one = State()
    seq = [one.draw(big) for _ in range(10)]
    two = State()
    for _ in range(5):
        two.draw(big)
    two = State.fromDict(json.loads(json.dumps(two.toDict())))
    assert [two.draw(big) for _ in range(5)] == seq[5:]


def test_the_slot_menu_survives_saves_that_parse_but_are_not_saves():
    for bad in (
        {"minute": "ten"},
        {"minute": None, "facts": []},
        {"minute": 20, "facts": 7},
        {"minute": True, "facts": []},
        {},
        {"minute": 20, "flags": [], "facts": []},
    ):
        metadata = slotMetadata("slot", bad)
        assert describeSlot(metadata)
    good = slotMetadata("slot", State().toDict())
    assert describeSlot(good) == "8:00 pm, 0 known"


def test_no_person_or_scene_gates_on_the_clock():
    """What opens a line or a menu row is what you know, a flag, or a state
    property - never a comparison against the minute, and never a fixed
    hour carried out of state.py. Only crossing.py fires the hours."""
    root = os.path.join(os.path.dirname(__file__), "..", "src", "nightferry")
    paths = [os.path.join(root, "people.py")]
    scenes = os.path.join(root, "scenes")
    paths += [os.path.join(scenes, n) for n in os.listdir(scenes) if n.endswith(".py")]
    compared = re.compile(
        r"\.minute\b\s*(?:[<>]=?|[=!]=|\bin\b)|(?:[<>]=?|[=!]=)\s*\w+\.minute\b"
    )
    hours = re.compile(
        r"\b(?:LAST_ORDERS|SALOON_DARK|HANNE_WAKES|CAPTAIN_COMES_DOWN|THE_LIGHT|DOCKING|OSKAR_ROUNDS|RASKE_ON_THE_PHONE)\b"
    )
    for path in paths:
        with open(path) as f:
            source = f.read()
        name = os.path.relpath(path, root)
        assert not compared.search(source), (name, compared.search(source).group())
        assert not hours.search(source), (name, hours.search(source).group())


def test_every_flag_the_game_sets_is_declared_in_one_place():
    """Every flags.NAME the source writes is listed in flags.ALL, and no
    string key is written to - or read from - state.flags directly."""
    root = os.path.join(os.path.dirname(__file__), "..", "src", "nightferry")
    used = set()
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if not name.endswith(".py") or name == "flags.py":
                continue
            with open(os.path.join(dirpath, name)) as f:
                source = f.read()
            assert 'flags["' not in source and "flags['" not in source, name
            assert 'flags.get("' not in source and "flags.get('" not in source, name
            used.update(re.findall(r"flags\.([A-Z_]+)\b", source))
            used.update(re.findall(r"state\.flags\[([A-Z_]+)\]", source))
            used.update(re.findall(r"state\.flags\.get\(([A-Z_]+)\)", source))
    declared = {name for name in dir(flags) if name.isupper() and name != "ALL"}
    assert used <= declared, used - declared
    assert set(getattr(flags, n) for n in declared) == set(flags.ALL)
    assert len(set(flags.ALL)) == len(flags.ALL)
