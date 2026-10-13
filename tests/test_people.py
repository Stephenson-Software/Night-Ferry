"""The people on the first crossing answer what the steward knows: each
gated line opens on the fact or choice it names, every choice has both of
its sides, and the lines that change with the hour or with what was done
earlier in the night say the version that matches."""

import pytest

from nightferry import facts, flags, people
from nightferry.state import HANNE_WAKES, LAST_ORDERS, THE_LIGHT

from conftest import FakeGame


def _game(known=(), tonight=None, minute=0):
    """A game on the first crossing at `minute`, knowing `known`, with
    `tonight`'s flags already set."""
    game = FakeGame()
    state = game.state
    state.minute = minute
    for factId in known:
        state.learn(factId)
    state.flags.update(tonight or {})
    return game


def _questions(game, who):
    return [o["question"] for o in getattr(people, who)(game).get_dialogue_options()]


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


def test_asking_anything_marks_the_conversation_as_time_spent():
    game = _game()
    assert game.spoke is False
    _ask(game, "oskar", "Anything that needs doing?")
    assert game.spoke is True


# --- the purser -------------------------------------------------------------
def test_oskar_sends_you_to_halde_for_who_m_sollid_is():
    game = _game(known=[facts.CABIN_SIX])
    assert _ask(game, "oskar", "Who is M. Sollid?").startswith("A passenger. Was.")
    assert not game.state.knows(facts.THE_TEACHER)
    taught = _game(known=[facts.CABIN_SIX, facts.THE_TEACHER])
    assert not any("M. Sollid" in q for q in _questions(taught, "oskar"))


def test_oskar_names_harbour_house_once_you_know_the_piano():
    assert not any("Harbour House" in q for q in _questions(_game(), "oskar"))
    game = _game(known=[facts.THE_PIANO])
    assert "Ingrid Halvard" in _ask(game, "oskar", "Whose is Harbour House?")
    assert game.state.knows(facts.HARBOUR_HOUSE)


def test_oskar_tells_it_when_you_bring_him_the_ledger_and_the_teacher():
    ledgerOnly = _game(known=[facts.THE_LEDGER])
    assert not any("schoolteacher" in q for q in _questions(ledgerOnly, "oskar"))
    game = _game(known=[facts.THE_LEDGER, facts.THE_TEACHER])
    answer = _ask(game, "oskar", "Nineteen years of Fridays in six")
    assert "Then you've done the sum" in answer
    assert answer.endswith("That's the captain's to tell, not mine and not yours.")
    assert game.state.knows(facts.THE_CAPTAIN)


def test_oskar_on_raskes_audit_and_the_opened_cabin():
    game = _game(known=[facts.RASKES_AUDIT], tonight={flags.OPENED_SIX: True})
    assert _ask(game, "oskar", "Raske thinks").startswith("I know what he thinks.")
    assert _ask(game, "oskar", "I opened it.").endswith("I asked you one thing.")


# --- the woman holding two tickets ---------------------------------------
@pytest.mark.parametrize(
    "hanneKnows, expected",
    [
        (False, "Tea, please. Milk, no sugar."),
        (True, "Please. (She holds the cup without drinking it.)"),
    ],
)
def test_hanne_takes_tea_differently_once_she_knows(hanneKnows, expected):
    game = _game(tonight={flags.HANNE_KNOWS: True} if hanneKnows else None)
    assert _ask(game, "hanne", "Can I get you anything?").startswith(expected)


@pytest.mark.parametrize(
    "tonight, expected",
    [
        ({}, "(She laughs, once,"),
        ({flags.HANNE_PREPARED: True}, "(She is very still.) Dr Fenn said"),
    ],
)
def test_hanne_hears_it_more_gently_when_dr_fenn_prepared_her(tonight, expected):
    game = _game(known=[facts.THE_CAPTAIN], tonight=tonight)
    assert _ask(game, "hanne", "Cabin 6 was booked for your mother.").startswith(
        expected
    )
    assert game.state.flags[flags.TOLD_HANNE] is True
    assert game.state.flags[flags.HANNE_KNOWS] is True
    assert flags.BROKE_YOUR_WORD not in game.state.flags


def test_telling_hanne_after_promising_the_captain_breaks_your_word():
    game = _game(known=[facts.THE_CAPTAIN], tonight={flags.KEPT_INGRIDS_SECRET: True})
    _ask(game, "hanne", "Cabin 6 was booked for your mother.")
    assert game.state.flags[flags.BROKE_YOUR_WORD] is True


