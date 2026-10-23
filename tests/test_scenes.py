"""The places on the first crossing offer what the hour and the night so far
allow: rows appear, go unavailable with a reason, or change their label as
the clock and the steward's choices say, and each place's own actions learn
what they name and cost the time they say. The notebook costs nothing,
keeps its last page for after the ending, and always closes somewhere."""

from nightferry import endings, facts, flags, scenes
from nightferry.scenes.corridor import Corridor
from nightferry.scenes.deck import SEA, Deck
from nightferry.scenes.epilogue import Epilogue
from nightferry.scenes.journal import Journal
from nightferry.scenes.saloon import SALOON_SIGHTS, Saloon
from nightferry.state import HANNE_WAKES, LAST_ORDERS, SALOON_DARK

from conftest import FakeGame, ScriptedUI


def _game(script, known=(), tonight=None, minute=0, location="saloon"):
    """A game on the first crossing at `minute`, knowing `known`, with
    `tonight`'s flags already set, whose menus are driven by `script`."""
    game = FakeGame(ScriptedUI(script))
    state = game.state
    state.minute = minute
    state.location = location
    for factId in known:
        state.learn(factId)
    state.flags.update(tonight or {})
    return game


def _menu(game, index=0):
    """The labels and unavailable reasons of the `index`th menu shown."""
    _, labels, reasons, _ = game.ui.menus[index]
    return dict(zip(labels, reasons))


# --- the saloon ---------------------------------------------------------------
def test_raske_on_the_phone_can_be_overheard_from_the_foyer():
    game = _game(["Stand near the foyer"], minute=2 * 60)
    assert Saloon(game).run() == "saloon"
    menu = _menu(game)
    assert menu["Talk to the man with the laptop"] == (
        "he's on the ship's phone in the foyer"
    )
    assert game.state.knows(facts.LAST_WINTER)
    assert game.ui.saw("the night service ends in March")
    assert game.state.minute == 2 * 60 + 20


def test_there_is_no_foyer_to_stand_near_when_raske_is_off_the_phone():
    game = _game(["Look around the saloon"], minute=60)
    Saloon(game).run()
    assert not any("foyer" in label for label in _menu(game))


def test_the_ledgers_are_under_oskar_until_he_walks_the_boat():
    seated = _game(["Look around the saloon"], known=[facts.CABIN_SIX], minute=60)
    Saloon(seated).run()
    assert _menu(seated)["Look through the old ledgers under the hatch"] == (
        "Oskar is sitting on them"
    )

    game = _game(
        ["Look through the old ledgers"], known=[facts.CABIN_SIX], minute=2 * 60
    )
    Saloon(game).run()
    assert game.state.knows(facts.THE_LEDGER)
    assert game.ui.saw("M. Sollid - once more.")
    assert game.state.minute == 2 * 60 + 20


def test_the_ledgers_are_not_offered_before_cabin_six_means_anything():
    game = _game(["Look around the saloon"], minute=2 * 60)
    Saloon(game).run()
    assert not any("ledgers" in label for label in _menu(game))


def test_looking_around_the_saloon_draws_a_sight_and_takes_a_turn():
    game = _game(["Look around the saloon"], minute=60)
    Saloon(game).run()
    assert game.state.rngDraws == 1
    assert any(text in SALOON_SIGHTS for text in game.ui.dialogues)
    assert game.state.minute == 60 + 20


def test_hanne_unprepared_hears_it_from_the_captain_and_can_choose_the_churchyard():
    game = _game(
        ["Take Hanne up to the wheelhouse", "Take her home to the churchyard"],
        tonight={flags.INGRID_ASKED_FOR_HANNE: True},
        minute=3 * 60 + 20,
    )
    assert Saloon(game).run() == "saloon"
    assert game.ui.saw("'The steward says you asked for me.'")
    assert not game.ui.saw("Dr Fenn told me")
    assert game.state.flags[flags.HANNE_KNOWS] is True
    assert game.state.flags[flags.MET_IN_WHEELHOUSE] is True
    assert game.state.flags[flags.HANNE_CHOSE_LIGHT] is False
    assert flags.INGRID_WILL_STOP not in game.state.flags
    assert game.ui.saw("[Hanne will remember that.]")


def test_hanne_cannot_be_taken_up_while_she_sleeps():
    game = _game(
        ["Look around the saloon"],
        tonight={flags.INGRID_ASKED_FOR_HANNE: True},
        minute=SALOON_DARK,
    )
    Saloon(game).run()
    assert _menu(game)["Take Hanne up to the wheelhouse"] == (
        "she's asleep - the captain can wait an hour, or can't"
    )


KEPT_SECRET = {flags.KEPT_INGRIDS_SECRET: True}
ASHES = "Carry Hanne's bag to cabin 6 for an hour"


def test_the_bag_cannot_go_to_six_while_gus_sleeps_in_it():
    game = _game(
        ["Look around the saloon"],
        tonight=dict(KEPT_SECRET, **{flags.LET_GUS_IN: True}),
        minute=SALOON_DARK,
    )
    Saloon(game).run()
    assert _menu(game)[ASHES] == "Gus Tamm is asleep in cabin 6"


def test_the_bag_cannot_go_to_six_when_hanne_would_wake_before_the_hour_is_out():
    minute = HANNE_WAKES - 40
    game = _game(["Look around the saloon"], tonight=KEPT_SECRET, minute=minute)
    Saloon(game).run()
    assert game.state.hanneAsleep
    assert _menu(game)[ASHES] == "she'll wake before the hour is out"


