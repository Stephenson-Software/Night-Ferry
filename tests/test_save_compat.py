"""Saves written by Night Ferry 0.1.0 - before the last night boat - still
load, describe themselves, play on, and sail the last boat.

The fixtures in tests/fixtures/saves-0.1.0 were written by 0.1.0's own
save() (see make_saves.py there); they are schema version 1, with no
"crossing" and no "past". Nothing in them may be lost or changed by loading
them, and the first save after loading writes them back as version 2."""

import json
import os

import pytest

from tak.saves import validateAgainstSchema

from nightferry import endings, facts, flags
from nightferry.game import describeSlot, slotMetadata
from nightferry.lastboat import endings as lastEndings
from nightferry.state import LAST_BOAT, SAVE_VERSION, State, migrate

from conftest import FIXTURES
from routes import CANONICAL, LAST_DO_NOTHING_UNTIL_FIVE, SAIL

ENDED = {
    "off_the_light": endings.OFF_THE_LIGHT,
    "beside_arne": endings.BESIDE_ARNE,
    "at_the_door": endings.AT_THE_DOOR,
    "kept_crossing": endings.KEPT_CROSSING,
    "kept_letter_in_pocket": endings.KEPT_CROSSING,
}


def _fixture(name):
    with open(os.path.join(FIXTURES, name + ".json")) as f:
        return json.load(f)


def _onDisk(path):
    with open(path) as f:
        return json.load(f)


def test_the_fixtures_really_are_0_1_0_saves():
    for name in list(ENDED) + ["mid_crossing"]:
        data = _fixture(name)
        assert data["version"] == 1, name
        assert "crossing" not in data and "past" not in data, name
        # They validate against the current schema as they are.
        validateAgainstSchema(data, "schemas/save.json")


def test_migration_adds_and_never_changes_or_drops():
    for name in list(ENDED) + ["mid_crossing"]:
        old = _fixture(name)
        new = migrate(old)
        assert new["version"] == SAVE_VERSION == 2
        assert new["crossing"] == 1 and new["past"] is None
        for key, value in old.items():
            if key != "version":
                assert new[key] == value, (name, key)
        assert old["version"] == 1  # the input is not modified
        validateAgainstSchema(new, "schemas/save.json")
        # Through State and back out, everything 0.1.0 wrote is still there.
        out = State.fromDict(old).toDict()
        for key, value in old.items():
            if key != "version":
                assert out[key] == value, (name, key)


def test_the_slot_menu_describes_0_1_0_saves_as_it_did():
    assert (
        describeSlot(slotMetadata("s", _fixture("mid_crossing"))) == "9:40 pm, 9 known"
    )
    assert (
        describeSlot(slotMetadata("s", _fixture("off_the_light")))
        == "docked - off the light, 16 known"
    )
    assert (
        describeSlot(slotMetadata("s", _fixture("kept_crossing")))
        == "docked - the kept crossing, 4 known"
    )


def test_a_mid_crossing_0_1_0_save_loads_and_plays_to_its_ending(scripted, installSave):
    path = installSave("mid_crossing")
    old = _fixture("mid_crossing")
    rest = CANONICAL[CANONICAL.index("Go out on the open deck") :]
    game, ui = scripted(["Load Slot 1"] + rest)
    assert ui.menus[0][1][0] == "Load Slot 1 (9:40 pm, 9 known)"
    # Loaded exactly as written, before anything is done.
    state = game.state
    assert game.failedLoad is None
    assert state.crossing == 1 and state.past is None
    assert state.minute == old["minute"] and state.location == old["location"]
    assert state.facts == old["facts"] and state.flags == old["flags"]
    assert state.factMinutes == old["factMinutes"]
    game.play()
    assert game.state.ending == endings.OFF_THE_LIGHT
    assert len(game.state.facts) == 16
    assert ui.saw("WHAT HAPPENED. At five o'clock the Kittiwake stopped her engines")
    # Written back as version 2, valid, and still the same crossing.
    data = _onDisk(path)
    assert data["version"] == 2 and data["crossing"] == 1 and data["past"] is None
    validateAgainstSchema(data, "schemas/save.json")
    assert data["flags"][flags.FENN_TELLS] is True  # chosen under 0.1.0, kept


