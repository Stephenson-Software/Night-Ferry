# @author Daniel McCoy Stephenson
from nightferry import crossing, endings, facts, premise
from nightferry.scenes.base import Scene

OCTOBER_PAGE = "The October crossing"


class Journal(Scene):
    """Everything you know, written down. Reading it costs no time: it is
    the player's own memory, laid out.

    The same notebook serves both crossings. On the last night boat its
    pages are the second crossing's, and one more page keeps October: the
    first crossing's last page, exactly as it was written."""

    id = "journal"
    travelTo = ()

    def _modules(self):
        """(premise, calendar, last page) for the crossing being played."""
        if self.state.lastBoat:
            from nightferry.lastboat import crossing as lastCrossing
            from nightferry.lastboat import endings as lastEndings
            from nightferry.lastboat import premise as lastPremise

            return lastPremise, lastCrossing, lastEndings
        return premise, crossing, endings

    def run(self):
        state = self.state
        storyPage, clock, lastPage = self._modules()
        options = [
            "What is happening to you",
            "What you know",
            "The night, as you know it",
        ]
        if state.over:
            options.append("The last page")
        if state.past is not None:
            options.append(OCTOBER_PAGE)
        options.append("Close the notebook")
        choice = int(self.ui.showOptions(self.descriptor(), options))
        label = options[choice - 1]
        if label == "What is happening to you":
            self.ui.showDialogue(storyPage.text(state))
        elif label == "What you know":
            self.ui.showDialogue(self.knownText() + self.leadsText())
        elif label == "The night, as you know it":
            self.ui.showDialogue(self.calendarText(clock))
        elif label == "The last page":
            self.ui.showDialogue(lastPage.text(state))
        elif label == OCTOBER_PAGE:
            self.ui.showDialogue(octoberPage(state))
        else:
            back = "epilogue" if state.over else self.game.returnTo
            if back not in self.game.scenes or back == self.id:
                back = "saloon"
            return self.go(back)
        return self.id

    def descriptor(self):
        state = self.state
        registry = state.registry
        onTrail = sum(1 for f in registry.TRAIL if state.knows(f))
        return "%s. %d of %d things known; %d of %d on %s." % (
            state.clock,
            len(state.facts),
            len(registry.FACTS),
            onTrail,
            len(registry.TRAIL),
            getattr(registry, "TRAIL_NAME", "the trail to cabin 6"),
        )

    def knownText(self):
        state = self.state
        registry = state.registry
        if not state.facts:
            return "Nothing yet."
        lines = []
        for factId in registry.FACTS:  # registry order, not learning order
            if state.knows(factId):
                marker = "*" if factId in registry.TRAIL else "-"
                when = state.learnedAt(factId)
                lines.append(
                    "%s %s%s\n  %s"
                    % (
                        marker,
                        registry.title(factId),
                        "" if when is None else " - " + when,
                        registry.text(factId),
                    )
                )
        lines.append(
            "\n(* marks %s.)" % getattr(registry, "TRAIL_NAME", "the trail to cabin 6")
        )
        return "\n\n".join(lines)

    def leadsText(self):
        """The rumour web: under what you know, where it points that you
        haven't been. Never names the missing fact - says where to look."""
        state = self.state
        registry = state.registry
        lines = []
        for factId in registry.FACTS:
            if not state.knows(factId):
                continue
            for target, text in registry.leads(factId):
                if not state.knows(target) and text not in lines:
                    lines.append(text)
        if not lines:
            return ""
        return "\n\nThere's more to learn:\n" + "\n".join("? " + line for line in lines)

    def calendarText(self, clock=crossing):
        return "\n".join(
            "%8s  %s" % (when, line) for when, line in clock.calendar(self.state)
        )


def octoberPage(state):
    """The first crossing's last page, rebuilt from what State.past kept."""
    from nightferry.state import State

    ending, known, flagsThen = state.firstCrossing()
    then = State()
    then.ending = ending
    then.facts = [f for f in known if f in facts.FACTS]
    then.flags = flagsThen
    return "OCTOBER - %s.\n\n%s" % (endings.name(then), endings.text(then))
