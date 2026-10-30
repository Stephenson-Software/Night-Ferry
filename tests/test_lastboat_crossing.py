"""The last night boat's clock fires every fixed hour of the night and only
those: each turn is twenty minutes, the Halde light goes astern at twenty to
nine and remembers October, midnight sends the captain down to six, five
o'clock is the failure-proof answer at the stern rail unless the books are
already settled, six o'clock docks at Brekka, and the notebook's calendar
says the same night."""

import pytest

from nightferry import endings, flags
from nightferry.lastboat import crossing
from nightferry.lastboat import endings as lastEndings
from nightferry.lastboat import facts
from nightferry.state import (
    LB_BREKKA_LIGHTS,
    LB_DOCKING,
    LB_LAST_ORDERS,
    LB_LIGHT_ASTERN,
    LB_SALOON_DARK,
    LB_THE_STERN,
    LB_THE_WATCH,
    TURN_MINUTES,
)

from conftest import FakeGame


def _lastBoat(minute=0, tonight=None, october=endings.KEPT_CROSSING):
    """A game on the last boat after a first crossing that ended `october`,
    at `minute`, with `tonight`'s flags set."""
    game = FakeGame()
    state = game.state
    state.ending = october
    state.sailAgain()
    state.minute = minute
    state.flags.update(tonight or {})
    return game


def _justBefore(hour, tonight=None, october=endings.KEPT_CROSSING):
    """A game one turn before `hour`."""
    return _lastBoat(hour - TURN_MINUTES, tonight, october)


# --- the turn -----------------------------------------------------------------
def test_every_turn_costs_twenty_minutes():
    game = _lastBoat(60)
    outcome = crossing.advance(game, turns=2)
    assert game.state.minute == 60 + 2 * TURN_MINUTES
    assert outcome.lines == []
    assert not outcome.interrupted
    assert outcome.ending is None


@pytest.mark.parametrize(
    "hour, words",
    [
        (LB_LAST_ORDERS, "Eleven. Oskar pulls the grille down"),
        (LB_SALOON_DARK, "One o'clock. The saloon lights go down"),
        (LB_BREKKA_LIGHTS, "Four. Off the bow, low and orange, Brekka."),
    ],
)
def test_each_quiet_hour_is_announced_once_on_the_turn_it_strikes(hour, words):
    game = _justBefore(hour)
    outcome = crossing.advance(game)
    assert len(outcome.lines) == 1
    assert outcome.lines[0].startswith(words)
    assert crossing.advance(game).lines == []


def test_a_night_that_has_ended_does_not_move_the_clock():
    game = _lastBoat(LB_THE_STERN)
    game.state.ending = lastEndings.OVER_THE_SIDE
    outcome = crossing.advance(game, turns=3)
    assert game.state.minute == LB_THE_STERN
    assert outcome.lines == []


# --- twenty to nine -----------------------------------------------------------
def test_the_halde_light_goes_astern_at_twenty_to_nine():
    game = _justBefore(LB_LIGHT_ASTERN)
    outcome = crossing.advance(game)
    assert len(outcome.lines) == 1
    assert outcome.lines[0].startswith("Twenty to nine. The Halde light")
    assert "in October, Maren went into the water" not in outcome.lines[0]


def test_the_halde_light_remembers_october_off_the_light():
    game = _justBefore(LB_LIGHT_ASTERN, october=endings.OFF_THE_LIGHT)
    outcome = crossing.advance(game)
    assert "in October, Maren went into the water" in outcome.lines[0]


# --- midnight -----------------------------------------------------------------
def test_at_midnight_the_captain_gives_the_watch_and_goes_down_to_six():
    game = _justBefore(LB_THE_WATCH)
    outcome = crossing.advance(game)
    assert len(outcome.lines) == 1
    assert outcome.lines[0].startswith("Midnight.")
    assert "she goes below to cabin 6" in outcome.lines[0]
    assert "I always knew where you were" not in outcome.lines[0]
    assert not outcome.interrupted


@pytest.mark.parametrize("perTells, said", [(True, True), (False, False)])
def test_at_midnight_per_says_what_he_knew_only_if_he_chose_to(perTells, said):
    game = _justBefore(LB_THE_WATCH, {flags.PER_TELLS_HER: perTells})
    outcome = crossing.advance(game)
    assert ("I always knew where you were" in outcome.lines[0]) == said


