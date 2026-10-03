"""The last night boat: every ending is reachable by a scripted route, the
answer comes out at five on every one of them, and October is remembered."""

import pytest

from nightferry import endings, flags
from nightferry.lastboat import endings as lastEndings
from nightferry.lastboat import facts
from nightferry.state import LAST_BOAT, LB_DOCKING

from routes import (
    CANONICAL,
    DO_NOTHING,
    KEPT,
    LAST_CANONICAL,
    LAST_DO_NOTHING_UNTIL_FIVE,
    PANTRY,
    SAIL,
    lastBoatAfter,
    waitInPantry,
)

TO_BREKKA = ["Go along the cabin corridor", PANTRY]  # from five: 5:00 -> 6:00


def _assertAnswered(ui):
    assert ui.saw(
        "WHERE THE CAPTAIN WAS GOING. Away. Ingrid Halvard sold Harbour House"
    )
    assert ui.saw("WHAT IT COST.")
    assert ui.saw("FROM OCTOBER.")


def test_the_last_boat_canonical_learns_everything_and_ends_on_which_days(scripted):
    game, ui = scripted(lastBoatAfter(CANONICAL) + LAST_CANONICAL)
    game.play()
    state = game.state
    assert state.crossing == LAST_BOAT
    assert state.ending == lastEndings.ON_WHICH_DAYS
    assert state.minute == LB_DOCKING
    for fact in facts.FACTS:
        assert state.knows(fact), fact
    assert len(state.facts) == 13
    for who in ("Oskar", "Hanne", "Per", "Gus", "Jory"):
        assert ui.saw("[%s will remember that.]" % who), who
    assert state.flags[flags.INGRID_HEARD_THE_PIANO] is True
    assert state.flags[flags.HANNE_KNOCKS] is True
    assert flags.AT_THE_STERN not in state.flags  # nobody had to be sent for
    # The opening remembered October: the steward opened six and was let go.
    assert ui.saw("March. The MV Kittiwake's last night crossing")
    assert ui.saw("'This isn't keeping you on,'")
    assert ui.saw("In October, from this ship, Maren Sollid went into the water")
    assert ui.saw("Somewhere under it, in October, Maren went into the water")
    assert ui.saw("'I always knew where you were, captain. Every Friday. I was glad.'")
    assert ui.saw("a door opens and does not close")
    # The last page.
    assert ui.saw("WHAT HAPPENED. Nothing went over the side. In the small hours Hanne")
    assert ui.saw("HANNE. She has the days.")
    assert ui.saw(
        "OSKAR. He tore the column out of nineteen ledgers for you, and you gave it"
    )
    assert ui.saw("JORY. He played the Grieg")
    assert ui.saw("The captain heard it in six.")
    assert ui.saw(
        "YOU. You opened six while she was on the bridge - her one rule tonight, as you broke his"
    )
    _assertAnswered(ui)


def test_doing_nothing_on_the_last_boat_still_gets_the_whole_answer_at_five(scripted):
    script = lastBoatAfter(DO_NOTHING) + LAST_DO_NOTHING_UNTIL_FIVE
    script += ["Let them go."] + TO_BREKKA + ["Quit"]
    game, ui = scripted(script)
    game.play()
    state = game.state
    assert state.ending == lastEndings.OVER_THE_SIDE
    assert state.flags[flags.AT_THE_STERN] is True
    for fact in (facts.THE_ANSWER, facts.THE_BOX, facts.THE_MARGINS, facts.THE_STOP):
        assert state.knows(fact), fact
    assert ui.saw("Five o'clock. Per sends for you")
    assert ui.saw("Harbour House is sold, and Maren's piano is on the car deck")
    assert ui.saw("'Happy. - M.'")
    # The rail menu is the only thing on offer at five.
    descriptor, options, _, _ = [
        m for m in ui.menus if m[0].startswith("The stern rail")
    ][0]
    assert options == [
        "Give them to Hanne. They're the days her mother meant.",
        "Take them with you. They're yours.",
        "Let them go.",
    ]
    assert ui.saw("[Ingrid will remember that.]")
    assert ui.saw("WHAT YOU DID. At the stern, at five, you watched them go.")
    # October was the door: Hanne knew, so she knows still.
    assert ui.saw("HANNE. She knows where her mother went, and who with.")
    _assertAnswered(ui)


def test_asking_for_the_books_at_five_without_knowing_why_is_refused(scripted):
    script = lastBoatAfter(DO_NOTHING) + LAST_DO_NOTHING_UNTIL_FIVE
    script += ["Give them to Hanne"] + TO_BREKKA + ["Quit"]
    game, ui = scripted(script)
    game.play()
    assert game.state.ending == lastEndings.OVER_THE_SIDE
    assert ui.saw("'Hanne has never asked me for anything,' she says.")


