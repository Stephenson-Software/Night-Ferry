# @author Daniel McCoy Stephenson
from nightferry import endings, facts

LOCATION_NAMES = {
    "saloon": "The Saloon",
    "cardeck": "The Car Deck",
    "corridor": "The Cabin Corridor",
    "deck": "The Open Deck",
    "wheelhouse": "The Wheelhouse",
    "journal": "Your Notebook",
    "epilogue": "Halde",
}


def buildHeader(game):
    """The status line: the time, where the player is, the hours left, how
    much they know."""
    state = game.state
    if state.over:
        first = "Halde - %s" % endings.name(state)
        chips = [first, LOCATION_NAMES.get(state.location, "")]
    else:
        first = state.clock
        chips = [first, LOCATION_NAMES.get(state.location, "")]
        hours = {"text": "Hours to dock: %d" % state.hoursToDock}
        if state.hoursToDock <= 2:
            hours["class"] = "low"
        chips.append(hours)
    chips.append("Known: %d/%d" % (len(state.facts), len(facts.FACTS)))
    return {"title": "Night Ferry - %s" % first, "chips": chips}
