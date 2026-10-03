# @author Daniel McCoy Stephenson
from nightferry import facts, people
from nightferry.flags import LET_GUS_IN
from nightferry.scenes.base import Scene


class CarDeck(Scene):
    id = "cardeck"
    travelTo = ("saloon", "corridor", "deck", "wheelhouse")

    def descriptor(self):
        if self.state.flags.get(LET_GUS_IN):
            return (
                "The car deck: eleven cars, a van of fish boxes, and the lorry, "
                "its cab dark and empty. Gus is in cabin 6 because of you."
            )
        return (
            "The car deck: eleven cars, a van of fish boxes, the smell of diesel "
            "and wet rope, and one lorry with a tarpaulin over its load and a "
            "radio going low in the cab."
        )

    def run(self):
        state = self.state
        options, actions, unavailable = [], [], {}
        if not state.flags.get(LET_GUS_IN):
            options.append(
                "Talk to Gus, the lorry driver"
                if state.knows(facts.THE_PIANO)
                else "Talk to the lorry driver"
            )
            actions.append(("gus", None))
        options.append("Lift the tarpaulin on the lorry")
        actions.append(("tarpaulin", None))
        self.addTravel(options, actions, unavailable)

        kind, arg = self.choose(self.descriptor(), options, actions, unavailable)
        common = self.common(kind, arg)
        if common is not None:
            return common
        if kind == "gus":
            return self.talk(people.gus(self.game))
        if self.game.learn(facts.THE_PIANO):
            self.ui.showDialogue(
                "Not yours to lift, and you lift it. An upright piano, strapped "
                "and blanketed, with HALDE SCHOOL stencilled on the back in white "
                "paint gone yellow. The delivery docket is taped to the blanket: "
                "'Ex Sollid house clearance. Sold Brekka saleroom, cash, buyer "
                "declined to give name. DELIVER: Harbour House, Halde.' On the "
                "music shelf, under the strap, someone has left a crossword book."
            )
        else:
            self.ui.showDialogue(
                "The piano, under its blankets, going home to an island it was "
                "sold away from. Harbour House, the docket says."
            )
        return self.spend(1)
