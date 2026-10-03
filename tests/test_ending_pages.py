"""The last pages, built straight from a state: every ending says what
happened, who cabin 6 was for, what you did and what it cost - and every
person on the boat gets a sentence, whichever way they were left."""

import itertools

from nightferry import endings, flags
from nightferry.state import State

PEOPLE = ("HANNE.", "INGRID.", "OSKAR.", "RASKE.", "DR FENN.", "JORY.", "GUS.", "TOVE.", "YOU.")


def _ended(ending, **setFlags):
    state = State()
    state.ending = ending
    state.flags.update(setFlags)
    return state


def _paragraphs(state):
    return endings.text(state).split("\n\n")


def _starting(state, prefix):
    return [p for p in _paragraphs(state) if p.startswith(prefix)]


def test_each_ending_has_its_name_its_shape_and_everyone_in_it():
    cases = [
        (endings.OFF_THE_LIGHT, "off the light", "stopped her engines off the Halde light"),
        (endings.BESIDE_ARNE, "beside Arne", "knowing who cabin 6 had been for"),
        (endings.AT_THE_DOOR, "at the door", "the captain came down to cabin"),
        (endings.KEPT_CROSSING, "the kept crossing", "not knowing who cabin 6 had"),
    ]
    for ending, name, opening in cases:
        state = _ended(ending)
        assert endings.name(state) == name
        paragraphs = _paragraphs(state)
        assert paragraphs[0].startswith("WHAT HAPPENED.") and opening in paragraphs[0]
        assert paragraphs[1].startswith("WHO CABIN 6 WAS FOR. Maren Sollid")
        assert paragraphs[2].startswith("WHAT YOU DID.")
        assert paragraphs[3] == "WHAT IT COST."
        for who in PEOPLE:
            assert len(_starting(state, who)) == 1, (ending, who)
        assert paragraphs[-1].startswith("WHAT IT WAS.")


def test_every_combination_of_choices_builds_a_page():
    """No flag combination makes a page crash or drop a person."""
    choices = [
        flags.KEPT_INGRIDS_SECRET,
        flags.HANNE_CHOSE_LIGHT,
        flags.FENN_TELLS,
        flags.TOLD_RASKE,
        flags.LET_GUS_IN,
        flags.JORY_TELLS,
        flags.TOVE_GAVE_LETTER,
    ]
    values = (None, True, False)
    extras = [flags.LETTER_DELIVERED, flags.READ_THE_LETTER, flags.OPENED_SIX]
    for ending in endings.ENDINGS:
        for combo in itertools.product(values, repeat=len(choices)):
            state = _ended(ending)
            for flag, value in zip(choices, combo):
                if value is not None:
                    state.flags[flag] = value
            for extra in extras:
                state.flags[extra] = sum(v is True for v in combo) % 2 == 0
            page = endings.text(state)
            for who in PEOPLE:
                assert ("\n\n" + who) in page, (ending, combo, who)


def test_the_letter_is_quoted_only_if_it_got_there():
    sent = _ended(endings.OFF_THE_LIGHT, **{flags.LETTER_DELIVERED: True})
    assert "it was never him I crossed for" in _paragraphs(sent)[1]
    unsent = _ended(endings.KEPT_CROSSING)
    assert "It was never delivered on the boat." in _paragraphs(unsent)[1]
    pocket = _ended(endings.KEPT_CROSSING, **{flags.TOVE_GAVE_LETTER: True})
    assert _starting(pocket, "TOVE. She trusted you with the thing Maren said")


def test_oskar_and_raske_turn_on_what_you_told_raske():
    told = _ended(endings.BESIDE_ARNE, **{flags.TOLD_RASKE: True})
    assert _starting(told, "OSKAR. Cleared.")
    assert _starting(told, "RASKE. You told him the truth")
    lied = _ended(endings.BESIDE_ARNE, **{flags.TOLD_RASKE: False})
    assert _starting(lied, "OSKAR. Raske's report went in as the columns read")
    assert "because you told Raske you knew nothing" in endings.text(lied)
    never = _ended(endings.BESIDE_ARNE)
    assert "because nobody told Raske what the bookings were" in endings.text(never)


def test_fenn_jory_gus_are_remembered_each_way():
    for flag, prefixTrue, prefixFalse, prefixNone in (
        (flags.FENN_TELLS, "DR FENN. He told Hanne", "DR FENN. He let it lie", "DR FENN. Nobody asked"),
        (flags.JORY_TELLS, "JORY. He told his parents", "JORY. He is keeping it", "JORY. He went down the ramp"),
        (flags.LET_GUS_IN, "GUS. He slept in cabin 6", "GUS. He slept in his cab", "GUS. He delivered"),
    ):
        assert _starting(_ended(endings.AT_THE_DOOR, **{flag: True}), prefixTrue)
        assert _starting(_ended(endings.AT_THE_DOOR, **{flag: False}), prefixFalse)
        assert _starting(_ended(endings.AT_THE_DOOR), prefixNone)


def test_you_lose_the_job_only_if_you_opened_the_door():
    opened = _ended(endings.KEPT_CROSSING, **{flags.OPENED_SIX: True})
    assert _starting(opened, "YOU. You opened cabin 6")
    kept = _ended(endings.KEPT_CROSSING)
    assert _starting(kept, "YOU. You never opened cabin 6.")


def test_the_captain_remembers_a_broken_word_and_a_lifted_seal():
    state = _ended(
        endings.BESIDE_ARNE,
        **{flags.BROKE_YOUR_WORD: True, flags.INGRID_SAW_THE_SEAL: True}
    )
    ingrid = _starting(state, "INGRID.")[0]
    assert "You promised her you would keep it, and then you told Hanne." in ingrid
    assert "you opened Maren's letter before you gave it to her" in ingrid


def test_an_empty_night_says_you_did_nothing_that_changed_it():
    state = _ended(endings.KEPT_CROSSING)
    assert _paragraphs(state)[2] == "WHAT YOU DID. Nothing that changed it. You poured coffee."
