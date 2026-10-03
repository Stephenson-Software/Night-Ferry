"""Every ending is reachable by a scripted route, and the mystery is
answered on every one of them."""

from nightferry import endings, facts, flags
from nightferry.state import DOCKING

from routes import CANONICAL, DO_NOTHING, KEPT, NEW, PANTRY, waitInPantry


def _assertAnswered(ui):
    assert ui.saw("WHO CABIN 6 WAS FOR. Maren Sollid, the Halde schoolteacher")
    assert ui.saw("WHAT IT COST.")


def test_doing_nothing_still_gets_the_whole_answer_at_four(scripted):
    """The failure-proof answer: the steward asks nobody anything, and the
    captain comes down at four, and it comes out in the corridor."""
    game, ui = scripted(DO_NOTHING)
    game.play()
    state = game.state
    assert state.ending == endings.AT_THE_DOOR
    assert state.minute == DOCKING
    assert state.flags[flags.AT_THE_DOOR] is True
    # The answer, the letter, and Maren's own words - all without asking.
    assert state.knows(facts.THE_CAPTAIN)
    assert state.knows(facts.WHAT_MAREN_WROTE)
    assert state.knows(facts.THE_LETTER)
    assert ui.saw("Four o'clock. Oskar finds you")
    assert ui.saw("Ingrid tells her: that Maren came home on the Friday boat")
    assert ui.saw("never him I crossed for")
    assert ui.saw("WHAT HAPPENED. At four in the morning the captain came down")
    assert ui.saw("WHAT YOU DID. When it came out, at four, it came out without you")
    _assertAnswered(ui)


def test_the_churchyard_is_an_ending_of_its_own(scripted):
    script = list(CANONICAL)
    script[script.index("Do what she asked. The light.")] = "Take her home to the churchyard"
    # Without the light, the night runs on to the quay: one more hour.
    script[-1:] = [PANTRY, "Quit"]
    game, ui = scripted(script)
    game.play()
    assert game.state.ending == endings.BESIDE_ARNE
    assert game.state.flags[flags.HANNE_CHOSE_LIGHT] is False
    assert ui.saw("WHAT HAPPENED. The Kittiwake docked at six. Hanne Sollid went down")
    assert ui.saw("HANNE. She knows, and she chose the churchyard")
    assert ui.saw("Five o'clock. The Halde light comes abeam to port and goes by")
    _assertAnswered(ui)


def test_keeping_the_secret_is_an_ending_and_maren_gets_her_hour(scripted):
    game, ui = scripted(KEPT)
    game.play()
    state = game.state
    assert state.ending == endings.KEPT_CROSSING
    assert state.flags[flags.KEPT_INGRIDS_SECRET] is True
    assert state.flags[flags.ASHES_IN_SIX] is True
    assert flags.HANNE_KNOWS not in state.flags
    assert flags.AT_THE_DOOR not in state.flags  # the captain stayed on the bridge
    assert ui.saw("[Ingrid will remember that.]")
    assert ui.saw("WHAT HAPPENED. The Kittiwake docked at six. Hanne Sollid went down the")
    assert ui.saw("For an hour, while Hanne slept, Maren was in cabin 6")
    assert ui.saw("HANNE. She went ashore not knowing.")
    _assertAnswered(ui)


def test_after_the_door_the_light_can_still_be_reached(scripted):
    script = (
        NEW
        + ["Go along the cabin corridor"]
        + waitInPantry(8)  # 4:00, the door
        + [
            "Go back to the saloon",
            "Sit with Hanne",
            "Do what she asked. The light.",
            "[Back]",  # 4:20
            "Go up to the wheelhouse",
            "Talk to the captain",
            "Will you stop the ship at five",
            "[Back]",  # 4:40
            "Look at the chart table",  # 5:00
            "Quit",
        ]
    )
    game, ui = scripted(script)
    game.play()
    assert game.state.ending == endings.OFF_THE_LIGHT
    assert game.state.flags[flags.AT_THE_DOOR] is True
    assert ui.saw("HANNE. She found out in a corridor at four in the morning, and")
    _assertAnswered(ui)


def test_telling_hanne_after_promising_the_captain_breaks_your_word(scripted):
    script = KEPT[: KEPT.index("I'll keep it") + 2] + [
        "Go back to the saloon",
        "Sit with the woman holding two tickets",
        "Cabin 6 was booked for your mother",
        "[Back]",  # 9:20
        "Go along the cabin corridor",
    ] + waitInPantry(9) + ["Quit"]
    game, ui = scripted(script)
    game.play()
    state = game.state
    assert state.flags[flags.BROKE_YOUR_WORD] is True
    assert state.ending == endings.BESIDE_ARNE
    assert ui.saw("You promised her you would keep it, and then you told Hanne.")
    assert ui.saw("HANNE. She knows, and nobody asked her what she wanted")


def test_letting_gus_into_cabin_6_is_found_at_four(scripted):
    script = NEW + [
        "Ask the purser",
        "cabin 6",
        "[Back]",
        "Walk the lower deck",
        "Talk to the lorry driver",
        "All right. Cabin 6",
        "[Back]",
        "Go along the cabin corridor",
    ] + waitInPantry(10) + ["Quit"]
    game, ui = scripted(script)
    game.play()
    state = game.state
    assert state.flags[flags.LET_GUS_IN] is True
    assert state.flags[flags.OPENED_SIX] is True
    assert state.knows(facts.INSIDE_SIX)
    assert state.ending == endings.AT_THE_DOOR
    assert ui.saw("[Gus will remember that.]")
    assert ui.saw("[Oskar will remember that.]")
    assert ui.saw("Gus Tamm is asleep on the bunk in his socks")
    assert ui.saw("GUS. He slept in cabin 6 because you let him, and the captain found")
    assert ui.saw("YOU. You opened cabin 6 for a lorry driver")


def test_taking_tove_up_delivers_the_letter_in_her_own_hands(scripted):
    script = NEW + [
        "Walk the lower deck",
        "Lift the tarpaulin",  # THE_PIANO
        "Go out on the open deck",
        "Talk to the boy",
        "Whose is Harbour House",
        "[Back]",
        "Go along the cabin corridor",
        "Knock at cabin 4",
        "What takes you to Halde",
        "Come up with me",
        "[Back]",
        "Quit",
    ]
    game, ui = scripted(script)
    game.play()
    state = game.state
    assert state.flags[flags.TOVE_GAVE_LETTER] is False
    assert state.flags[flags.LETTER_DELIVERED] is True
    assert state.flags[flags.INGRID_ASKED_FOR_HANNE] is True
    assert state.location == "wheelhouse"
    assert state.knows(facts.WHAT_MAREN_WROTE)
    assert ui.saw("[Tove will remember that.]")
    assert ui.saw("she says 'Are you I.H.?'")


def test_reading_the_letter_first_is_noticed(scripted):
    script = NEW + [
        "Walk the lower deck",
        "Lift the tarpaulin",
        "Go out on the open deck",
        "Talk to the boy",
        "Whose is Harbour House",
        "[Back]",
        "Go along the cabin corridor",
        "Knock at cabin 4",
        "What takes you to Halde",
        "Give it to me",
        "[Back]",
        "Read Maren's letter",
        "Go up to the wheelhouse",
        "Talk to the captain",
        "This is from Maren",
        "[Back]",
        "Quit",
    ]
    game, ui = scripted(script)
    game.play()
    assert game.state.flags[flags.INGRID_SAW_THE_SEAL] is True
    assert ui.saw("the flap has been lifted")
    assert ui.saw("[Ingrid will remember that.]")
