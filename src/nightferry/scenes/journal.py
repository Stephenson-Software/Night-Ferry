# @author Daniel McCoy Stephenson
from nightferry import crossing, endings, facts, premise
from nightferry.scenes.base import Scene


class Journal(Scene):
    """Everything you know, written down. Reading it costs no time: it is
    the player's own memory, laid out."""

    id = "journal"
    travelTo = ()

    def run(self):
        state = self.state
        options = [
            "What is happening to you",
            "What you know",
            "The night, as you know it",
        ]
        if state.over:
            options.append("The last page")
        options.append("Close the notebook")
        choice = int(self.ui.showOptions(self.descriptor(), options))
        label = options[choice - 1]
        if label == "What is happening to you":
            self.ui.showDialogue(premise.text(state))
        elif label == "What you know":
            self.ui.showDialogue(self.knownText() + self.leadsText())
        elif label == "The night, as you know it":
            self.ui.showDialogue(self.calendarText())
        elif label == "The last page":
            self.ui.showDialogue(endings.text(state))
        else:
            back = "epilogue" if state.over else self.game.returnTo
            if back not in self.game.scenes or back == self.id:
                back = "saloon"
            return self.go(back)
        return self.id

    def descriptor(self):
        state = self.state
        onTrail = sum(1 for f in facts.TRAIL if state.knows(f))
        return "%s. %d of %d things known; %d of %d on the trail to cabin 6." % (
            state.clock,
            len(state.facts),
            len(facts.FACTS),
            onTrail,
            len(facts.TRAIL),
        )

    def knownText(self):
        state = self.state
        if not state.facts:
            return "Nothing yet."
        lines = []
        for factId in facts.FACTS:  # registry order, not learning order
            if state.knows(factId):
                marker = "*" if factId in facts.TRAIL else "-"
                when = state.learnedAt(factId)
                lines.append(
                    "%s %s%s\n  %s"
                    % (
                        marker,
                        facts.title(factId),
                        "" if when is None else " - " + when,
                        facts.text(factId),
                    )
                )
        lines.append("\n(* marks the trail to cabin 6.)")
        return "\n\n".join(lines)

    def leadsText(self):
        """The rumour web: under what you know, where it points that you
        haven't been. Never names the missing fact - says where to look."""
        state = self.state
        lines = []
        for factId in facts.FACTS:
            if not state.knows(factId):
                continue
            for target, text in facts.leads(factId):
                if not state.knows(target) and text not in lines:
                    lines.append(text)
        if not lines:
            return ""
        return "\n\nThere's more to learn:\n" + "\n".join("? " + line for line in lines)

    def calendarText(self):
        return "\n".join(
            "%8s  %s" % (when, line) for when, line in crossing.calendar(self.state)
        )