@pytest.mark.parametrize("name", sorted(ENDED))
def test_an_ended_0_1_0_save_loads_rereads_and_quits_unchanged(
    scripted, installSave, name
):
    path = installSave(name)
    old = _fixture(name)
    game, ui = scripted(["Load Slot 1", "Read the last page again", "Quit"])
    game.play()
    assert game.failedLoad is None
    assert game.state.ending == ENDED[name]
    expected = State.fromDict(old)
    assert ui.dialogues[-1] == endings.text(expected)
    assert not ui.saw("This save could not be read")
    # Quitting saved it as version 2 with every field 0.1.0 wrote intact.
    data = _onDisk(path)
    assert data["version"] == 2 and data["crossing"] == 1
    for key, value in old.items():
        if key != "version":
            assert data[key] == value, key


@pytest.mark.parametrize("name", sorted(ENDED))
def test_an_ended_0_1_0_save_sails_the_last_boat(scripted, installSave, name):
    path = installSave(name)
    old = _fixture(name)
    script = (
        ["Load Slot 1", SAIL]
        + LAST_DO_NOTHING_UNTIL_FIVE
        + [
            "Let them go.",
            "Go along the cabin corridor",
            "Sit in the steward's pantry",  # 6:00, Brekka
            "Read October's last page",
            "Quit",
        ]
    )
    game, ui = scripted(script)
    game.play()
    state = game.state
    assert state.crossing == LAST_BOAT
    assert state.ending == lastEndings.OVER_THE_SIDE
    # October, exactly as 0.1.0 left it.
    assert state.past == {
        "ending": old["ending"],
        "facts": old["facts"],
        "flags": old["flags"],
    }
    assert ui.saw("OCTOBER - %s." % endings.NAMES[old["ending"]])
    assert ui.saw("WHERE THE CAPTAIN WAS GOING. Away.")
    data = _onDisk(path)
    validateAgainstSchema(data, "schemas/save.json")
    assert data["crossing"] == 2 and data["past"]["flags"] == old["flags"]

    # And the two-crossing save loads again.
    game2, ui2 = scripted(["Load Slot 1", "Quit"])
    assert ui2.menus[0][1][0].startswith(
        "Load Slot 1 (last boat, docked - over the side"
    )
    game2.play()
    assert game2.state.past == state.past
    assert game2.state.ending == lastEndings.OVER_THE_SIDE


def test_a_last_boat_save_mid_crossing_resumes(scripted, installSave):
    installSave("at_the_door")
    script = [
        "Load Slot 1",
        SAIL,
        "Ask the purser about cabin 6",
        "What's the story with cabin 6 tonight",
        "[Back]",
        "Quit",
    ]
    game, ui = scripted(script)
    game.play()
    assert game.state.minute == 20
    game2, ui2 = scripted(["Load Slot 1", "Quit"])
    assert ui2.menus[0][1][0] == "Load Slot 1 (last boat, 8:20 pm, 1 known)"
    game2.play()
    assert game2.state.crossing == LAST_BOAT
    assert game2.state.facts == ["six_tonight"]
    assert game2.state.past["ending"] == endings.AT_THE_DOOR
    # The header counts the last boat's facts.
    assert "Known: 1/13" in [c["text"] for c in ui2.headers[-1]["chips"]]


def test_a_last_boat_save_drops_facts_the_game_no_longer_has():
    state = State()
    state.ending = endings.AT_THE_DOOR
    state.learn(facts.CABIN_SIX)
    state.sailAgain()
    state.learn("six_tonight")
    data = json.loads(json.dumps(state.toDict()))
    data["facts"].append("retired_fact")
    data["past"]["facts"].append("retired_fact")
    again = State.fromDict(data)
    assert again.facts == ["six_tonight"]
    assert again.past["facts"] == [facts.CABIN_SIX]


def test_sailing_again_is_only_from_an_ended_first_crossing():
    state = State()
    with pytest.raises(ValueError):
        state.sailAgain()
    state.ending = endings.KEPT_CROSSING
    state.sailAgain()
    with pytest.raises(ValueError):
        state.sailAgain()
