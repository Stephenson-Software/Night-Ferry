"""The first crossing's clock fires every fixed hour of the night and only
those: each turn is twenty minutes, four o'clock brings the captain down
unless Hanne already knows or the steward is keeping the secret, five
o'clock stops the ship only when both Hanne and Ingrid have chosen it, six
o'clock docks, and the notebook's calendar says the same night."""

import pytest

from nightferry import crossing, endings, facts, flags
from nightferry.state import (
    CAPTAIN_COMES_DOWN,
    DOCKING,
    HANNE_WAKES,
    LAST_ORDERS,
    SALOON_DARK,
    THE_LIGHT,
    TURN_MINUTES,
)

from conftest import FakeGame


def _game(minute=0, tonight=None):
    """A game on the first crossing at `minute`, with `tonight`'s flags set."""
    game = FakeGame()
    game.state.minute = minute
    game.state.flags.update(tonight or {})
    return game


def _justBefore(hour, tonight=None):
    """A game one turn before `hour`."""
    return _game(hour - TURN_MINUTES, tonight)


# --- the turn ---------------------------------------------------------------
def test_every_turn_costs_twenty_minutes():
    game = _game()
    outcome = crossing.advance(game, turns=2)
    assert game.state.minute == 2 * TURN_MINUTES
    assert outcome.lines == []
    assert not outcome.interrupted
    assert outcome.ending is None


@pytest.mark.parametrize(
    "hour, words",
    [
        (60, "Nine o'clock."),
        (LAST_ORDERS, "Eleven. Oskar pulls the grille down"),
        (SALOON_DARK, "One o'clock. The saloon lights go down"),
        (HANNE_WAKES, "Three. Hanne is awake"),
    ],
)
def test_each_quiet_hour_is_announced_once_on_the_turn_it_strikes(hour, words):
    game = _justBefore(hour)
    outcome = crossing.advance(game)
    assert len(outcome.lines) == 1
    assert outcome.lines[0].startswith(words)
    assert crossing.advance(game).lines == []


def test_a_night_that_has_ended_does_not_move_the_clock():
    game = _game(THE_LIGHT)
    game.state.ending = endings.OFF_THE_LIGHT
    outcome = crossing.advance(game, turns=3)
    assert game.state.minute == THE_LIGHT
    assert outcome.lines == []


# --- four o'clock -----------------------------------------------------------
@pytest.mark.parametrize(
    "tonight, comesDown",
    [
        ({}, True),
        ({flags.HANNE_KNOWS: True}, False),
        ({flags.KEPT_INGRIDS_SECRET: True}, False),
        ({flags.KEPT_INGRIDS_SECRET: True, flags.LETTER_DELIVERED: True}, True),
        ({flags.KEPT_INGRIDS_SECRET: False}, True),
    ],
)
def test_the_captain_comes_down_unless_hanne_knows_or_the_secret_is_kept(
    tonight, comesDown
):
    assert crossing.captainComesDown(_game(tonight=tonight).state) is comesDown


def test_four_oclock_takes_you_to_the_corridor_and_stops_a_longer_wait():
    game = _justBefore(CAPTAIN_COMES_DOWN)
    outcome = crossing.advance(game, turns=4)
    state = game.state
    assert state.minute == CAPTAIN_COMES_DOWN
    assert outcome.interrupted
    assert state.location == "corridor"
    assert state.flags[flags.AT_THE_DOOR] is True
    assert state.flags[flags.HANNE_KNOWS] is True
    for factId in (facts.THE_ASHES, facts.THE_CAPTAIN):
        assert state.knows(factId)


def test_at_the_door_tove_brings_the_letter_nobody_carried():
    game = _justBefore(CAPTAIN_COMES_DOWN)
    text = crossing.advance(game).lines[0]
    state = game.state
    assert "Tove Ness, the nurse, has been listening" in text
    assert "Ingrid reads it aloud, to Hanne" in text
    assert state.knows(facts.THE_LETTER)
    assert state.knows(facts.WHAT_MAREN_WROTE)
    assert state.flags[flags.LETTER_DELIVERED] is True


def test_at_the_door_the_letter_in_your_pocket_goes_to_the_captain():
    game = _justBefore(
        CAPTAIN_COMES_DOWN,
        {flags.TOVE_GAVE_LETTER: True, flags.READ_THE_LETTER: True},
    )
    text = crossing.advance(game).lines[0]
    state = game.state
    assert "You have Maren's letter in your inside pocket." in text
    assert "Tove Ness" not in text
    assert not state.knows(facts.THE_LETTER)
    assert state.flags[flags.LETTER_DELIVERED] is True
    assert state.flags[flags.INGRID_SAW_THE_SEAL] is True


def test_at_the_door_a_delivered_letter_is_not_read_again():
    game = _justBefore(
        CAPTAIN_COMES_DOWN,
        {flags.KEPT_INGRIDS_SECRET: False, flags.LETTER_DELIVERED: True},
    )
    text = crossing.advance(game).lines[0]
    assert "Ingrid reads it aloud" not in text
    assert "Tove Ness" not in text


