# @author Daniel McCoy Stephenson
"""What the boat shows the player, and when - see tak.progression.

Only one thing unlocks on the Kittiwake: the steward's notebook, once there
is something in it worth writing down. Everything else on the boat is
gated by what you know, on the menus themselves, with the reason shown.
"""

from tak import Progression

NOTEBOOK = "notebook"

UNLOCKS = [
    {
        "id": NOTEBOOK,
        "name": "your notebook",
        "announcement": "You have a steward's order pad in your jacket. Things "
        "worth keeping go in it. Its first page, 'What is happening to you', "
        "says the story so far, plainly, as far as you know it.",
        "condition": lambda state: bool(state.facts),
    },
]

progression = Progression(UNLOCKS)


def isUnlocked(state, featureId):
    return progression.isUnlocked(state.unlocked, featureId)


def getNextUnlock(state):
    return progression.getNextUnlock(state, state.unlocked)


def catchUp(state):
    progression.catchUp(state, state.unlocked)
