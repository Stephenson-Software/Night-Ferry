# @author Daniel McCoy Stephenson
from nightferry import facts, people
from nightferry.flags import (
    ASHES_IN_SIX,
    HANNE_CHOSE_LIGHT,
    HANNE_KNOWS,
    HANNE_PREPARED,
    INGRID_ASKED_FOR_HANNE,
    INGRID_WILL_STOP,
    KEPT_INGRIDS_SECRET,
    LET_GUS_IN,
    MET_IN_WHEELHOUSE,
)
from nightferry.scenes.base import TRAVEL_LABELS, Scene

# What there is to notice in the saloon, in no order anyone chose. Drawn
# from the night's fixed sequence, so a reloaded save sees the same night.
SALOON_SIGHTS = (
    "The bar sells tea, beer, and a sandwich that has made this crossing "
    "before. Somebody has written HALDE OR BUST in the condensation on a "
    "window and somebody else has added a question mark.",
    "The old man with the crossword says 'Seven down' aloud, to nobody, and "
    "does not fill it in.",
    "The man with the laptop has a folder of photocopied ledger pages and a "
    "pencil, and keeps ringing the same column.",
    "The woman with two tickets has not let go of them since Brekka. Her foot "
    "is against a canvas bag, and when the boat rolls she moves her foot with "
    "it.",
    "A framed photograph by the bar: the Kittiwake new, 1987, dressed overall, "
    "and a young woman in a mate's cap on the bridge wing, laughing.",
    "Oskar comes out from behind the hatch, looks along the saloon the way a "
    "man counts sheep, and goes back.",
)


