"""The last night boat's last pages, built straight from a state: every
ending says what happened, where the captain was going, what you did and
what it cost - every person aboard gets a sentence, whichever way October
went and whichever way they were left - and the people from October who are
not aboard get a paragraph."""

import itertools

from nightferry import endings as firstEndings
from nightferry import flags
from nightferry.lastboat import endings, facts, premise
from nightferry.state import State

PEOPLE = ("HANNE.", "INGRID.", "PER.", "OSKAR.", "GUS.", "JORY.", "YOU.")


def _ended(ending, october=firstEndings.AT_THE_DOOR, pastFlags=None, **setFlags):
    state = State()
    state.ending = october
    state.flags.update(pastFlags or {})
    state.sailAgain()
    state.ending = ending
    state.flags.update(setFlags)
    return state


def _paragraphs(state):
    return endings.text(state).split("\n\n")


def _starting(state, prefix):
    return [p for p in _paragraphs(state) if p.startswith(prefix)]


def test_each_ending_has_its_name_its_shape_and_everyone_in_it():
    cases = [
        (endings.ON_WHICH_DAYS, "on which days", "Nothing went over the side."),
        (endings.THE_COLUMN, "the column", "Oskar's column folded into"),
        (endings.OVER_THE_SIDE, "over the side", "the wake took them"),
        (endings.KEPT_FROM_THE_RECORD, "kept from the record", "and she did."),
    ]
    for ending, name, opening in cases:
        state = _ended(ending)
        assert endings.name(state) == name
        paragraphs = _paragraphs(state)
        assert paragraphs[0].startswith("WHAT HAPPENED.") and opening in paragraphs[0]
        assert paragraphs[1].startswith("WHERE THE CAPTAIN WAS GOING. Away.")
        assert paragraphs[2].startswith("WHAT YOU DID.")
        assert paragraphs[3] == "WHAT IT COST."
        for who in PEOPLE:
            assert len(_starting(state, who)) == 1, (ending, who)
        assert paragraphs[-2].startswith("FROM OCTOBER. Dr Fenn")
        assert paragraphs[-1].startswith("WHAT IT WAS.")


def test_every_combination_of_choices_and_octobers_builds_a_page():
    choices = [
        flags.OSKAR_GAVE_COLUMN,
        flags.JORY_PLAYS,
        flags.GUS_OPENS_THE_LORRY,
        flags.PER_TELLS_HER,
        flags.INGRID_GIVES_BOOKS,
        flags.HANNE_KNOCKS,
    ]
    extras = [
        flags.PIANO_PLAYED,
        flags.COLUMN_TO_HANNE,
        flags.OPENED_SIX_AGAIN,
        flags.AT_THE_STERN,
        flags.TOLD_HANNE_TONIGHT,
    ]
    octobers = [
        (firstEndings.OFF_THE_LIGHT, {flags.TOLD_RASKE: True, flags.OPENED_SIX: True}),
        (
            firstEndings.BESIDE_ARNE,
            {flags.FENN_TELLS: True, flags.LETTER_DELIVERED: True},
        ),
        (firstEndings.AT_THE_DOOR, {flags.TOLD_RASKE: False}),
        (firstEndings.KEPT_CROSSING, {flags.TOVE_GAVE_LETTER: True}),
    ]
    for october, pastFlags in octobers:
        for ending in endings.ENDINGS:
            for combo in itertools.product((None, True, False), repeat=len(choices)):
                state = _ended(ending, october, pastFlags)
                for flag, value in zip(choices, combo):
                    if value is not None:
                        state.flags[flag] = value
                for extra in extras:
                    state.flags[extra] = sum(v is True for v in combo) % 2 == 0
                page = endings.text(state)
                for who in PEOPLE:
                    assert ("\n\n" + who) in page, (october, ending, combo, who)
                assert "\n\nFROM OCTOBER. " in page


def test_hanne_who_never_learned_is_said_to_have_never_learned():
    state = _ended(endings.OVER_THE_SIDE, october=firstEndings.KEPT_CROSSING)
    assert _starting(state, "HANNE. She still doesn't know what the crosses were.")
    told = _ended(
        endings.OVER_THE_SIDE,
        october=firstEndings.KEPT_CROSSING,
        **{flags.TOLD_HANNE_TONIGHT: True}
    )
    assert _starting(told, "HANNE. She knows now where her mother went")


def test_october_is_remembered_in_the_page():
    light = _ended(
        endings.ON_WHICH_DAYS,
        october=firstEndings.OFF_THE_LIGHT,
        pastFlags={flags.TOLD_RASKE: True},
    )
    text = endings.text(light)
    assert "In October, from this ship's stern, Hanne and Ingrid put Maren" in text
    assert "Raske's report put the captain's name before the board" in text
    assert "He has his pension; Raske's report saw to that." in text
    pocket = _ended(
        endings.KEPT_FROM_THE_RECORD,
        october=firstEndings.KEPT_CROSSING,
        pastFlags={flags.TOVE_GAVE_LETTER: True},
    )
    assert (
        "believes, still, that the letter she gave you in October was delivered"
        in endings.text(pocket)
    )


def test_an_empty_last_boat_says_you_were_sent_for():
    state = _ended(endings.KEPT_FROM_THE_RECORD)
    assert _paragraphs(state)[2].startswith("WHAT YOU DID. Nothing that changed it.")


def test_the_notebook_page_grows_and_ends():
    state = _ended(None)
    assert premise.text(state).startswith("WHERE YOU ARE. The last night boat")
    for fact in facts.FACTS:
        state.learn(fact)
    state.ending = endings.THE_COLUMN
    page = premise.text(state)
    assert (
        "HOW IT ENDED. The books went over the side, and Hanne has Oskar's column."
        in page
    )
    assert "(15 of 15 parts of the story known." in page
