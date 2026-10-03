"""Achievements reach tak.arcade.unlock when they are earned - by scripted
routes through both crossings, and by loading a save made before they
existed - and only once a run. tak.arcade is mocked: the real one is a no-op
outside the browser."""

import re

import pytest

from tak import arcade

from nightferry import achievements

from routes import (
    CANONICAL,
    DO_NOTHING,
    KEPT,
    LAST_CANONICAL,
    LAST_DO_NOTHING_UNTIL_FIVE,
    PANTRY,
    lastBoatAfter,
)

TO_BREKKA = ["Go along the cabin corridor", PANTRY]


@pytest.fixture
def unlocked(monkeypatch):
    calls = []
    monkeypatch.setattr(
        arcade, "unlock", lambda achievementId: calls.append(achievementId)
    )
    return calls


def _run(scripted, script):
    game, ui = scripted(script)
    game.play()
    return game


def test_ids_are_what_arcade_accepts_and_unique():
    for a in achievements.ACHIEVEMENTS:
        assert arcade.ID_PATTERN.match(a["id"]), a["id"]
        assert a["title"] and a["description"]
        assert isinstance(a["hidden"], bool)
    assert len(set(achievements.IDS)) == len(achievements.IDS)
    # Every ending on both crossings has one.
    for ending in (
        "off-the-light",
        "beside-arne",
        "at-the-door",
        "kept-crossing",
        "on-which-days",
        "the-column",
        "over-the-side",
        "kept-from-the-record",
    ):
        assert "ending-" + ending in achievements.IDS


def test_spoilers_are_hidden_and_titles_do_not_name_the_answer():
    for a in achievements.ACHIEVEMENTS:
        if a["id"].startswith("ending-"):
            assert a["hidden"], a["id"]
        assert not re.search(r"Ingrid|Maren|captain's secret", a["title"]), a["id"]


def test_the_canonical_crossings_unlock_their_endings_and_discoveries(
    scripted, unlocked
):
    _run(scripted, lastBoatAfter(CANONICAL) + LAST_CANONICAL)
    assert len(unlocked) == len(set(unlocked))  # once a run
    for earned in (
        "first-crossing",
        "ending-off-the-light",
        "all-sixteen",
        "before-four",
        "the-last-night-boat",
        "ending-on-which-days",
        "all-thirteen",
        "the-grieg",
        "master-below",
    ):
        assert earned in unlocked, earned
    # Opened six in October: no "one rule". Never carried the bag.
    assert "one-rule" not in unlocked and "her-hour" not in unlocked
    assert "ending-beside-arne" not in unlocked
    # Unlocked when earned, in play order: October's ending before the last boat.
    assert unlocked.index("ending-off-the-light") < unlocked.index(
        "the-last-night-boat"
    )


def test_the_other_first_crossing_endings(scripted, unlocked):
    _run(scripted, DO_NOTHING)
    assert {"first-crossing", "ending-at-the-door", "one-rule"} <= set(unlocked)
    assert "before-four" not in unlocked
    del unlocked[:]
    _run(scripted, KEPT)
    assert {"ending-kept-crossing", "her-hour", "one-rule", "before-four"} <= set(
        unlocked
    )
    del unlocked[:]
    churchyard = list(CANONICAL)
    churchyard[
        churchyard.index("Do what she asked. The light.")
    ] = "Take her home to the churchyard"
    churchyard[-1:] = [PANTRY, "Quit"]
    _run(scripted, churchyard)
    assert "ending-beside-arne" in unlocked


@pytest.mark.parametrize(
    "atTheRail,earned",
    [
        ("Let them go.", "ending-over-the-side"),
        ("Take them with you", "ending-kept-from-the-record"),
    ],
)
def test_the_last_boat_rail_endings(scripted, unlocked, atTheRail, earned):
    _run(
        scripted,
        lastBoatAfter(DO_NOTHING)
        + LAST_DO_NOTHING_UNTIL_FIVE
        + [atTheRail]
        + TO_BREKKA
        + ["Quit"],
    )
    assert earned in unlocked and "the-last-night-boat" in unlocked


def test_the_column_ending(scripted, unlocked):
    from test_lastboat import KEPT_THEN_COLUMN

    _run(scripted, KEPT_THEN_COLUMN)
    assert "ending-the-column" in unlocked


def test_a_save_made_before_achievements_is_credited_on_load(
    scripted, unlocked, installSave
):
    installSave("off_the_light")
    scripted(["Load Slot 1", "Quit"])  # constructing the game loads it
    assert {"first-crossing", "ending-off-the-light", "all-sixteen"} <= set(unlocked)
    assert "the-last-night-boat" not in unlocked


def test_every_achievement_is_earnable_by_some_route(scripted, unlocked, installSave):
    from test_lastboat import KEPT_THEN_COLUMN

    churchyard = list(CANONICAL)
    churchyard[
        churchyard.index("Do what she asked. The light.")
    ] = "Take her home to the churchyard"
    churchyard[-1:] = [PANTRY, "Quit"]
    for script in (
        lastBoatAfter(CANONICAL) + LAST_CANONICAL,
        KEPT_THEN_COLUMN,
        churchyard,
        lastBoatAfter(DO_NOTHING)
        + LAST_DO_NOTHING_UNTIL_FIVE
        + ["Let them go."]
        + TO_BREKKA
        + ["Quit"],
        lastBoatAfter(DO_NOTHING)
        + LAST_DO_NOTHING_UNTIL_FIVE
        + ["Take them"]
        + TO_BREKKA
        + ["Quit"],
    ):
        _run(scripted, script)
    assert set(unlocked) == set(achievements.IDS)


def test_a_failing_arcade_never_stops_play(scripted, monkeypatch):
    def broken(achievementId):
        raise RuntimeError("arcade is down")

    monkeypatch.setattr(arcade, "unlock", broken)
    game = _run(scripted, DO_NOTHING)
    assert game.state.ending == "at_the_door"