def test_knowing_the_crosses_wins_the_books_at_the_rail(scripted):
    script = (
        lastBoatAfter(DO_NOTHING)
        + [
            "Sit with Hanne Sollid",
            "Crossing back to Brekka",
            "[Back]",
            "Go along the cabin corridor",
        ]
        + waitInPantry(9)
        + ["Give them to Hanne"]
        + TO_BREKKA
        + ["Quit"]
    )
    game, ui = scripted(script)
    game.play()
    assert game.state.ending == lastEndings.ON_WHICH_DAYS
    assert ui.saw("You tell her about the diaries")
    assert ui.saw("At the stern rail, with the engines stopped")
    assert ui.saw("WHAT HAPPENED. Nothing went over the side. At five o'clock")


def test_taking_them_south_is_kept_from_the_record(scripted):
    script = lastBoatAfter(DO_NOTHING) + LAST_DO_NOTHING_UNTIL_FIVE
    script += ["Take them with you"] + TO_BREKKA + ["Quit"]
    game, ui = scripted(script)
    game.play()
    assert game.state.ending == lastEndings.KEPT_FROM_THE_RECORD
    assert game.state.flags[flags.BOOKS_KEPT] is True
    assert ui.saw("'Mine,' she says")
    assert ui.saw("INGRID. She kept them.")


# The kept crossing, then: Oskar's column, the captain told to do what she
# came to do, and the column given to Hanne - after telling her, in March,
# what the crosses were.
KEPT_THEN_COLUMN = (
    lastBoatAfter(KEPT)
    + [
        "Ask the purser about cabin 6",
        "What's the story with cabin 6 tonight",
        "What happens to your ledgers",
        "Give me the column instead",
        "[Back]",  # 8:20
        "Sit with Hanne Sollid",
        "Crossing back to Brekka",
        "The crosses are the Fridays",  # TOLD_HANNE_TONIGHT (you knew in October)
        "This is from the purser's ledgers",  # COLUMN_TO_HANNE
        "[Back]",  # 8:40
        "Go up to the wheelhouse",
        "Talk to Per Aasen",
        "Why isn't the captain in command",
        "What's in the night order book",
        "[Back]",  # 9:00
        "Go along the cabin corridor",
        "Open cabin 6 with your master key",  # THE_BOX; 9:20
        "Go up to the wheelhouse",
        "Talk to the captain",
        "Where are you going, Ingrid",
        "Do what you came to do",  # INGRID_GIVES_BOOKS = False
        "[Back]",  # 9:40
        "Go along the cabin corridor",
    ]
    + waitInPantry(8)
    + TO_BREKKA
    + ["Quit"]
)  # 9:40 -> 4:40 -> five; then six


def test_the_books_go_but_hanne_has_the_column(scripted):
    game, ui = scripted(KEPT_THEN_COLUMN)
    game.play()
    state = game.state
    assert state.ending == lastEndings.THE_COLUMN
    assert state.past["ending"] == endings.KEPT_CROSSING
    assert state.flags[flags.TOLD_HANNE_TONIGHT] is True
    assert state.flags[flags.BOOKS_OVERBOARD] is True
    assert ui.saw("[Ingrid will remember that.]")
    assert ui.saw("'You said to do what I came to do,' she says, and does it.")
    assert ui.saw("HANNE. She has the dates, in the purser's hand")
    assert ui.saw("In October you kept the captain's secret")
    # The captain sees that Hanne was told tonight, not in October.
    assert ui.saw("And you've told her daughter, tonight.")
    _assertAnswered(ui)


def test_talking_her_round_before_five_brings_hanne_to_the_stern(scripted):
    script = (
        lastBoatAfter(KEPT)
        + [
            "Sit with Hanne Sollid",
            "Crossing back to Brekka",  # THE_CROSSES
            "[Back]",
            "Go along the cabin corridor",
            "Open cabin 6 with your master key",  # THE_BOX
            "Go up to the wheelhouse",
            "Talk to the captain",
            "Where are you going, Ingrid",
            "Give the books to Hanne",  # persuaded: she knows the crosses
            "[Back]",
            "Go along the cabin corridor",
        ]
        + waitInPantry(8)
        + TO_BREKKA
        + ["Quit"]
    )
    game, ui = scripted(script)
    game.play()
    state = game.state
    assert state.flags[flags.INGRID_GIVES_BOOKS] is True
    assert state.ending == lastEndings.ON_WHICH_DAYS
    # Hanne did not know (October was kept); Ingrid tells her at the stern.
    assert ui.saw("Ingrid tells her first, all of it, the way Maren asked her to")
    assert ui.saw("You have brought Hanne up to the stern rail")
    assert flags.AT_THE_STERN not in state.flags


def test_the_letter_in_your_pocket_reaches_hanne_at_last(scripted, installSave):
    installSave("kept_letter_in_pocket")
    script = [
        "Load Slot 1",
        SAIL,
        "Sit with Hanne Sollid",
        "I have your mother's letter",
        "[Back]",
        "Quit",
    ]
    game, ui = scripted(script)
    game.play()
    assert game.state.flags[flags.LETTER_TO_HANNE] is True
    assert ui.saw("'If H. is on the boat, tell her.")
    assert ui.saw("I was on the boat.")
    assert ui.saw("[Hanne will remember that.]")


