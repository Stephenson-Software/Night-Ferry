# @author Daniel McCoy Stephenson
from nightferry import facts, people
from nightferry.flags import (
    LET_GUS_IN,
    LETTER_DELIVERED,
    OPENED_SIX,
    READ_THE_LETTER,
    TOVE_GAVE_LETTER,
)
from nightferry.scenes.base import Scene


class Corridor(Scene):
    id = "corridor"
    travelTo = ("saloon", "cardeck", "deck", "wheelhouse")

    def descriptor(self):
        return (
            "The cabin corridor: eight doors, a fire hose, the linen cupboard, "
            "your pantry with its kettle, and at the end, cabin 6, with a card "
            "in the slot that says RESERVED in Oskar's square hand."
        )

    def run(self):
        state = self.state
        options, actions, unavailable = [], [], {}
        options.append("Knock at cabin 4")
        actions.append(("tove", None))
        options.append("Listen at the door of cabin 4")
        actions.append(("listen", None))
        if state.fennInHisCabin:
            options.append("Knock at cabin 3")
            actions.append(("fenn", None))
        if state.flags.get(LET_GUS_IN):
            options.append("Look in on Gus in cabin 6")
            actions.append(("gus", None))
        else:
            options.append(
                "Open cabin 6 with your master key"
                if not state.flags.get(OPENED_SIX)
                else "Open cabin 6 again"
            )
            actions.append(("six", None))
        if (
            state.flags.get(TOVE_GAVE_LETTER) is True
            and not state.flags.get(LETTER_DELIVERED)
            and not state.flags.get(READ_THE_LETTER)
        ):
            options.append("Read Maren's letter under the pantry lamp")
            actions.append(("read", None))
        options.append("Sit in the steward's pantry for an hour")
        actions.append(("wait", None))
        self.addTravel(options, actions, unavailable)

        kind, arg = self.choose(self.descriptor(), options, actions, unavailable)
        common = self.common(kind, arg)
        if common is not None:
            return common
        if kind == "tove":
            return self.talk(people.tove(self.game))
        if kind == "fenn":
            return self.talk(people.fenn(self.game))
        if kind == "gus":
            return self.talk(people.gus(self.game))
        if kind == "listen":
            return self.listen()
        if kind == "six":
            return self.openSix()
        if kind == "read":
            return self.readTheLetter()
        self.ui.showDialogue(
            "You sit in the pantry with the door open and the kettle ticking, "
            "and the boat goes on through the dark under you."
        )
        return self.spend(3)

    def listen(self):
        if self.game.learn(facts.THE_LETTER):
            self.ui.showDialogue(
                "Through the door of cabin 4, a woman's voice, quiet, trying the "
                "words out the way you would rehearse for an interview: 'Excuse "
                "me. Are you I.H.? I'm - I was Maren's nurse. She gave me this for "
                "you. She said you'd be on the Friday boat.' A pause. 'Excuse me. "
                "Are you - ' She stops, and you hear her sit down on the bunk."
            )
        else:
            self.ui.showDialogue(
                "Cabin 4 is quiet. Once, the creak of the bunk as somebody turns "
                "over and does not sleep."
            )
        return self.spend(1)

    def openSix(self):
        state = self.state
        first = not state.flags.get(OPENED_SIX)
        state.flags[OPENED_SIX] = True
        self.game.learn(facts.INSIDE_SIX)
        self.ui.showDialogue(
            "The master key turns and the door of six swings in on its hook. "
            "Made up for one, with care, by somebody who knew how it was liked: "
            "the blanket turned down, a sprig of sea-pink on the pillow. A "
            "cardigan on the hook with a Halde School badge on the pocket. Two "
            "cups on the shelf, not one. In the drawer, crossword books - "
            "nineteen years of them, by the dates - every one filled in by two "
            "hands: a schoolteacher's round print, and a cramped capital hand "
            "that writes like a ship's log."
            if first
            else "Six, as it was: the sea-pink, the cardigan, the two cups. "
            "Nobody has come."
        )
        if first:
            self.remember("Oskar")
        return self.spend(1)

    def readTheLetter(self):
        self.state.flags[READ_THE_LETTER] = True
        self.game.learn(facts.WHAT_MAREN_WROTE)
        self.ui.showDialogue(
            "You promised. You steam the flap over the kettle anyway, and read "
            "it under the pantry lamp, and press it shut again.\n\n"
            + facts.text(facts.WHAT_MAREN_WROTE)
        )
        return self.spend(1)