# --- five o'clock -------------------------------------------------------------
def test_five_oclock_brings_the_steward_to_the_stern_and_tells_all_of_it():
    game = _justBefore(LB_THE_STERN)
    outcome = crossing.advance(game, turns=3)
    state = game.state
    assert outcome.interrupted
    assert state.minute == LB_THE_STERN
    assert state.location == "deck"
    assert state.flags[flags.AT_THE_STERN] is True
    assert state.flags[flags.INGRID_TOLD_YOU_TONIGHT] is True
    for factId in (facts.THE_STOP, facts.THE_BOX, facts.THE_MARGINS, facts.THE_ANSWER):
        assert state.knows(factId)
    assert "Per sends for you" in outcome.lines[0]
    assert "a single south" in outcome.lines[0]
    assert "'Happy. - M.'" in outcome.lines[0]
    assert flags.BOOKS_OVERBOARD not in state.flags
    assert outcome.ending is None


def test_five_oclock_does_not_tell_it_twice_if_she_already_told_you():
    game = _justBefore(LB_THE_STERN, {flags.INGRID_TOLD_YOU_TONIGHT: True})
    outcome = crossing.advance(game)
    assert "Per sends for you" in outcome.lines[0]
    assert "a single south" not in outcome.lines[0]
    assert "'Happy. - M.'" in outcome.lines[0]


def test_five_oclock_lets_the_books_go_when_you_told_her_to_do_what_she_came_to_do():
    game = _justBefore(LB_THE_STERN, {flags.INGRID_GIVES_BOOKS: False})
    outcome = crossing.advance(game)
    assert game.state.flags[flags.BOOKS_OVERBOARD] is True
    assert "You said to do what I came to do" in outcome.lines[0]


def test_five_oclock_gives_hanne_the_books_at_the_rail_when_ingrid_agreed():
    game = _justBefore(LB_THE_STERN, {flags.INGRID_GIVES_BOOKS: True})
    outcome = crossing.advance(game)
    state = game.state
    assert outcome.interrupted
    assert state.location == "deck"
    assert state.flags[flags.BOOKS_TO_HANNE] is True
    assert flags.AT_THE_STERN not in state.flags
    assert outcome.lines[0].startswith("Five o'clock. You have brought Hanne up")
    assert "At the stern rail" in outcome.lines[0]


def test_five_oclock_is_quiet_when_hanne_already_has_the_books():
    game = _justBefore(LB_THE_STERN, {flags.BOOKS_TO_HANNE: True})
    game.state.location = "saloon"
    outcome = crossing.advance(game)
    state = game.state
    assert not outcome.interrupted
    assert state.location == "saloon"
    assert flags.AT_THE_STERN not in state.flags
    assert not state.knows(facts.THE_STOP)
    assert outcome.lines[0].startswith("Five o'clock. Per rings the engines to stop")
    assert "Nothing goes over the side." in outcome.lines[0]


# --- six o'clock --------------------------------------------------------------
@pytest.mark.parametrize(
    "tonight, ending",
    [
        ({}, lastEndings.KEPT_FROM_THE_RECORD),
        ({flags.BOOKS_TO_HANNE: True}, lastEndings.ON_WHICH_DAYS),
        ({flags.BOOKS_OVERBOARD: True}, lastEndings.OVER_THE_SIDE),
        (
            {flags.BOOKS_OVERBOARD: True, flags.COLUMN_TO_HANNE: True},
            lastEndings.THE_COLUMN,
        ),
    ],
)
def test_six_oclock_docks_at_brekka_and_comes_to_an_ending(tonight, ending):
    game = _justBefore(LB_DOCKING, tonight)
    outcome = crossing.advance(game, turns=3)
    assert outcome.ending == ending
    assert game.state.ending == ending
    assert game.state.location == "deck"
    assert game.state.minute == LB_DOCKING
    assert outcome.lines[0].startswith("Six o'clock. Brekka.")


# --- the notebook -------------------------------------------------------------
def test_the_calendar_lists_the_fixed_hours_but_not_five_oclock():
    assert crossing.calendar(_lastBoat().state) == [
        ("11:00 pm", "The bar shuts, for the last time."),
        ("12:00 am", "Midnight. The mate takes the watch."),
        ("1:00 am", "The saloon goes dark."),
        ("6:00 am", "Brekka. The last night boat comes in."),
    ]


def test_the_calendar_lists_the_stop_once_you_know_the_captains_order():
    state = _lastBoat().state
    state.learn(facts.THE_STOP)
    assert crossing.calendar(state)[3] == (
        "5:00 am",
        "Engines stop, two minutes. The captain's order.",
    )
    state.ending = lastEndings.OVER_THE_SIDE
    assert len(crossing.calendar(state)) == 4
    assert crossing.calendar(state)[3][0] == "6:00 am"
