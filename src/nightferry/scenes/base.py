# @author Daniel McCoy Stephenson
from nightferry import crossing, endings, people, progression

TRAVEL_LABELS = {
    "saloon": "Go back to the saloon",
    "cardeck": "Walk the lower deck",
    "corridor": "Go along the cabin corridor",
    "deck": "Go out on the open deck",
    "wheelhouse": "Go up to the wheelhouse",
}


class Scene:
    """Shared menu plumbing: a scene builds paired options/actions lists so
    rows can come and go with the player's progress without the numbers
    drifting - see tak's unavailableReasons - and the travel rows, the
    notebook and Quit close every menu the same way.

    Moving about the boat is free; anything done in a place costs a turn
    of twenty minutes, charged by spend()."""

    id = ""
    travelTo = ()

    def __init__(self, game):
        self.game = game

    @property
    def ui(self):
        return self.game.ui

    @property
    def state(self):
        return self.game.state

    def addTravel(self, options, actions, unavailable, travelTo=None):
        for destination in self.travelTo if travelTo is None else travelTo:
            options.append(TRAVEL_LABELS[destination])
            actions.append(("go", destination))
        options.append("Open your notebook")
        actions.append(("notebook", None))
        if not progression.isUnlocked(self.state, progression.NOTEBOOK):
            unavailable[len(options)] = "nothing written in it yet"
        options.append("Quit")
        actions.append(("quit", None))

    def choose(self, descriptor, options, actions, unavailable=None):
        choice = int(self.ui.showOptions(descriptor, options, unavailable or {}))
        return actions[choice - 1]

    def common(self, kind, arg):
        """The rows every place shares. Returns where to go, or None if the
        choice was the scene's own."""
        if kind == "go":
            return self.go(arg)
        if kind == "quit":
            return "quit"
        if kind == "notebook":
            self.game.returnTo = self.id
            return self.go("journal")
        return None

    def go(self, destination):
        self.state.location = destination
        self.game.prompt.reset()
        return destination

    def remember(self, who):
        """The beat after a choice someone will hold you to - for good."""
        self.ui.showDialogue("[%s will remember that.]" % who)

    def talk(self, npc):
        """Run a conversation; say who will remember any choice it settled;
        charge a turn if anything was asked."""
        before = set(self.state.flags)
        self.game.spoke = False
        self.ui.showInteractiveDialogue(npc)
        for flag in list(self.state.flags):
            if flag not in before and flag in people.REMEMBERED:
                self.remember(people.REMEMBERED[flag])
        if self.game.spoke:
            return self.spend(1)
        return self.after()

    def spend(self, turns=1):
        """An action took time. Returns where the game goes next."""
        outcome = crossing.advance(self.game, turns)
        if outcome.lines:
            self.ui.showDialogue("\n\n".join(outcome.lines))
        return self.after()

    def after(self):
        state = self.state
        if state.over:
            if state.location != "epilogue":
                self.ui.showDialogue(endings.text(state))
            return self.go("epilogue")
        return state.location
