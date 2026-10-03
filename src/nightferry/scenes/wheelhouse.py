# @author Daniel McCoy Stephenson
from nightferry import people
from nightferry.flags import INGRID_WILL_STOP
from nightferry.scenes.base import Scene


class Wheelhouse(Scene):
    id = "wheelhouse"
    travelTo = ("saloon", "cardeck", "corridor", "deck")

    def descriptor(self):
        return (
            "The wheelhouse: dark, warm, the radar sweeping green, the binnacle "
            "lit. The captain stands at the forward windows with her hands behind "
            "her back and has not turned round."
        )

    def run(self):
        options, actions, unavailable = [], [], {}
        options.append("Talk to the captain")
        actions.append(("ingrid", None))
        options.append("Look at the chart table")
        actions.append(("chart", None))
        self.addTravel(options, actions, unavailable)

        kind, arg = self.choose(self.descriptor(), options, actions, unavailable)
        common = self.common(kind, arg)
        if common is not None:
            return common
        if kind == "ingrid":
            return self.talk(people.ingrid(self.game))
        if self.state.flags.get(INGRID_WILL_STOP):
            self.ui.showDialogue(
                "The chart of the Halde approaches. At the light, in pencil, in a "
                "cramped capital hand: 0500 - STOP ENGINES. Underneath, smaller: "
                "M."
            )
        else:
            self.ui.showDialogue(
                "The chart of the Halde approaches, nineteen years of pencil on it. "
                "At the light, in a cramped capital hand, a small cross and the "
                "time 0500, rubbed out and written in again so many times the "
                "paper has gone soft."
            )
        return self.spend(1)