def test_hanne_asks_you_to_ask_the_captain_unless_she_already_will_stop():
    game = _game(tonight={flags.HANNE_KNOWS: True})
    assert _ask(game, "hanne", "The light.").endswith(" Will you?")
    assert game.state.flags[flags.HANNE_CHOSE_LIGHT] is True
    willStop = _game(tonight={flags.HANNE_KNOWS: True, flags.INGRID_WILL_STOP: True})
    assert _ask(willStop, "hanne", "The light.").endswith("who asks.")


def test_hanne_can_choose_the_churchyard_and_holds_you_to_it():
    game = _game(tonight={flags.HANNE_KNOWS: True})
    assert _ask(game, "hanne", "to the churchyard").startswith(
        "(She nods.) The churchyard."
    )
    assert game.state.flags[flags.HANNE_CHOSE_LIGHT] is False
    assert not any("The light." in q for q in _questions(game, "hanne"))


def test_hanne_is_not_asked_about_the_light_once_it_has_passed():
    game = _game(tonight={flags.HANNE_KNOWS: True}, minute=THE_LIGHT)
    assert not any("The light." in q for q in _questions(game, "hanne"))
    assert not any("churchyard" in q for q in _questions(game, "hanne"))


# --- the doctor -------------------------------------------------------------
@pytest.mark.parametrize(
    "minute, expected",
    [
        (0, "Seven down: 'kept from the record', five letters."),
        (LAST_ORDERS, "(He has the door on the latch and a book open.)"),
    ],
)
def test_dr_fenn_does_the_crossword_in_the_saloon_then_in_his_cabin(minute, expected):
    assert _ask(_game(minute=minute), "fenn", "Good crossword?").startswith(expected)


def test_dr_fenn_names_harbour_house_once_you_know_the_letter():
    game = _game(known=[facts.THE_LETTER])
    assert _ask(game, "fenn", "Whose is Harbour House?").startswith(
        "Harbour House is Ingrid Halvard's."
    )
    assert game.state.knows(facts.HARBOUR_HOUSE)


def test_dr_fenn_can_be_asked_to_let_it_lie():
    game = _game(known=[facts.THE_APPOINTMENTS])
    assert "Let it go into the ground with her." in _ask(game, "fenn", "Let it lie.")
    assert game.state.flags[flags.FENN_TELLS] is False
    assert flags.HANNE_PREPARED not in game.state.flags
    assert not any("Tonight." in q for q in _questions(game, "fenn"))


def test_dr_fenn_does_not_offer_to_tell_hanne_once_she_knows():
    game = _game(known=[facts.THE_APPOINTMENTS], tonight={flags.HANNE_KNOWS: True})
    assert not any("Let it lie" in q for q in _questions(game, "fenn"))


# --- the company's man ------------------------------------------------------
def test_raske_is_working_late():
    assert _ask(_game(), "raske", "Working late?").endswith("Coffee would be welcome.")


def test_saying_you_know_nothing_leaves_the_purser_responsible():
    game = _game(known=[facts.RASKES_AUDIT, facts.THE_CAPTAIN])
    assert _ask(game, "raske", "I don't know anything").endswith("purser responsible.")
    assert game.state.flags[flags.TOLD_RASKE] is False
    assert not any("captain's." in q for q in _questions(game, "raske"))


# --- the lorry driver -------------------------------------------------------
@pytest.mark.parametrize(
    "tonight, expected",
    [
        ({}, "Like a dropped crate."),
        ({flags.LET_GUS_IN: False}, "Like a dropped crate."),
        ({flags.LET_GUS_IN: True}, "Like a new man."),
    ],
)
def test_gus_back_says_whether_he_got_the_cabin(tonight, expected):
    assert _ask(_game(tonight=tonight), "gus", "How's the back?").startswith(expected)


def test_gus_takes_no_for_an_answer_and_cabin_6_stays_shut():
    game = _game(known=[facts.CABIN_SIX])
    assert _ask(game, "gus", "No. That cabin's spoken for.").startswith(
        "(He takes it well, mostly.)"
    )
    assert game.state.flags[flags.LET_GUS_IN] is False
    assert flags.OPENED_SIX not in game.state.flags
    assert not game.state.knows(facts.INSIDE_SIX)


def test_gus_is_not_offered_the_cabin_once_the_captain_has_come_down():
    game = _game(known=[facts.CABIN_SIX], tonight={flags.AT_THE_DOOR: True})
    assert not any("Cabin 6, till Halde" in q for q in _questions(game, "gus"))


