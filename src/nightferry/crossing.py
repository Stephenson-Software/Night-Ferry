# @author Daniel McCoy Stephenson
"""The clock, the night's fixed hours, and what each of them does.

Every action a scene offers costs a turn of twenty minutes and goes through
advance(). The fixed hours are here and only here: the bar shutting at
eleven, the saloon going dark at one, Hanne waking at three, the captain
coming down at four, the Halde light at five, the quay at six. Scenes never
decide any of that for themselves; they ask here, so the notebook's "night
as you know it" and the scenes can never disagree.

Four o'clock is the failure-proof answer. If nobody has told Hanne who
cabin 6 was for, and the steward has not promised the captain to keep it,
Ingrid goes down to the cabin herself at four and Hanne is in the corridor.
A player who never asked a single question still hears all of it before
the boat docks.
"""

from nightferry import endings, facts, flags
from nightferry.people import deliverTheLetter
from nightferry.state import (
    CAPTAIN_COMES_DOWN,
    DOCKING,
    HANNE_WAKES,
    LAST_ORDERS,
    SALOON_DARK,
    THE_LIGHT,
    TURN_MINUTES,
    formatClock,
)

HOUR_LINES = {
    60: "Nine o'clock. Brekka's lights have gone under the horizon astern. "
    "There is nothing in any direction now but the Kittiwake and the dark.",
    LAST_ORDERS: "Eleven. Oskar pulls the grille down over the bar. Dr Fenn "
    "folds his newspaper, says goodnight to nobody in particular, and goes "
    "along to cabin 3.",
    SALOON_DARK: "One o'clock. The saloon lights go down to the blue night "
    "lamps. Hanne has fallen asleep sitting up, the two tickets in her lap and "
    "her foot against the canvas bag.",
    HANNE_WAKES: "Three. Hanne is awake, and walking: the saloon, the stairs, "
    "the corridor, the saloon. Off the port bow, very small, a light is "
    "turning. Halde.",
}


class Outcome:
    """What an advance() had to say.

    lines are shown to the player in order. interrupted is True when an
    hour of the night took the player somewhere (the corridor at four), so
    a longer wait stops there. ending is set when the night came to one."""

    def __init__(self):
        self.lines = []
        self.interrupted = False
        self.ending = None


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
    line = HOUR_LINES.get(state.minute)
    if line:
        outcome.lines.append(line)
    if state.minute == CAPTAIN_COMES_DOWN:
        _theDoor(game, outcome)
    elif state.minute == THE_LIGHT:
        _theLight(game, outcome)
    elif state.minute >= DOCKING:
        _theQuay(game, outcome)


def captainComesDown(state):
    """Whether four o'clock brings Ingrid down to cabin 6.

    She stays on the bridge only if Hanne already knows, or if the steward
    promised to keep it and she has not since been asked, by the letter, to
    tell it."""
    if state.flags.get(flags.HANNE_KNOWS):
        return False
    kept = state.flags.get(flags.KEPT_INGRIDS_SECRET) is True
    return not (kept and not state.flags.get(flags.LETTER_DELIVERED))


