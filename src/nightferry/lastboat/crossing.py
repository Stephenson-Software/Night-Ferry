# @author Daniel McCoy Stephenson
"""The last night boat's clock, its fixed hours, and what each of them does.

The same contract as nightferry.crossing: every action costs a turn of
twenty minutes and goes through advance(), and the fixed hours are here and
only here - the Halde light going astern, the bar's last last orders,
midnight (the mate takes the watch; the captain goes down to six), the
saloon going dark, Brekka's lights, five o'clock, the quay.

Five o'clock is the failure-proof answer. If the books have not already gone
to Hanne, Per sends for the steward, and at the stern rail Ingrid says where
she is going and what is in the box - so a player who never asked anyone
anything still hears all of it before the boat docks - and then puts the
choice to them, unless they have already made it.
"""

from nightferry import flags
from nightferry.crossing import Outcome
from nightferry.lastboat import carried, endings, facts
from nightferry.lastboat.people import theBooksToHanne
from nightferry import endings as firstEndings
from nightferry.state import (
    LB_BREKKA_LIGHTS,
    LB_DOCKING,
    LB_LAST_ORDERS,
    LB_LIGHT_ASTERN,
    LB_SALOON_DARK,
    LB_THE_STERN,
    LB_THE_WATCH,
    TURN_MINUTES,
    formatClock,
)

HOUR_LINES = {
    LB_LAST_ORDERS: "Eleven. Oskar pulls the grille down over the bar for the "
    "last time, and stands with his hand on it for a moment, and then locks it.",
    LB_SALOON_DARK: "One o'clock. The saloon lights go down to the blue night "
    "lamps. Nobody is asleep who is not pretending.",
    LB_BREKKA_LIGHTS: "Four. Off the bow, low and orange, Brekka. The last "
    "night boat has two hours left to run.",
}


def advance(game, turns=1):
    """Move the clock a turn at a time, firing each hour of the night."""
    outcome = Outcome()
    state = game.state
    for _ in range(turns):
        if state.over or outcome.interrupted:
            break
        state.minute += TURN_MINUTES
        _theHour(game, outcome)
    return outcome


def _theHour(game, outcome):
    state = game.state
    if state.minute == LB_LIGHT_ASTERN:
        outcome.lines.append(_theLightAstern(state))
    line = HOUR_LINES.get(state.minute)
    if line:
        outcome.lines.append(line)
    if state.minute == LB_THE_WATCH:
        outcome.lines.append(_theWatch(state))
    elif state.minute == LB_THE_STERN:
        _theStern(game, outcome)
    elif state.minute >= LB_DOCKING:
        _brekka(game, outcome)


def _theLightAstern(state):
    line = (
        "Twenty to nine. The Halde light comes abeam to starboard - three white "
        "flashes, then dark - and begins to fall astern for the last time from "
        "a night boat."
    )
    if carried.octoberEnding(state) == firstEndings.OFF_THE_LIGHT:
        line += (
            " Somewhere under it, in October, Maren went into the water from "
            "this ship's stern. At the back of the wheelhouse the captain does "
            "not turn her head, and does not need to."
        )
    return line


def _theWatch(state):
    parts = [
        "Midnight. On the bridge it is not Per who speaks but the captain, from "
        "the back of the wheelhouse, out of nineteen years of habit: 'Mr Aasen, "
        "you have the watch.' It was never hers to give tonight. Per says, 'I "
        "have the watch,' and she goes below to cabin 6, and shuts the door."
    ]
    if state.flags.get(flags.PER_TELLS_HER) is True:
        parts.append(
            "On the ladder she stops, because Per has said, to the windows and "
            "not to her, 'I always knew where you were, captain. Every Friday. I "
            "was glad.' She stands there long enough for the radar to go round "
            "four times. Then she says, 'Thank you, Mr Aasen,' and goes down."
        )
    return "\n\n".join(parts)