def test_jory_will_not_play_before_midnight_and_gus_can_say_no(scripted):
    base = lastBoatAfter(DO_NOTHING) + [
        "Walk the lower deck",
        "Talk to the lorry driver",
        "What are you hauling this time",
        "[Back]",
        "Go out on the open deck",
        "Talk to the young man at the rail",
        "Going back to Brekka",
        "Play it tonight",
        "[Back]",
        "Walk the lower deck",
        "Talk to Gus",
    ]
    game, ui = scripted(base + ["Open the back for Jory", "[Back]", "Quit"])
    game.play()
    _, options, reasons, _ = ui.menus[-1]
    row = options.index("Fetch Jory down to the piano")
    assert reasons[row] == "he won't play to a full saloon - after midnight"

    game, ui = scripted(base + ["Keep it strapped", "[Back]", "Quit"])
    game.play()
    assert game.state.flags[flags.GUS_OPENS_THE_LORRY] is False
    assert "Fetch Jory down to the piano" not in ui.menus[-1][1]


def test_the_piano_before_midnight_is_heard_by_nobody_in_six(scripted):
    """Played after five - the captain is on deck by then - it is still the
    Grieg, but it does not reach six."""
    script = (
        lastBoatAfter(DO_NOTHING)
        + [
            "Walk the lower deck",
            "Talk to the lorry driver",
            "What are you hauling this time",
            "[Back]",
            "Go out on the open deck",
            "Talk to the young man at the rail",
            "Going back to Brekka",
            "Play it tonight",
            "[Back]",
            "Walk the lower deck",
            "Talk to Gus",
            "Open the back for Jory",
            "[Back]",  # 9:00
            "Go along the cabin corridor",
        ]
        + waitInPantry(8)
        + [
            "Let them go.",
            "Walk the lower deck",
            "Fetch Jory down to the piano",
            "Quit",
        ]
    )
    game, ui = scripted(script)
    game.play()
    assert game.state.flags[flags.PIANO_PLAYED] is True
    assert flags.INGRID_HEARD_THE_PIANO not in game.state.flags


def test_the_captain_is_on_the_bridge_until_midnight_and_in_six_after(scripted):
    script = lastBoatAfter(DO_NOTHING) + [
        "Go up to the wheelhouse",
        "Go along the cabin corridor",
    ]
    script += waitInPantry(4) + [
        "Go up to the wheelhouse",
        "Go along the cabin corridor",
        "Quit",
    ]
    game, ui = scripted(script)
    game.play()
    menus = {m[0][:20]: m[1] for m in ui.menus}
    wheelhouseBefore = [m for m in ui.menus if m[0].startswith("The wheelhouse")][0][1]
    wheelhouseAfter = [m for m in ui.menus if m[0].startswith("The wheelhouse")][-1][1]
    assert "Talk to the captain" in wheelhouseBefore
    assert "Talk to the captain" not in wheelhouseAfter
    corridorAfter = [m for m in ui.menus if m[0].startswith("The cabin corridor")][-1][
        1
    ]
    assert "Knock at cabin 6" in corridorAfter
    assert ui.saw("Midnight. On the bridge it is not Per who speaks")
    assert menus


@pytest.mark.parametrize(
    "first,expected",
    [
        (CANONICAL, "In October, from this ship, Maren Sollid went into the water"),
        (DO_NOTHING, "In October it came out in the cabin corridor at four"),
        (KEPT, "In October you kept the captain's secret"),
    ],
)
def test_the_opening_remembers_october(scripted, first, expected):
    game, ui = scripted(lastBoatAfter(first) + ["Quit"])
    game.play()
    assert ui.saw(expected)
    header = ui.headers[-1]
    assert header["title"] == "Night Ferry - the last boat - 8:00 pm"
    texts = [chip["text"] for chip in header["chips"]]
    assert texts == ["8:00 pm", "The Saloon", "Hours to dock: 10", "Known: 0/13"]


def test_the_notebook_keeps_october(scripted):
    script = lastBoatAfter(KEPT) + [
        "Ask the purser about cabin 6",
        "What's the story with cabin 6 tonight",
        "[Back]",
        "Open your notebook",
        "What is happening to you",
        "What you know",
        "The night, as you know it",
        "The October crossing",
        "Close the notebook",
        "Quit",
    ]
    game, ui = scripted(script)
    game.play()
    assert ui.saw("WHAT IS HAPPENING TO YOU. The captain is crossing as a passenger")
    assert ui.saw("on the trail to the box") or any(
        "on the trail to the box" in m[0] for m in ui.menus
    )
    assert ui.saw("Midnight. The mate takes the watch.")
    assert ui.saw("OCTOBER - the kept crossing.")
    assert ui.saw("For an hour, while Hanne slept, Maren was in cabin 6")
    assert game.state.location == "saloon"