def test_at_the_door_hanne_asks_what_she_was_prepared_to_ask():
    unprepared = crossing.advance(_justBefore(CAPTAIN_COMES_DOWN)).lines[0]
    assert "'That's my mother's name on that door,' Hanne says." in unprepared
    prepared = crossing.advance(
        _justBefore(CAPTAIN_COMES_DOWN, {flags.HANNE_PREPARED: True})
    ).lines[0]
    assert "'Dr Fenn says she went somewhere every month" in prepared
    assert "That's my mother's name" not in prepared


def test_at_the_door_ingrid_finds_gus_asleep_in_six_if_you_let_him_in():
    assert "Gus Tamm is asleep on the bunk" in (
        crossing.advance(
            _justBefore(CAPTAIN_COMES_DOWN, {flags.LET_GUS_IN: True})
        ).lines[0]
    )
    assert "Gus Tamm" not in crossing.advance(_justBefore(CAPTAIN_COMES_DOWN)).lines[0]


def test_four_oclock_is_silent_when_the_steward_keeps_the_secret():
    game = _justBefore(CAPTAIN_COMES_DOWN, {flags.KEPT_INGRIDS_SECRET: True})
    outcome = crossing.advance(game)
    assert outcome.lines == []
    assert not outcome.interrupted
    assert game.state.location == "saloon"
    assert flags.AT_THE_DOOR not in game.state.flags


# --- five o'clock -----------------------------------------------------------
def test_the_ship_stops_off_the_light_when_hanne_chose_it_and_ingrid_will():
    game = _justBefore(
        THE_LIGHT,
        {
            flags.HANNE_KNOWS: True,
            flags.HANNE_CHOSE_LIGHT: True,
            flags.INGRID_WILL_STOP: True,
        },
    )
    outcome = crossing.advance(game, turns=3)
    assert outcome.ending == endings.OFF_THE_LIGHT
    assert game.state.ending == endings.OFF_THE_LIGHT
    assert game.state.location == "deck"
    assert game.state.minute == THE_LIGHT
    assert outcome.lines[0].startswith("Five o'clock. The engines stop.")


def test_the_light_goes_by_when_nobody_asked_the_captain_to_stop():
    game = _justBefore(
        THE_LIGHT, {flags.HANNE_KNOWS: True, flags.HANNE_CHOSE_LIGHT: True}
    )
    outcome = crossing.advance(game)
    assert outcome.ending is None
    assert not game.state.over
    assert "Nobody asked the captain to stop, and the ship does not stop." in (
        outcome.lines[0]
    )


@pytest.mark.parametrize("choseLight", [None, False])
def test_the_light_goes_by_quietly_when_hanne_did_not_choose_it(choseLight):
    tonight = {flags.HANNE_KNOWS: True, flags.INGRID_WILL_STOP: True}
    if choseLight is not None:
        tonight[flags.HANNE_CHOSE_LIGHT] = choseLight
    outcome = crossing.advance(_justBefore(THE_LIGHT, tonight))
    assert outcome.ending is None
    assert outcome.lines == [
        "Five o'clock. The Halde light comes abeam to port and goes by, and the "
        "sky behind the island goes from black to grey."
    ]


# --- six o'clock ------------------------------------------------------------
@pytest.mark.parametrize(
    "tonight, ending",
    [
        ({}, endings.KEPT_CROSSING),
        ({flags.HANNE_KNOWS: True}, endings.BESIDE_ARNE),
        ({flags.HANNE_KNOWS: True, flags.AT_THE_DOOR: True}, endings.AT_THE_DOOR),
    ],
)
def test_six_oclock_docks_at_halde_and_comes_to_an_ending(tonight, ending):
    game = _justBefore(DOCKING, tonight)
    outcome = crossing.advance(game, turns=3)
    assert outcome.ending == ending
    assert game.state.ending == ending
    assert game.state.location == "deck"
    assert game.state.minute == DOCKING
    assert outcome.lines[0].startswith("Six o'clock. Halde.")


# --- the notebook -----------------------------------------------------------
def test_the_calendar_lists_the_fixed_hours_but_not_four_oclock():
    assert crossing.calendar(_game().state) == [
        ("11:00 pm", "The bar shuts."),
        ("1:00 am", "The saloon goes dark for the sleepers."),
        ("5:00 am", "The Halde light, abeam to port."),
        ("6:00 am", "Halde. The ramp goes down."),
    ]


def test_the_calendar_says_the_captain_will_stop_once_she_has_agreed():
    state = _game(tonight={flags.INGRID_WILL_STOP: True}).state
    assert crossing.calendar(state)[2] == (
        "5:00 am",
        "The Halde light. The captain will stop the ship.",
    )
    state.ending = endings.OFF_THE_LIGHT
    assert crossing.calendar(state)[2] == ("5:00 am", "The Halde light, abeam to port.")