# --- the student ------------------------------------------------------------
@pytest.mark.parametrize(
    "minute, expected",
    [
        (0, "Better than inside."),
        (HANNE_WAKES, "That's the Halde light, there."),
    ],
)
def test_jory_points_out_the_light_from_three(minute, expected):
    assert _ask(_game(minute=minute), "jory", "Cold out here.").startswith(expected)


def test_jory_knew_maren_sollid():
    game = _game(known=[facts.THE_ASHES])
    assert _ask(game, "jory", "Did you know Maren Sollid?").startswith(
        "Mrs Sollid taught everybody."
    )
    assert game.state.knows(facts.THE_TEACHER)


def test_jory_can_let_it_wait_till_after_saturday():
    game = _game(known=[facts.JORYS_TERM])
    assert _ask(game, "jory", "after Saturday").startswith("After Saturday.")
    assert game.state.flags[flags.JORY_TELLS] is False
    assert not any("on the quay" in q for q in _questions(game, "jory"))


# --- the nurse --------------------------------------------------------------
@pytest.mark.parametrize(
    "tonight, expected",
    [
        ({}, "No. Thank you. (Her hand stays on the envelope.)"),
        (
            {flags.LETTER_DELIVERED: True},
            "No. (She smiles for the first time.) Not now.",
        ),
    ],
)
def test_tove_needs_nothing_once_the_letter_is_delivered(tonight, expected):
    assert _ask(_game(tonight=tonight), "tove", "Do you need anything?") == expected


# --- the captain ------------------------------------------------------------
def test_ingrid_takes_coffee():
    assert _ask(_game(), "ingrid", "Coffee, captain?").startswith("Black.")


def test_ingrid_turns_aside_a_steward_who_only_knows_the_booking():
    game = _game(known=[facts.CABIN_SIX])
    assert _ask(game, "ingrid", "booked to an M. Sollid").startswith(
        "Then it's booked."
    )
    assert flags.INGRID_TOLD_YOU not in game.state.flags
    assert not any("Who was cabin 6 for" in q for q in _questions(game, "ingrid"))


@pytest.mark.parametrize(
    "known, expected",
    [
        ([facts.THE_CAPTAIN], "Oskar's told you"),
        ([facts.INSIDE_SIX], "You've been in six."),
        ([facts.THE_DOOR], "Somebody saw me at the door."),
        ([facts.HARBOUR_HOUSE], "Harbour House. The piano."),
    ],
)
def test_ingrid_knows_how_you_found_out_before_she_tells_you(known, expected):
    game = _game(known=known)
    answer = _ask(game, "ingrid", "Who was cabin 6 for, captain?")
    assert answer.startswith(expected)
    assert answer.endswith("What are you going to do with it?")
    assert game.state.flags[flags.INGRID_TOLD_YOU] is True
    assert game.state.knows(facts.THE_CAPTAIN)
    assert not any("booked to an M. Sollid" in q for q in _questions(game, "ingrid"))


def test_ingrid_thanks_you_for_the_hour_in_six():
    game = _game(tonight={flags.ASHES_IN_SIX: True})
    assert _ask(game, "ingrid", "She was in six for an hour.").endswith(
        "It was the right cabin."
    )


@pytest.mark.parametrize(
    "tonight, expected",
    [
        ({flags.AT_THE_DOOR: True}, "In a corridor, at four. But it's said."),
        (
            {flags.AT_THE_DOOR: True, flags.LET_GUS_IN: True},
            "with a man in socks behind a door.",
        ),
    ],
)
def test_ingrid_on_the_corridor_remembers_gus_in_six(tonight, expected):
    assert expected in _ask(_game(tonight=tonight), "ingrid", "About the corridor.")


def test_ingrid_on_the_sale_once_she_has_told_you():
    notYet = _game(known=[facts.LAST_WINTER])
    assert not any("being sold" in q for q in _questions(notYet, "ingrid"))
    game = _game(known=[facts.LAST_WINTER, facts.THE_CAPTAIN])
    assert _ask(game, "ingrid", "being sold").startswith("March. (Unsurprised.)")


def test_the_letter_carried_by_hand_shows_ingrid_the_lifted_seal():
    game = _game(tonight={flags.TOVE_GAVE_LETTER: True, flags.READ_THE_LETTER: True})
    answer = _ask(game, "ingrid", "This is from Maren.")
    assert "the flap has been lifted" in answer
    assert game.state.flags[flags.INGRID_SAW_THE_SEAL] is True
    assert game.state.flags[flags.LETTER_DELIVERED] is True
    assert game.state.knows(facts.WHAT_MAREN_WROTE)
