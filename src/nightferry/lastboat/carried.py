# @author Daniel McCoy Stephenson
"""What the last night boat remembers of the first crossing.

Five months have passed. What happened in October - how it ended, what the
steward did, what they were told - is in State.past, unchanged, and these
are the questions the second crossing asks of it. Nothing here writes.
"""

from nightferry import endings as firstEndings
from nightferry import facts as firstFacts
from nightferry import flags
from nightferry.lastboat import facts


def octoberEnding(state):
    return state.pastEnding


def hanneKnewInOctober(state):
    """Whether Hanne went ashore in October knowing who cabin 6 was for.

    Every first-crossing ending but the kept crossing is one where she did."""
    return state.pastEnding in (
        firstEndings.OFF_THE_LIGHT,
        firstEndings.BESIDE_ARNE,
        firstEndings.AT_THE_DOOR,
    )


def letterInYourPocket(state):
    """The kept crossing, with Maren's letter carried and never delivered:
    it has been in the steward's inside pocket since October."""
    return (
        state.pastEnding == firstEndings.KEPT_CROSSING
        and state.pastFlag(flags.TOVE_GAVE_LETTER) is True
        and not state.pastFlag(flags.LETTER_DELIVERED)
    )


def hanneKnows(state):
    """Whether Hanne knows, by now, who cabin 6 was for."""
    return bool(
        hanneKnewInOctober(state)
        or state.flags.get(flags.TOLD_HANNE_TONIGHT)
        or state.flags.get(flags.LETTER_TO_HANNE)
        or state.flags.get(flags.BOOKS_TO_HANNE)
    )


def youKnewInOctober(state):
    """Whether the steward came ashore in October knowing who cabin 6 was for."""
    return state.pastKnew(firstFacts.THE_CAPTAIN)


def oskarCleared(state):
    """In October the steward told Raske the truth, and it cleared Oskar and
    put the captain's name in front of the board."""
    return state.pastFlag(flags.TOLD_RASKE) is True


def firedInOctober(state):
    """The steward opened cabin 6 in October, and Oskar did not keep them on."""
    return bool(state.pastFlag(flags.OPENED_SIX))


def persuadable(state):
    """Whether the captain can be talked out of the side.

    Two things will do it: knowing that Hanne has been counting her mother's
    crosses, or Maren's piano played under the floor of six by Maren's last
    pupil. Without one of them, she says no."""
    return state.knows(facts.THE_CROSSES) or bool(
        state.flags.get(flags.INGRID_HEARD_THE_PIANO)
    )


def readyToTell(state):
    """Enough known that the captain will say where she is going: the box
    itself, or two of the things around it."""
    if state.knows(facts.THE_BOX):
        return True
    around = (facts.HOUSE_SOLD, facts.PIANO_AGAIN, facts.TICKET_SOUTH, facts.THE_STOP)
    return sum(1 for f in around if state.knows(f)) >= 2


def booksSettled(state):
    return bool(
        state.flags.get(flags.BOOKS_TO_HANNE)
        or state.flags.get(flags.BOOKS_OVERBOARD)
        or state.flags.get(flags.BOOKS_KEPT)
    )
