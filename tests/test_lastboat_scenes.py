"""The places on the last night boat offer what the hour and the night so far
allow: each place's own actions learn what they name and cost the time they
say, what is seen over the rail follows the clock, and the stern rail's
choice can be won by the piano as well as by the crosses."""

from nightferry import endings, flags
from nightferry.lastboat import endings as lastEndings
from nightferry.lastboat import facts
from nightferry.lastboat.scenes import (
    QUIT,
    SALOON_SIGHTS,
    SEA,
    CarDeck,
    Corridor,
    Deck,
    Epilogue,
    Saloon,
    Wheelhouse,
)
from nightferry.state import (
    LB_BREKKA_LIGHTS,
    LB_LAST_ORDERS,
    LB_THE_STERN,
    LB_THE_WATCH,
)

from conftest import FakeGame, ScriptedUI


def _lastBoat(script, minute=0, known=(), tonight=None, location="saloon"):
    """A game on the last boat after a kept crossing, at `minute`, knowing
    `known`, with `tonight`'s flags already set, whose menus are driven by
    `script`."""
    game = FakeGame(ScriptedUI(script))
    state = game.state
    state.ending = endings.KEPT_CROSSING
    state.sailAgain()
    state.minute = minute
    state.location = location
    for factId in known:
        state.learn(factId)
    state.flags.update(tonight or {})
    return game


def _labels(game, index=0):
    """The labels of the `index`th menu shown."""
    return game.ui.menus[index][1]


# --- the saloon ---------------------------------------------------------------
def test_looking_around_the_last_saloon_draws_a_sight_and_takes_a_turn():
    game = _lastBoat(["Look around the saloon"], minute=60)
    assert Saloon(game).run() == "saloon"
    assert game.state.rngDraws == 1
    assert any(text in SALOON_SIGHTS for text in game.ui.dialogues)
    assert game.state.minute == 60 + 20


# --- the car deck -------------------------------------------------------------
def test_lifting_the_tarpaulin_finds_the_piano_once_and_then_only_sees_it():
    game = _lastBoat(["Lift the tarpaulin", "Lift the tarpaulin"], minute=60)
    CarDeck(game).run()
    assert game.state.knows(facts.PIANO_AGAIN)
    assert game.ui.saw("HALDE SCHOOL stencilled on the back")
    assert game.state.minute == 60 + 20

    CarDeck(game).run()
    assert "Talk to Gus" in _labels(game, 1)
    assert game.ui.dialogues[-1].startswith("Maren's piano, under its blankets")
    assert game.state.minute == 60 + 40


# --- the cabin corridor -------------------------------------------------------
def test_opening_six_a_second_time_only_looks_and_remembers_nobody_again():
    game = _lastBoat(["Open cabin 6", "Look into six again"], minute=60)
    Corridor(game).run()
    assert game.ui.saw("[Oskar will remember that.]")
    remembered = len(game.ui.dialogues)

    Corridor(game).run()
    assert game.ui.dialogues[-1] == (
        "Six, as it was: the suitcase, the box, the label. BALLAST."
    )
    assert len(game.ui.dialogues) == remembered + 1
    assert game.state.minute == 60 + 40


# --- the open deck ------------------------------------------------------------
def test_the_halde_light_is_what_is_over_the_rail_until_eleven():
    game = _lastBoat(["Look out over the water"], minute=60, location="deck")
    Deck(game).run()
    assert "the Halde light, getting smaller" in game.ui.menus[0][0]
    assert game.ui.saw("The Halde light: three white flashes")
    assert game.state.rngDraws == 0


def test_after_eleven_and_before_brekka_the_rail_looks_at_the_sea():
    game = _lastBoat(
        ["Look out over the water"], minute=LB_LAST_ORDERS + 20, location="deck"
    )
    Deck(game).run()
    assert game.ui.menus[0][0].startswith("The open deck, astern. Wet steel")
    assert "Jory at the rail" in game.ui.menus[0][0]
    assert game.state.rngDraws == 1
    assert any(text in SEA for text in game.ui.dialogues)


def test_from_four_the_rail_looks_at_brekka():
    game = _lastBoat(
        ["Look out over the water"], minute=LB_BREKKA_LIGHTS + 20, location="deck"
    )
    Deck(game).run()
    assert game.ui.saw("Brekka, low and orange along the bow")
    assert game.state.rngDraws == 0


def test_the_captain_can_be_talked_to_at_the_stern_once_the_books_are_settled():
    game = _lastBoat(
        ["Look out over the water"],
        minute=LB_THE_STERN + 20,
        tonight={flags.AT_THE_STERN: True, flags.BOOKS_KEPT: True},
        location="deck",
    )
    Deck(game).run()
    assert "Talk to Ingrid" in _labels(game)
    assert "The captain is at the rail" in game.ui.menus[0][0]


def test_the_piano_under_six_wins_the_books_at_the_rail_without_the_crosses():
    game = _lastBoat(
        ["Give them to Hanne"],
        minute=LB_THE_STERN,
        tonight={flags.AT_THE_STERN: True, flags.INGRID_HEARD_THE_PIANO: True},
        location="deck",
    )
    Deck(game).run()
    assert game.state.flags.get(flags.BOOKS_TO_HANNE) is True
    assert not game.state.flags.get(flags.BOOKS_OVERBOARD)
    assert game.ui.saw("She heard Jory play the Grieg under the floor of six")
    assert game.ui.saw("[Ingrid will remember that.]")
    assert game.state.minute == LB_THE_STERN


# --- the wheelhouse -----------------------------------------------------------
def test_the_night_order_book_shows_the_stop_once_and_then_only_the_line():
    game = _lastBoat(
        ["Read the night order book", "Read the night order book"],
        minute=LB_THE_WATCH,
        location="wheelhouse",
    )
    Wheelhouse(game).run()
    assert "the back of the wheelhouse empty" in game.ui.menus[0][0]
    assert "Talk to the captain" not in _labels(game)
    assert game.state.knows(facts.THE_STOP)
    assert game.ui.saw("'0500 - STOP ENGINES, TWO MINUTES. I.H.' Per has initialled")

    Wheelhouse(game).run()
    assert game.ui.dialogues[-1] == (
        "0500 - STOP ENGINES, TWO MINUTES. I.H. Initialled, P.A."
    )
    assert game.state.minute == LB_THE_WATCH + 40


# --- the epilogue -------------------------------------------------------------
def _epilogue(script):
    game = _lastBoat(script, location="epilogue")
    game.state.ending = lastEndings.KEPT_FROM_THE_RECORD
    return game


def test_the_epilogue_reads_the_last_page_again():
    game = _epilogue(["Read the last page again"])
    assert Epilogue(game).run() == "epilogue"
    assert lastEndings.name(game.state) in game.ui.menus[0][0]
    assert game.ui.dialogues == [lastEndings.text(game.state)]


def test_the_epilogue_opens_the_notebook_and_comes_back_to_itself():
    game = _epilogue(["Open your notebook"])
    assert Epilogue(game).run() == "journal"
    assert game.state.location == "journal"
    assert game.returnTo == "epilogue"


def test_the_epilogue_quits():
    game = _epilogue(["Quit"])
    assert Epilogue(game).run() == QUIT