class Saloon(Scene):
    id = "saloon"
    travelTo = ("corridor", "deck")

    def descriptor(self):
        state = self.state
        if state.atDeparture:
            return (
                "8:00 pm, the Halde crossing. The ferry leaves on time. Cabin 6 "
                "was paid for in cash and nobody has come aboard to claim it."
            )
        if state.hanneAsleep:
            return (
                "The saloon under the blue night lamps. Sleepers in the reclining "
                "seats under company blankets; the hatch with the purser's lamp "
                "behind it; the engines, which you have stopped hearing."
            )
        return (
            "The saloon: forty reclining seats and nine people in them, a bar, "
            "the purser's hatch, and the windows black with the sea."
        )

    def run(self):
        state = self.state
        options, actions, unavailable = [], [], {}

        def row(label, action, reason=None):
            options.append(label)
            actions.append(action)
            if reason:
                unavailable[len(options)] = reason

        row(TRAVEL_LABELS["cardeck"], ("go", "cardeck"))
        row(
            "Ask the purser about cabin 6"
            if not state.knows(facts.CABIN_SIX)
            else "Talk to Oskar, the purser",
            ("oskar", None),
            "he's walking the boat" if state.oskarOnRounds else None,
        )
        row(
            "Sit with the woman holding two tickets"
            if not state.knows(facts.THE_ASHES)
            else "Sit with Hanne",
            ("hanne", None),
            "she's asleep, sitting up, her foot against the bag"
            if state.hanneAsleep
            else None,
        )
        row(TRAVEL_LABELS["wheelhouse"], ("go", "wheelhouse"))
        if not state.fennInHisCabin:
            row(
                "Talk to the old man with the crossword"
                if not state.knows(facts.THE_TEACHER)
                and not state.knows(facts.THE_APPOINTMENTS)
                else "Talk to Dr Fenn",
                ("fenn", None),
            )
        row(
            "Talk to the man with the laptop"
            if not state.knows(facts.RASKES_AUDIT)
            else "Talk to Raske",
            ("raske", None),
            "he's on the ship's phone in the foyer" if state.raskeOnThePhone else None,
        )
        if state.raskeOnThePhone:
            row("Stand near the foyer while Raske is on the phone", ("phone", None))
        if state.knows(facts.CABIN_SIX):
            row(
                "Look through the old ledgers under the hatch",
                ("ledgers", None),
                None if state.oskarOnRounds else "Oskar is sitting on them",
            )
        if state.flags.get(INGRID_ASKED_FOR_HANNE) and not state.flags.get(HANNE_KNOWS):
            row(
                "Take Hanne up to the wheelhouse",
                ("bringHanne", None),
                "she's asleep - the captain can wait an hour, or can't"
                if state.hanneAsleep
                else None,
            )
        if (
            state.flags.get(KEPT_INGRIDS_SECRET) is True
            and state.hanneAsleep
            and not state.flags.get(ASHES_IN_SIX)
            and not state.flags.get(HANNE_KNOWS)
        ):
            reason = None
            if state.flags.get(LET_GUS_IN):
                reason = "Gus Tamm is asleep in cabin 6"
            elif not state.hanneAsleepForAnHour:
                reason = "she'll wake before the hour is out"
            row("Carry Hanne's bag to cabin 6 for an hour", ("ashes", None), reason)
        row("Look around the saloon", ("look", None))
        self.addTravel(options, actions, unavailable)

        kind, arg = self.choose(self.descriptor(), options, actions, unavailable)
        common = self.common(kind, arg)
        if common is not None:
            return common
        if kind == "oskar":
            return self.talk(people.oskar(self.game))
        if kind == "hanne":
            return self.talk(people.hanne(self.game))
        if kind == "fenn":
            return self.talk(people.fenn(self.game))
        if kind == "raske":
            return self.talk(people.raske(self.game))
        if kind == "phone":
            return self.overhear()
        if kind == "ledgers":
            return self.readLedgers()
        if kind == "bringHanne":
            return self.bringHanneUp()
        if kind == "ashes":
            return self.borrowAnHour()
        self.ui.showDialogue(state.draw(SALOON_SIGHTS))
        return self.spend(1)

    def overhear(self):
        self.game.learn(facts.LAST_WINTER)
        self.ui.showDialogue(
            "You wipe tables near the foyer. Raske has his back to you and his "
            "voice down, and the ship's phone line is bad, so he repeats "
            "everything. '...No, the night service ends in March, it's "
            "settled... The buyer takes her in April... The master was told in "
            "June, yes. She didn't say anything. She never does... The books "
            "will be clean by docking. There's one column. The purser, yes. "
            "...I know. I was at school with half this boat.' He puts the phone "
            "down and stands with his hand on it for a while."
        )
        return self.spend(1)

    def readLedgers(self):
        self.game.learn(facts.THE_LEDGER)
        self.ui.showDialogue(
            "Under the hatch, under the cash box, nineteen narrow ledgers in "
            "Oskar's square hand. You find the column without trying: cabin 6, "
            "the Friday crossing home, M. Sollid. March 2007. April 2007. Every "
            "month, never missed, always 'cash, paid in full'. None of it is in "
            "the company's computer; you check. The entries stop in June of "
            "this year. Tonight's is on a loose slip, tucked in the last page, "
            "in the same hand: 'M. Sollid - once more.'"
        )
        return self.spend(1)

    def bringHanneUp(self):
        state = self.state
        state.flags[HANNE_KNOWS] = True
        state.flags[MET_IN_WHEELHOUSE] = True
        if state.flags.get(HANNE_PREPARED):
            arrival = (
                "Hanne says, before anyone else can, 'Dr Fenn told me she went "
                "somewhere every month that made her happy. Was it you?'"
            )
        else:
            arrival = (
                "Hanne stands in the wheelhouse door with the bag in her arms "
                "and says, 'The steward says you asked for me.'"
            )
        self.ui.showDialogue(
            "You tell Hanne the captain has asked to see her, and nothing else; "
            "it is not yours to say. She brings the bag. Up two ladders, into "
            "the dark of the wheelhouse, where the only light is the radar and "
            "the binnacle.\n\n" + arrival + "\n\nIngrid Halvard tells her. All "
            "of it: the Friday boat, cabin 6, nineteen years, the crossword, the "
            "mate taking the watch at midnight, the specialist who was a ferry. "
            "Then she gives Hanne the letter, and Hanne reads it by the binnacle "
            "light and puts her hand flat on the chart table, and the two of "
            "them stand there not touching for a long time, with the boat "
            "going on underneath them as if nothing had happened."
        )
        choice = int(
            self.ui.showOptions(
                "On the ladder down, Hanne stops, with the bag against her chest. "
                "'She wants the light,' she says. 'The whole island is coming to "
                "the churchyard tomorrow, and the stone's cut. What would you "
                "do?'",
                [
                    "Do what she asked. The light.",
                    "Take her home to the churchyard. It's your decision, not hers.",
                ],
            )
        )
        if choice == 1:
            state.flags[HANNE_CHOSE_LIGHT] = True
            state.flags[INGRID_WILL_STOP] = True
            self.ui.showDialogue(
                "Hanne nods, and turns round, and goes back up the ladder. You "
                "hear her say it, and you hear the captain say 'Five o'clock. I'll "
                "stop her,' and the scratch of a pencil on the chart."
            )
        else:
            state.flags[HANNE_CHOSE_LIGHT] = False
            self.ui.showDialogue(
                "Hanne nods. 'The churchyard. She was my mother on Halde before "
                "she was anything else.' She goes down the rest of the ladder "
                "without looking back up it."
            )
        self.remember("Hanne")
        self.state.location = "saloon"
        return self.spend(1)

    def borrowAnHour(self):
        state = self.state
        state.flags[ASHES_IN_SIX] = True
        self.game.learn(facts.INSIDE_SIX)
        self.ui.showDialogue(
            "Hanne is asleep with her chin on her chest. You lift the canvas bag "
            "from against her foot, slowly, and she doesn't stir. It is heavier "
            "than you expected and lighter than it should be.\n\nYou sent word "
            "up with the captain's coffee, and Ingrid is waiting at the door of "
            "six; she has given the bridge to the mate. "
            "She opens it with her own key - made up for one, a sprig of "
            "sea-pink on the pillow, a cardigan on the hook, two cups on the "
            "shelf, a drawer of crossword books - and you set the bag on the bunk "
            "and go and sit in the steward's pantry with the door ajar. You hear "
            "her talking for a while, in an ordinary voice, about the weather.\n\n"
            "At the end of the hour she gives you the bag back without a word, "
            "and you set it against Hanne's foot again, exactly where it was. "
            "Hanne moves her foot against it in her sleep."
        )
        self.remember("Ingrid")
        return self.spend(3)
