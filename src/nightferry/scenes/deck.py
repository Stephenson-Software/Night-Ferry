# @author Daniel McCoy Stephenson
from nightferry import facts, people
from nightferry.scenes.base import Scene

# The sea, which says the same things to everyone. Drawn from the night's
# fixed sequence.
SEA = (
    "The wake goes back white into the dark and closes over.",
    "A gannet, or something the size of one, follows the stern light for a "
    "while and then is not there.",
    "The wind is south-west and steady. Somebody has tied a bin bag to the "
    "rail and it cracks like a flag.",
    "No lights anywhere. The stars are the only things that are not moving.",
)


class Deck(Scene):
    id = "deck"
    travelTo = ("saloon", "cardeck", "corridor", "wheelhouse")

    def descriptor(self):
        if self.state.lightInSight:
            return (
                "The open deck, astern. Wet steel, the rail, the wake, and off "
                "the port bow a light turning on the edge of the world: Halde. "
                "The boy is still at the rail."
            )
        return (
            "The open deck, astern. Wet steel, the rail, the wake, the dark. A "
            "boy in a student's coat at the rail with headphones round his neck "
            "and an unlit cigarette. From here you can see straight down the "
            "cabin corridor through the stairwell door."
        )

    def run(self):
        state = self.state
        options, actions, unavailable = [], [], {}
        options.append(
            "Talk to Jory" if state.knows(facts.JORYS_TERM) else "Talk to the boy at the rail"
        )
        actions.append(("jory", None))
        options.append("Look out over the water")
        actions.append(("look", None))
        self.addTravel(options, actions, unavailable)

        kind, arg = self.choose(self.descriptor(), options, actions, unavailable)
        common = self.common(kind, arg)
        if common is not None:
            return common
        if kind == "jory":
            return self.talk(people.jory(self.game))
        if state.lightInSight:
            self.ui.showDialogue(
                "The Halde light: three white flashes, then dark, then three "
                "again. It is the first thing on the island anyone sees, coming "
                "home, and the last thing going."
            )
        else:
            self.ui.showDialogue(state.draw(SEA))
        return self.spend(1)