def _theDoor(game, outcome):
    state = game.state
    if not captainComesDown(state):
        return
    state.flags[flags.AT_THE_DOOR] = True
    state.flags[flags.HANNE_KNOWS] = True
    game.learn(facts.THE_ASHES)
    game.learn(facts.THE_CAPTAIN)
    state.location = "corridor"
    outcome.interrupted = True

    parts = [
        "Four o'clock. Oskar finds you and says only, 'Corridor,' and you go.\n\n"
        "The captain has come down. She has the bridge key in one hand and the "
        "key to six in the other, and she is standing at the door the way a "
        "person stands at a graveside. Hanne Sollid, who has been walking since "
        "three, has stopped at the end of the corridor with the canvas bag in "
        "her arms."
    ]
    if state.flags.get(flags.LET_GUS_IN):
        parts.append(
            "Ingrid opens six. Gus Tamm is asleep on the bunk in his socks with "
            "the cardigan folded on the chair and the sea-pink on the shelf, "
            "exactly where he put them. Ingrid looks at him for a long moment "
            "and closes the door again, very gently, and that is when her face "
            "goes."
        )
    if state.flags.get(flags.HANNE_PREPARED):
        hanneAsks = (
            "'Dr Fenn says she went somewhere every month that made her happy,' "
            "Hanne says. 'Was it here?'"
        )
    else:
        hanneAsks = "'That's my mother's name on that door,' Hanne says. 'Isn't it.'"
    parts.append(hanneAsks)
    parts.append(
        "And it comes out there, in the corridor, between the fire hose and the "
        "linen cupboard, at four in the morning, because there is nowhere else "
        "for it to go. Ingrid tells her: that Maren came home on the Friday "
        "boat every month for nineteen years, in cabin 6; that when the mate "
        "took the watch at midnight Ingrid went down to her; that the "
        "specialist was the crossing; that she booked six tonight in Maren's "
        "name so Maren could come home in it once more, and then could not "
        "make herself come down the stairs to where Maren actually was."
    )
    if not state.flags.get(flags.LETTER_DELIVERED):
        if state.flags.get(flags.TOVE_GAVE_LETTER) is True:
            parts.append(
                "You have Maren's letter in your inside pocket. You give it to "
                "the captain, because there is nothing else to do with it."
            )
        else:
            game.learn(facts.THE_LETTER)
            parts.append(
                "The door of cabin 4 opens. Tove Ness, the nurse, has been "
                "listening, and she has a sealed envelope in her hand. 'Are you "
                "I.H.?' she says. 'She said you'd be on the Friday boat.'"
            )
        letter = deliverTheLetter(game, byTove=not state.flags.get(flags.TOVE_GAVE_LETTER))
        # The bridge is not where this is being read; the letter is.
        letter = letter.split("\n\n")[1]
        parts.append(
            "Ingrid reads it aloud, to Hanne, because it is to Hanne:\n\n" + letter
        )
    parts.append(
        "Hanne listens to all of it without putting the bag down. Then she says, "
        "'In a corridor,' and then, 'Nineteen years,' and goes back to the "
        "saloon, and Ingrid goes back up to her bridge."
    )
    outcome.lines.append("\n\n".join(parts))


def _theLight(game, outcome):
    state = game.state
    if state.flags.get(flags.HANNE_CHOSE_LIGHT) is True and state.flags.get(
        flags.INGRID_WILL_STOP
    ):
        state.location = "deck"
        state.ending = endings.OFF_THE_LIGHT
        outcome.ending = endings.OFF_THE_LIGHT
        outcome.lines.append(
            "Five o'clock. The engines stop. For the first time in twenty-two "
            "years of Friday nights the Kittiwake lies still off the Halde "
            "light, rolling a little, with the beam going round over all of "
            "you. Ingrid comes down from the bridge and Hanne comes out of the "
            "saloon with the bag, and they stand at the stern rail together, "
            "and it is getting light.\n\nHanne unties the canvas bag. Ingrid "
            "holds it steady for her while she does. Neither of them says "
            "anything until it is done, and the water has taken it, and the "
            "beam has gone round twice more. Then Ingrid says, 'Friday,' the "
            "way you would sign a log, and Hanne laughs, once, and then "
            "doesn't. Up on the bridge the mate rings the engines on again."
        )
        return
    if state.flags.get(flags.HANNE_CHOSE_LIGHT) is True:
        outcome.lines.append(
            "Five o'clock. The Halde light comes abeam to port and goes by at "
            "twelve knots. Hanne is at the stern rail with the bag in her arms. "
            "Nobody asked the captain to stop, and the ship does not stop."
        )
        return
    outcome.lines.append(
        "Five o'clock. The Halde light comes abeam to port and goes by, and the "
        "sky behind the island goes from black to grey."
    )


def _theQuay(game, outcome):
    state = game.state
    if state.over:
        return
    state.ending = endings.atTheQuay(state)
    outcome.ending = state.ending
    state.location = "deck"
    outcome.lines.append(
        "Six o'clock. Halde. The Kittiwake comes alongside the mole with the "
        "harbour lights still on, and the ramp goes down."
    )


def calendar(state):
    """The night as the player knows it, for the notebook: (time, line) pairs.

    The fixed hours of a night boat are common knowledge to the crew; four
    o'clock is not listed, because nobody plans it."""
    rows = [
        (LAST_ORDERS, "The bar shuts."),
        (SALOON_DARK, "The saloon goes dark for the sleepers."),
        (THE_LIGHT, "The Halde light, abeam to port."),
        (DOCKING, "Halde. The ramp goes down."),
    ]
    if state.flags.get(flags.INGRID_WILL_STOP) and not state.over:
        rows[2] = (THE_LIGHT, "The Halde light. The captain will stop the ship.")
    return [(formatClock(minute), line) for minute, line in rows]
