# @author Daniel McCoy Stephenson
from nightferry import endings
from nightferry.lastboat import endings as lastEndings

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
    much they know. On the last night boat the port is Brekka, and the count
    is out of that crossing's facts."""
    state = game.state
    port = "Brekka" if state.lastBoat else "Halde"
    names = dict(LOCATION_NAMES, epilogue=port)
    if state.over:
        ended = (lastEndings if state.lastBoat else endings).name(state)
        first = "%s - %s" % (port, ended)
        chips = [first, names.get(state.location, "")]
    else:
        first = state.clock
        chips = [first, names.get(state.location, "")]
        hours = {"text": "Hours to dock: %d" % state.hoursToDock}
        if state.hoursToDock <= 2:
            hours["class"] = "low"
        chips.append(hours)
    chips.append("Known: %d/%d" % (len(state.facts), len(state.registry.FACTS)))
    title = "Night Ferry - %s" % first
    if state.lastBoat and not state.over:
        title = "Night Ferry - the last boat - %s" % first
    return {"title": title, "chips": chips}
