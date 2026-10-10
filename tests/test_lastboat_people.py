"""The people on the last night boat remember October: each of them says
something different depending on how the first crossing ended and what the
steward did in it, and every one of those lines is reachable."""

import pytest

from nightferry import endings, flags
from nightferry.lastboat import facts, people
from nightferry.state import LB_BREKKA_LIGHTS, LB_LAST_ORDERS, LB_THE_WATCH

from conftest import FakeGame


def _lastBoat(ending, octoberFlags=None, minute=0, known=(), tonight=None):
    """A game on the last boat after a first crossing that ended `ending`
    with `octoberFlags` set, at `minute`, knowing `known`, with `tonight`'s
    flags already set."""
    game = FakeGame()
    state = game.state
    state.ending = ending
    state.flags = dict(octoberFlags or {})
    state.sailAgain()
    state.minute = minute
    for factId in known:
        state.learn(factId)
    state.flags.update(tonight or {})
    return game


def _ask(game, who, question):
    """Ask `who` the question whose label contains `question` and return the
    answer; fails if the question is not on their menu."""
    npc = getattr(people, who)(game)
    for option in npc.get_dialogue_options():
        if question in option["question"]:
            return option["response"]()
    raise AssertionError(
        "%r is not on %s's menu: %r"
        % (question, who, [o["question"] for o in npc.get_dialogue_options()])
    )


# --- the purser -------------------------------------------------------------
def test_oskar_remembers_being_cleared_and_letting_you_go():
    game = _lastBoat(
        endings.AT_THE_DOOR, {flags.TOLD_RASKE: True, flags.OPENED_SIX: True}
    )
    answer = _ask(game, "oskar", "About October.")
    assert answer.startswith("Raske cleared me in October")
    assert "I said I'd not keep you on, and I haven't." in answer
    assert "You didn't keep mine." in _ask(game, "oskar", "cabin 6 tonight")
    assert "The buyer won't." in _ask(game, "oskar", "ledgers")


def test_oskar_remembers_his_suspension_and_keeping_you_on():
    game = _lastBoat(endings.KEPT_CROSSING, {flags.TOLD_RASKE: False})
    answer = _ask(game, "oskar", "About October.")
    assert answer.startswith("They suspended me at the quay in October.")
    assert "You've done the Friday boat every week since." in answer
    assert "I'd keep it." in _ask(game, "oskar", "cabin 6 tonight")
    assert "five months' suspension" in _ask(game, "oskar", "ledgers")


# --- the mate ---------------------------------------------------------------
@pytest.mark.parametrize(
    "ending, octoberFlags, expected",
    [
        (
            endings.OFF_THE_LIGHT,
            {flags.TOLD_RASKE: True},
            "The board read Raske's report",
        ),
        (endings.OFF_THE_LIGHT, {}, "She stopped this ship off the Halde light"),
        (endings.KEPT_CROSSING, {}, "She asked the company to give me the last one."),
    ],
)
def test_per_says_why_the_captain_is_not_in_command(ending, octoberFlags, expected):
    game = _lastBoat(ending, octoberFlags)
    answer = _ask(game, "per", "Why isn't the captain in command?")
    assert answer.startswith(expected)
    assert game.state.knows(facts.THE_PASSENGER)


# --- the captain ------------------------------------------------------------
@pytest.mark.parametrize(
    "ending, octoberFlags, expected",
    [
        (
            endings.AT_THE_DOOR,
            {flags.BROKE_YOUR_WORD: True},
            "You promised me, and then you told her.",
        ),
        (endings.OFF_THE_LIGHT, {}, "The light."),
        (endings.AT_THE_DOOR, {}, "A corridor, at four in the morning."),
        (endings.BESIDE_ARNE, {}, "She put her beside Arne."),
    ],
)
def test_ingrid_remembers_how_october_ended(ending, octoberFlags, expected):
    game = _lastBoat(ending, octoberFlags)
    assert _ask(game, "ingrid", "About October.").startswith(expected)


def test_ingrid_remembers_the_kept_crossing_and_the_hour_in_six():
    withTheHour = _lastBoat(endings.KEPT_CROSSING, {flags.ASHES_IN_SIX: True})
    answer = _ask(withTheHour, "ingrid", "About October.")
    assert answer.startswith("You kept it.")
    assert "And the hour." in answer
    without = _ask(_lastBoat(endings.KEPT_CROSSING), "ingrid", "About October.")
    assert without == "You kept it. I've thought about that every Friday since."


def test_ingrid_on_the_house_until_she_has_said_where_she_is_going():
    game = _lastBoat(endings.KEPT_CROSSING, known=[facts.HOUSE_SOLD])
    assert _ask(game, "ingrid", "Harbour House is sold.").endswith("It's sold.")