def _theStern(game, outcome):
    state = game.state
    if state.flags.get(flags.BOOKS_TO_HANNE):
        outcome.lines.append(
            "Five o'clock. Per rings the engines to stop, as the night book says, "
            "and the Kittiwake lies still mid-channel for two minutes with the "
            "sky going grey behind her. Nothing goes over the side. At the stern "
            "rail Hanne Sollid has her mother's box against her chest and Ingrid "
            "beside her, and they let the two minutes go by without a word, and "
            "then the engines start again."
        )
        return
    state.location = "deck"
    if state.flags.get(flags.INGRID_GIVES_BOOKS) is True:
        outcome.interrupted = True
        outcome.lines.append(
            "Five o'clock. You have brought Hanne up to the stern rail, as the "
            "captain asked, and told her nothing but that she was wanted. Per "
            "rings the engines to stop. Ingrid comes up the ladder from the "
            "cabin corridor with the box in her arms and sets it on the rail "
            "between them.\n\n" + theBooksToHanne(game, atTheStern=True)
        )
        return
    state.flags[flags.AT_THE_STERN] = True
    outcome.interrupted = True
    game.learn(facts.THE_STOP)
    game.learn(facts.THE_BOX)
    game.learn(facts.THE_MARGINS)
    game.learn(facts.THE_ANSWER)
    parts = [
        "Five o'clock. Per sends for you: the deckhand says only, 'Stern,' and "
        "you go. The engines stop. The Kittiwake lies still mid-channel with "
        "the sky going grey, and at the stern rail the captain has a cardboard "
        "box tied with string, and the string untied."
    ]
    if not state.flags.get(flags.INGRID_TOLD_YOU_TONIGHT):
        state.flags[flags.INGRID_TOLD_YOU_TONIGHT] = True
        parts.append(
            "'Steward.' She does not seem surprised. 'Per thought somebody ought "
            "to be here, and he can't leave the bridge.' And she tells you, "
            "because you are the one standing there: Harbour House is sold, and "
            "Maren's piano is on the car deck going back to the saleroom, and on "
            "Tuesday she takes a single south to a sister she has not seen in "
            "thirty years. In the box are the crossword books from the drawer of "
            "six - nineteen years of Fridays, both their hands - and five was "
            "the hour she always went back up. 'They're the only place it was "
            "ever written down,' she says. 'Kept from the record. That was the "
            "whole of it.'"
        )
    parts.append(
        "She opens the top book, to show you what she means, and there in the "
        "margin beside a clue, in a schoolteacher's round print: 'Happy. - M.'"
    )
    if state.flags.get(flags.INGRID_GIVES_BOOKS) is False:
        state.flags[flags.BOOKS_OVERBOARD] = True
        parts.append(
            "'You said to do what I came to do,' she says, and does it. She "
            "drops them one at a time, nineteen years of Fridays, and the wake "
            "takes each one and turns it over and it is gone. When the box is "
            "empty she folds it flat. Up on the bridge Per rings the engines on "
            "again, and does not look aft."
        )
    outcome.lines.append("\n\n".join(parts))


def _brekka(game, outcome):
    state = game.state
    if state.over:
        return
    state.ending = endings.atBrekka(state)
    outcome.ending = state.ending
    state.location = "deck"
    outcome.lines.append(
        "Six o'clock. Brekka. The Kittiwake comes alongside for the last time "
        "as a night boat, with the town's lights going out one by one behind "
        "the cranes, and the ramp goes down."
    )


def calendar(state):
    """The night as the player knows it, for the notebook: (time, line) pairs."""
    rows = [
        (LB_LAST_ORDERS, "The bar shuts, for the last time."),
        (LB_THE_WATCH, "Midnight. The mate takes the watch."),
        (LB_SALOON_DARK, "The saloon goes dark."),
    ]
    if state.knows(facts.THE_STOP) and not state.over:
        rows.append((LB_THE_STERN, "Engines stop, two minutes. The captain's order."))
    rows.append((LB_DOCKING, "Brekka. The last night boat comes in."))
    return [(formatClock(minute), line) for minute, line in rows]