def test_the_bag_is_only_offered_to_a_steward_who_kept_the_secret_while_hanne_sleeps():
    awake = _game(["Look around the saloon"], tonight=KEPT_SECRET, minute=60)
    Saloon(awake).run()
    assert ASHES not in _menu(awake)

    told = _game(
        ["Look around the saloon"],
        tonight={flags.KEPT_INGRIDS_SECRET: False},
        minute=SALOON_DARK,
    )
    Saloon(told).run()
    assert ASHES not in _menu(told)


def test_carrying_the_bag_to_six_gives_maren_her_hour():
    game = _game([ASHES], tonight=KEPT_SECRET, minute=SALOON_DARK)
    Saloon(game).run()
    assert game.state.flags[flags.ASHES_IN_SIX] is True
    assert game.state.knows(facts.INSIDE_SIX)
    assert game.ui.saw("[Ingrid will remember that.]")
    assert game.state.minute == SALOON_DARK + 60


# --- the cabin corridor ---------------------------------------------------------
def test_listening_at_cabin_four_hears_tove_rehearse_once():
    game = _game(["Listen at the door of cabin 4"], location="corridor")
    assert Corridor(game).run() == "corridor"
    assert game.state.knows(facts.THE_LETTER)
    assert game.ui.saw("I'm - I was Maren's nurse.")
    assert game.state.minute == 20

    game.ui.script.append("Listen at the door of cabin 4")
    Corridor(game).run()
    assert game.ui.dialogues[-1].startswith("Cabin 4 is quiet.")
    assert game.state.minute == 40


def test_dr_fenn_is_knocked_for_in_cabin_three_only_after_last_orders():
    early = _game(["Sit in the steward's pantry"], location="corridor", minute=60)
    Corridor(early).run()
    assert "Knock at cabin 3" not in _menu(early)

    game = _game(
        ["Knock at cabin 3", "[Back]"], location="corridor", minute=LAST_ORDERS
    )
    assert Corridor(game).run() == "corridor"
    assert "Knock at cabin 3" in _menu(game)
    assert game.state.minute == LAST_ORDERS


def test_with_gus_let_in_six_is_his_and_not_opened_with_the_master_key():
    game = _game(
        ["Look in on Gus in cabin 6", "[Back]"],
        tonight={flags.LET_GUS_IN: True},
        location="corridor",
    )
    assert Corridor(game).run() == "corridor"
    assert not any("Open cabin 6" in label for label in _menu(game))
    assert game.state.minute == 0


# --- the open deck --------------------------------------------------------------
def test_looking_over_the_water_in_the_dark_draws_from_the_sea():
    game = _game(["Look out over the water"], location="deck", minute=60)
    assert Deck(game).run() == "deck"
    assert game.state.rngDraws == 1
    assert game.ui.dialogues[0] in SEA
    assert game.state.minute == 60 + 20


def test_from_three_the_deck_shows_the_halde_light_instead_of_the_sea():
    game = _game(["Look out over the water"], location="deck", minute=HANNE_WAKES)
    Deck(game).run()
    descriptor = game.ui.menus[0][0]
    assert "a light turning on the edge of the world: Halde" in descriptor
    assert game.ui.saw("three white flashes")
    assert game.state.rngDraws == 0
    assert game.state.minute == HANNE_WAKES + 20


# --- the notebook ---------------------------------------------------------------
def _notebook(script, known=(), ending=None, returnTo="saloon"):
    """A game with the notebook open on the first crossing, as the scene
    loop would have it: every place built, and somewhere to go back to."""
    game = _game(script, known=known, location="journal")
    game.state.ending = ending
    game.returnTo = returnTo
    game.scenes = scenes.build(game)
    return game


def test_a_notebook_with_nothing_in_it_says_so_and_points_nowhere():
    game = _notebook(["What you know"])
    assert Journal(game).run() == "journal"
    assert game.ui.dialogues == ["Nothing yet."]
    assert game.state.minute == 0


def test_the_last_page_is_only_in_the_notebook_once_the_night_has_ended():
    tonight = _notebook(["Close the notebook"])
    Journal(tonight).run()
    assert "The last page" not in _menu(tonight)

    game = _notebook(["The last page"], ending=endings.OFF_THE_LIGHT)
    assert Journal(game).run() == "journal"
    assert game.ui.dialogues == [endings.text(game.state)]


def test_once_everything_is_known_the_notebook_has_no_more_to_learn():
    game = _notebook(["What you know"], known=list(facts.FACTS))
    Journal(game).run()
    assert Journal(game).leadsText() == ""
    assert not game.ui.saw("There's more to learn:")
    assert game.ui.saw(facts.title(facts.CABIN_SIX))


def test_closing_the_notebook_after_the_ending_goes_back_to_the_epilogue():
    game = _notebook(["Close the notebook"], ending=endings.OFF_THE_LIGHT)
    assert Journal(game).run() == "epilogue"
    assert game.state.location == "epilogue"


def test_closing_the_notebook_with_nowhere_to_go_back_to_goes_to_the_saloon():
    for returnTo in ("journal", "nowhere"):
        game = _notebook(["Close the notebook"], returnTo=returnTo)
        assert Journal(game).run() == "saloon", returnTo
        assert game.state.location == "saloon"


# --- the epilogue ---------------------------------------------------------------
def test_the_epilogue_opens_the_notebook_and_comes_back_to_itself():
    game = _game(["Open your notebook"], location="epilogue")
    game.state.ending = endings.BESIDE_ARNE
    assert Epilogue(game).run() == "journal"
    assert endings.name(game.state) in game.ui.menus[0][0]
    assert game.state.location == "journal"
    assert game.returnTo == "epilogue"