@pytest.mark.parametrize(
    "ending, octoberFlags, tonight, expected",
    [
        (endings.OFF_THE_LIGHT, {}, {}, "Hanne knows where her mother went"),
        (
            endings.KEPT_CROSSING,
            {},
            {flags.TOLD_HANNE_TONIGHT: True},
            "And you've told her daughter, tonight.",
        ),
        (
            endings.KEPT_CROSSING,
            {flags.TOVE_GAVE_LETTER: True},
            {},
            "after Tuesday nobody will.",
        ),
        (
            endings.KEPT_CROSSING,
            {flags.TOVE_GAVE_LETTER: True, flags.LETTER_DELIVERED: True},
            {},
            "The nurse brought me Maren's letter",
        ),
    ],
)
def test_ingrid_says_what_hanne_knows_when_she_says_where_she_is_going(
    ending, octoberFlags, tonight, expected
):
    game = _lastBoat(
        ending,
        octoberFlags,
        known=[facts.HOUSE_SOLD, facts.PIANO_AGAIN],
        tonight=tonight,
    )
    answer = _ask(game, "ingrid", "Where are you going, Ingrid?")
    assert answer.startswith("You've a way of finding things out on this boat.")
    assert expected in answer
    assert "(She says it to the dark ahead.)" in answer
    assert game.state.flags[flags.INGRID_TOLD_YOU_TONIGHT] is True
    assert game.state.knows(facts.THE_ANSWER)
    assert game.state.knows(facts.THE_BOX)


def test_ingrid_says_it_to_the_porthole_from_six_and_knows_who_told_you():
    game = _lastBoat(
        endings.KEPT_CROSSING,
        minute=LB_THE_WATCH,
        known=[facts.HOUSE_SOLD, facts.TICKET_SOUTH],
    )
    answer = _ask(game, "ingrid", "Where are you going, Ingrid?")
    assert answer.startswith("Oskar. (She almost smiles.)")
    assert "(She says it to the porthole.)" in answer


# --- the daughter -------------------------------------------------------------
@pytest.mark.parametrize(
    "ending, expected",
    [
        (endings.OFF_THE_LIGHT, "I come over once a month now."),
        (endings.AT_THE_DOOR, "I haven't spoken to the captain since the corridor."),
        (endings.BESIDE_ARNE, "Mum's stone was finished in January"),
        (endings.KEPT_CROSSING, "We buried Mum in October, beside Dad."),
    ],
)
def test_hanne_opens_with_how_october_ended(ending, expected):
    game = _lastBoat(ending)
    answer = _ask(game, "hanne", "Crossing back to Brekka?")
    assert answer.startswith(expected)
    if ending == endings.KEPT_CROSSING:
        assert answer.endswith("and he never changes the subject.")
    else:
        assert answer.endswith("I don't know what any of them were.")


# --- the lorry driver -------------------------------------------------------
@pytest.mark.parametrize(
    "letGusIn, expected",
    [
        (True, "Never better since a certain cabin."),
        (False, "It remembers you, my back does."),
        (None, "Like a dropped crate."),
    ],
)
def test_gus_back_remembers_cabin_6(letGusIn, expected):
    octoberFlags = {} if letGusIn is None else {flags.LET_GUS_IN: letGusIn}
    game = _lastBoat(endings.KEPT_CROSSING, octoberFlags)
    assert _ask(game, "gus", "How's the back?").startswith(expected)


def test_gus_mentions_sleeping_in_her_cabin_only_if_he_did():
    slept = _lastBoat(endings.KEPT_CROSSING, {flags.LET_GUS_IN: True})
    assert "I'd slept in her cabin" in _ask(slept, "gus", "What are you hauling")
    refused = _lastBoat(endings.KEPT_CROSSING, {flags.LET_GUS_IN: False})
    assert _ask(refused, "gus", "What are you hauling").endswith("tipped me forty.")


# --- the student ------------------------------------------------------------
@pytest.mark.parametrize(
    "joryTells, expected",
    [
        (True, "I told Mum and Dad on the quay in October"),
        (False, "I told them after the funeral, like I said."),
        (None, "They still think I'm in my second year."),
    ],
)
def test_jory_remembers_what_he_told_his_parents(joryTells, expected):
    octoberFlags = {} if joryTells is None else {flags.JORY_TELLS: joryTells}
    game = _lastBoat(endings.KEPT_CROSSING, octoberFlags)
    assert _ask(game, "jory", "Going back to Brekka?").startswith(expected)
    assert game.state.knows(facts.JORYS_AUDITION)


@pytest.mark.parametrize(
    "minute, expected",
    [
        (0, "That's the Halde light, going."),
        (LB_LAST_ORDERS, "Better than inside."),
        (LB_BREKKA_LIGHTS, "Brekka."),
    ],
)
def test_jory_at_the_rail_says_what_is_in_sight(minute, expected):
    game = _lastBoat(endings.KEPT_CROSSING, minute=minute)
    assert _ask(game, "jory", "Cold out here.").startswith(expected)
