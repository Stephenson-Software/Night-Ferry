# @author Daniel McCoy Stephenson
"""Achievements, reported to arcade through tak.arcade.

One per ending on each crossing, and a few for discoveries. Each is declared
for the game in the gateway's config/play/boards.yaml (Stephenson-Software
RFC 0014) with the same id, title and description as here; ids are
permanent once used. Titles are spoiler-safe; anything that would give the
story away is declared hidden, so arcade shows it only once it is earned.

award() is called after every action and once when a save is loaded, so a
save made before achievements existed - an ending reached on 0.1.0 - is
credited the first time it is opened. tak.arcade.unlock never raises, never
waits, and does nothing outside the browser; award() only decides what has
been earned.
"""

from tak import arcade

from nightferry import endings, facts, flags
from nightferry.lastboat import endings as lastEndings
from nightferry.lastboat import facts as lastFacts
from nightferry.state import CAPTAIN_COMES_DOWN


def _first(state):
    """The first crossing's (ending, facts, flags), live or remembered."""
    return state.firstCrossing()


def _firstEnded(state, ending):
    return _first(state)[0] == ending


def _lastEnded(state, ending):
    return state.lastBoat and state.ending == ending


def _learnedBeforeFour(state):
    if state.lastBoat:
        return False
    minute = state.factMinutes.get(facts.THE_CAPTAIN)
    return minute is not None and minute < CAPTAIN_COMES_DOWN


ACHIEVEMENTS = [
    # --- the first crossing ---------------------------------------------------
    {
        "id": "first-crossing",
        "title": "Alongside",
        "description": "Finish the first crossing",
        "hidden": False,
        "earned": lambda s: _first(s)[0] is not None,
    },
    {
        "id": "ending-off-the-light",
        "title": "Off the Light",
        "description": "Stop the Kittiwake at the Halde light at five",
        "hidden": True,
        "earned": lambda s: _firstEnded(s, endings.OFF_THE_LIGHT),
    },
    {
        "id": "ending-beside-arne",
        "title": "Beside Arne",
        "description": "Dock at Halde with Hanne knowing, and the light gone by",
        "hidden": True,
        "earned": lambda s: _firstEnded(s, endings.BESIDE_ARNE),
    },
    {
        "id": "ending-at-the-door",
        "title": "Four O'Clock",
        "description": "Let the captain come down to cabin 6 herself",
        "hidden": True,
        "earned": lambda s: _firstEnded(s, endings.AT_THE_DOOR),
    },
    {
        "id": "ending-kept-crossing",
        "title": "The Kept Crossing",
        "description": "Keep the captain's secret all the way to Halde",
        "hidden": True,
        "earned": lambda s: _firstEnded(s, endings.KEPT_CROSSING),
    },
    {
        "id": "all-sixteen",
        "title": "Everything on the Kittiwake",
        "description": "Learn all sixteen things on the first crossing",
        "hidden": False,
        "earned": lambda s: all(f in _first(s)[1] for f in facts.FACTS),
    },
    {
        "id": "before-four",
        "title": "Before Four",
        "description": "Find out who cabin 6 was for before four in the morning",
        "hidden": False,
        "earned": _learnedBeforeFour,
    },
    {
        "id": "one-rule",
        "title": "One Rule",
        "description": "Reach Halde without opening cabin 6",
        "hidden": False,
        "earned": lambda s: _first(s)[0] is not None
        and not _first(s)[2].get(flags.OPENED_SIX),
    },
    {
        "id": "her-hour",
        "title": "Her Hour",
        "description": "Carry the bag to cabin 6 while Hanne sleeps",
        "hidden": True,
        "earned": lambda s: bool(_first(s)[2].get(flags.ASHES_IN_SIX)),
    },
    # --- the last night boat ----------------------------------------------------
    {
        "id": "the-last-night-boat",
        "title": "The Last Night Boat",
        "description": "Sail the Kittiwake's last night crossing",
        "hidden": False,
        "earned": lambda s: s.lastBoat,
    },
    {
        "id": "ending-on-which-days",
        "title": "On Which Days",
        "description": "Get the crossword books into Hanne's hands",
        "hidden": True,
        "earned": lambda s: _lastEnded(s, lastEndings.ON_WHICH_DAYS),
    },
    {
        "id": "ending-the-column",
        "title": "The Column",
        "description": "The books go over the side, and Hanne has the purser's column",
        "hidden": True,
        "earned": lambda s: _lastEnded(s, lastEndings.THE_COLUMN),
    },
    {
        "id": "ending-over-the-side",
        "title": "Over the Side",
        "description": "Let the books go at five",
        "hidden": True,
        "earned": lambda s: _lastEnded(s, lastEndings.OVER_THE_SIDE),
    },
    {
        "id": "ending-kept-from-the-record",
        "title": "Kept from the Record",
        "description": "Let the captain take the books south",
        "hidden": True,
        "earned": lambda s: _lastEnded(s, lastEndings.KEPT_FROM_THE_RECORD),
    },
    {
        "id": "all-thirteen",
        "title": "Everything, Again",
        "description": "Learn all thirteen things on the last night boat",
        "hidden": False,
        "earned": lambda s: s.lastBoat and all(s.knows(f) for f in lastFacts.FACTS),
    },
    {
        "id": "the-grieg",
        "title": "The Grieg",
        "description": "Hear Maren's piano played on the car deck",
        "hidden": True,
        "earned": lambda s: s.lastBoat and bool(s.flags.get(flags.PIANO_PLAYED)),
    },
    {
        "id": "master-below",
        "title": "Master Below",
        "description": "Let the mate say what he always knew",
        "hidden": True,
        "earned": lambda s: s.lastBoat and s.flags.get(flags.PER_TELLS_HER) is True,
    },
]

IDS = [a["id"] for a in ACHIEVEMENTS]


def earned(state):
    """The ids this save has earned, in declaration order."""
    found = []
    for achievement in ACHIEVEMENTS:
        try:
            if achievement["earned"](state):
                found.append(achievement["id"])
        except Exception:  # an odd save never stops play
            continue
    return found


def award(game):
    """Report anything earned and not yet reported this run. Never raises."""
    try:
        for achievementId in earned(game.state):
            if achievementId not in game.awarded:
                game.awarded.add(achievementId)
                arcade.unlock(achievementId)
    except Exception:
        pass
