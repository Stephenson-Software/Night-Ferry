# @author Daniel McCoy Stephenson
"""The places on the last night boat. The same boat and the same menus as
the first crossing (scenes.base.Scene), with the second crossing's clock,
last page and people."""

from nightferry import flags
from nightferry.lastboat import carried
from nightferry.lastboat import crossing as lastCrossing
from nightferry.lastboat import endings as lastEndings
from nightferry.lastboat import facts, people
from nightferry.scenes.base import TRAVEL_LABELS, Scene
from nightferry.scenes.journal import Journal, octoberPage

QUIT = "quit"

SALOON_SIGHTS = (
    "Somebody has written LAST ONE in the condensation on a window, and "
    "somebody else has drawn a ship under it, sinking, and somebody else has "
    "rubbed the ship out.",
    "The framed photograph by the bar has gone - the Kittiwake new, 1987, and "
    "a young mate laughing on the bridge wing. There is a pale square on the "
    "panelling where it hung.",
    "Half the saloon are Halde people crossing for no reason but to have been "
    "on the last one. They are very quiet about it.",
    "Oskar comes out from behind the hatch, looks along the saloon the way a "
    "man counts sheep, and goes back, and you see him write the number down.",
    "The bar sells tea, beer, and the last of the sandwiches. Nobody complains "
    "about them tonight.",
)

SEA = (
    "The wake goes back white into the dark and closes over.",
    "No lights anywhere. Somewhere ahead there is a mainland and a railway and "
    "a Tuesday.",
    "A gannet, or something the size of one, follows the stern light for a "
    "while and then is not there.",
    "The wind is north-west and cold. Somebody has tied a black ribbon to the "
    "stern rail, and it stands out straight.",
)


class LastBoatScene(Scene):
    clock = lastCrossing
    lastPage = lastEndings
    remembered = people.REMEMBERED


class Saloon(LastBoatScene):
    id = "saloon"
    travelTo = ("corridor", "deck")

    def descriptor(self):
        if self.state.atDeparture:
            return (
                "8:00 pm, the last night crossing. The ramp comes up at Halde "
                "for the last time. Cabin 6 is booked in the captain's own name."
            )
        if self.state.quietHours:
            return (
                "The saloon under the blue night lamps. Nobody is asleep who is "
                "not pretending. Oskar's lamp is still on behind the hatch."
            )
        return (
            "The saloon: forty reclining seats and all of them taken for once, a "
            "bar, the purser's hatch, and the windows black with the sea."
        )

    def run(self):
        state = self.state
        options, actions, unavailable = [], [], {}
        options.append(TRAVEL_LABELS["cardeck"])
        actions.append(("go", "cardeck"))
        options.append(
            "Ask the purser about cabin 6"
            if not state.knows(facts.SIX_TONIGHT)
            else "Talk to Oskar, the purser"
        )
        actions.append(("oskar", None))
        options.append("Sit with Hanne Sollid")
        actions.append(("hanne", None))
        options.append(TRAVEL_LABELS["wheelhouse"])
        actions.append(("go", "wheelhouse"))
        options.append("Look around the saloon")
        actions.append(("look", None))
        self.addTravel(options, actions, unavailable)

        kind, arg = self.choose(self.descriptor(), options, actions, unavailable)
        common = self.common(kind, arg)
        if common is not None:
            return common
        if kind == "oskar":
            return self.talk(people.oskar(self.game))
        if kind == "hanne":
            return self.talk(people.hanne(self.game))
        self.ui.showDialogue(state.draw(SALOON_SIGHTS))
        return self.spend(1)


class CarDeck(LastBoatScene):
    id = "cardeck"
    travelTo = ("saloon", "corridor", "deck", "wheelhouse")

    def descriptor(self):
        if self.state.flags.get(flags.PIANO_PLAYED):
            return (
                "The car deck: the cars, the fish van, and Gus's lorry with its "
                "tailgate down and Maren's piano under its blankets again, a fish "
                "box still in front of it."
            )
        return (
            "The car deck: a dozen cars, a van of fish boxes, the smell of diesel "
            "and wet rope, and one lorry with a tarpaulin over its load and the "
            "same radio going low in the cab."
        )

    def run(self):
        state = self.state
        options, actions, unavailable = [], [], {}
        options.append(
            "Talk to Gus"
            if state.knows(facts.PIANO_AGAIN)
            else "Talk to the lorry driver"
        )
        actions.append(("gus", None))
        options.append("Lift the tarpaulin on the lorry")
        actions.append(("tarpaulin", None))
        if (
            state.flags.get(flags.JORY_PLAYS) is True
            and state.flags.get(flags.GUS_OPENS_THE_LORRY) is True
            and not state.flags.get(flags.PIANO_PLAYED)
        ):
            options.append("Fetch Jory down to the piano")
            actions.append(("piano", None))
            if not state.quietHours:
                unavailable[
                    len(options)
                ] = "he won't play to a full saloon - after midnight"
        self.addTravel(options, actions, unavailable)

        kind, arg = self.choose(self.descriptor(), options, actions, unavailable)
        common = self.common(kind, arg)
        if common is not None:
            return common
        if kind == "gus":
            return self.talk(people.gus(self.game))
        if kind == "piano":
            return self.playThePiano()
        if self.game.learn(facts.PIANO_AGAIN):
            self.ui.showDialogue(
                "You know before you lift it. An upright piano, strapped and "
                "blanketed, HALDE SCHOOL stencilled on the back in white paint "
                "gone yellow. A new docket taped over the old one: 'Ex Harbour "
                "House, Halde. Consignor I. Halvard. To Brekka saleroom - ANY "
                "PRICE.' Two crates behind it, stencilled HALVARD."
            )
        else:
            self.ui.showDialogue(
                "Maren's piano, under its blankets, leaving the island for the "
                "second time. Any price, the docket says."
            )
        return self.spend(1)

    def playThePiano(self):
        state = self.state
        state.flags[flags.PIANO_PLAYED] = True
        heard = ""
        if state.ingridInSix:
            state.flags[flags.INGRID_HEARD_THE_PIANO] = True
            heard = (
                "\n\nThe car deck is steel, and steel carries. Above your head, "
                "through the deck plates, in the cabin corridor, a door opens and "
                "does not close."
            )
        self.ui.showDialogue(
            "Jory comes down the ladder as if it were the stairs to an exam. Gus "
            "has the tailgate down and the blankets off, and sets a fish box in "
            "front of the keys and says, 'Go on, then.' Jory sits. He does not "
            "take the music out. For a long time he does nothing at all, and then "
            "he plays the Grieg - badly for a page, too fast, the way she told "
            "him not to, and then not badly, and then the way nobody on the car "
            "deck of a night boat has any right to hear it. Gus takes his cap "
            "off. When it is finished Jory sits with his hands in his lap and "
            "says, to the keys, 'She'd have said the second page was rushed.'" + heard
        )
        return self.spend(1)


class Corridor(LastBoatScene):
    id = "corridor"
    travelTo = ("saloon", "cardeck", "deck", "wheelhouse")

    def descriptor(self):
        state = self.state
        if state.ingridInSix:
            return (
                "The cabin corridor: eight doors, the fire hose, the linen "
                "cupboard, your pantry, and cabin 6, with a line of light under "
                "the door."
            )
        if state.ingridAtTheStern:
            return (
                "The cabin corridor. The door of six stands open on a made bed "
                "and an empty drawer."
            )
        return (
            "The cabin corridor: eight doors, the fire hose, the linen cupboard, "
            "your pantry, and cabin 6, dark, with a card in the slot in the "
            "captain's capitals: I. HALVARD."
        )

    def run(self):
        state = self.state
        options, actions, unavailable = [], [], {}
        if state.ingridOnTheBridge:
            options.append(
                "Open cabin 6 with your master key"
                if not state.flags.get(flags.OPENED_SIX_AGAIN)
                else "Look into six again"
            )
            actions.append(("six", None))
            if state.flags.get(flags.OPENED_SIX_AGAIN) and not state.flags.get(
                flags.READ_A_BOOK
            ):
                options.append("Untie the string and read one of the books")
                actions.append(("read", None))
        elif state.ingridInSix:
            options.append("Knock at cabin 6")
            actions.append(("ingrid", None))
        options.append("Sit in the steward's pantry for an hour")
        actions.append(("wait", None))
        self.addTravel(options, actions, unavailable)

        kind, arg = self.choose(self.descriptor(), options, actions, unavailable)
        common = self.common(kind, arg)
        if common is not None:
            return common
        if kind == "six":
            return self.openSix()
        if kind == "read":
            return self.readABook()
        if kind == "ingrid":
            return self.talk(people.ingrid(self.game))
        self.ui.showDialogue(
            "You sit in the pantry with the door open and the kettle ticking. "
            "There are people on this boat who have done this crossing every "
            "week of their lives, and none of them is asleep."
        )
        return self.spend(3)

    def openSix(self):
        state = self.state
        first = not state.flags.get(flags.OPENED_SIX_AGAIN)
        state.flags[flags.OPENED_SIX_AGAIN] = True
        self.game.learn(facts.THE_BOX)
        if first:
            self.ui.showDialogue(
                "The master key turns. Six is as it always was - the bunk made up, "
                "the two cups on the shelf - except that the drawer is empty, and "
                "on the bunk there is a suitcase with a Tromsund label, and beside "
                "it a cardboard box tied with string. Through the string, the "
                "spines of crossword books, dozens of them, every one dated on "
                "the cover: always a Friday. A luggage label on the knot, in "
                "cramped capitals: BALLAST."
            )
            self.remember("Oskar")
        else:
            self.ui.showDialogue(
                "Six, as it was: the suitcase, the box, the label. BALLAST."
            )
        return self.spend(1)

    def readABook(self):
        self.state.flags[flags.READ_A_BOOK] = True
        self.game.learn(facts.THE_MARGINS)
        self.ui.showDialogue(
            "Not yours to untie, and you untie it. You take one from the middle: "
            "a Friday in May, eleven years ago. The squares are filled in by two "
            "hands. The margins are, too. 'SW 6, rain later. - I.' 'Jory Pell "
            "played the Grieg at last. - M.' And at the bottom of the page, in "
            "round print: 'Happy. - M.' You turn to another Friday. 'Fog. Stayed "
            "till half five. - I.' 'Happy. - M.' You tie the string again, not "
            "quite as it was."
        )
        return self.spend(1)


class Deck(LastBoatScene):
    id = "deck"
    travelTo = ("saloon", "cardeck", "corridor", "wheelhouse")

    def descriptor(self):
        state = self.state
        if state.flags.get(flags.AT_THE_STERN) and not carried.booksSettled(state):
            return (
                "The stern rail, five o'clock, the engines stopped. The box is on "
                "the rail between the captain's hands, the string untied. "
                "'Well, steward?'"
            )
        if state.ingridAtTheStern:
            return (
                "The open deck, astern, in the grey. The captain is at the rail "
                "with her hands behind her back. Off the bow, Brekka."
            )
        if state.haldeLightAstern:
            return (
                "The open deck, astern. Wet steel, the rail, the wake, and behind "
                "you the Halde light, getting smaller. A young man in a student's "
                "coat at the rail."
            )
        return (
            "The open deck, astern. Wet steel, the rail, the wake, the dark. Jory "
            "at the rail with his headphones round his neck."
        )

    def run(self):
        state = self.state
        if state.flags.get(flags.AT_THE_STERN) and not carried.booksSettled(state):
            return self.atTheRail()
        options, actions, unavailable = [], [], {}
        options.append(
            "Talk to Jory"
            if state.knows(facts.JORYS_AUDITION)
            else "Talk to the young man at the rail"
        )
        actions.append(("jory", None))
        if state.ingridAtTheStern:
            options.append("Talk to Ingrid")
            actions.append(("ingrid", None))
        options.append("Look out over the water")
        actions.append(("look", None))
        self.addTravel(options, actions, unavailable)

        kind, arg = self.choose(self.descriptor(), options, actions, unavailable)
        common = self.common(kind, arg)
        if common is not None:
            return common
        if kind == "jory":
            return self.talk(people.jory(self.game))
        if kind == "ingrid":
            return self.talk(people.ingrid(self.game))
        if state.haldeLightAstern:
            self.ui.showDialogue(
                "The Halde light: three white flashes, then dark, then three "
                "again, smaller each time. The first thing on the island anyone "
                "sees coming home, and the last thing going."
            )
        elif state.brekkaInSight:
            self.ui.showDialogue(
                "Brekka, low and orange along the bow: cranes, the station, the "
                "railway going south out of the lights."
            )
        else:
            self.ui.showDialogue(state.draw(SEA))
        return self.spend(1)

    def atTheRail(self):
        """Five o'clock, and the choice put to the steward - unless it was
        already made. It takes no time: the engines are stopped for two
        minutes, and this is what they were stopped for."""
        state = self.state
        options = [
            "Give them to Hanne. They're the days her mother meant.",
            "Take them with you. They're yours.",
            "Let them go.",
        ]
        choice = int(self.ui.showOptions(self.descriptor(), options))
        if choice == 1 and carried.persuadable(state):
            if state.knows(facts.THE_CROSSES):
                why = (
                    "You tell her about the diaries: a pencil cross on one Friday "
                    "a month, two hundred and twenty-six of them, and Hanne "
                    "reading the empty pages on a night boat because she cannot "
                    "stop."
                )
            else:
                why = (
                    "You don't have to say anything. She heard Jory play the "
                    "Grieg under the floor of six, on Maren's piano, and she is "
                    "still hearing it."
                )
            self.ui.showDialogue(
                why + " The captain closes the lid of the box with her hand flat "
                "on it. 'Fetch her,' she says. You fetch her. Hanne comes up the "
                "ladder with her mother's diary in her coat.\n\n"
                + people.theBooksToHanne(self.game, atTheStern=True)
            )
        elif choice == 1:
            state.flags[flags.BOOKS_OVERBOARD] = True
            self.ui.showDialogue(
                "'Hanne has never asked me for anything,' she says. 'She doesn't "
                "want a box of crosswords. She wants her mother.' And she drops "
                "them, one at a time, nineteen years of Fridays, and the wake "
                "takes each one and turns it over and it is gone. Up on the "
                "bridge Per rings the engines on again, and does not look aft."
            )
        elif choice == 2:
            state.flags[flags.BOOKS_KEPT] = True
            self.ui.showDialogue(
                "She looks at you for a long moment, and then she ties the string "
                "again, the same knot, and holds the box against her coat. 'Mine,' "
                "she says, as if trying the word. Up on the bridge Per rings the "
                "engines on, and the Kittiwake goes on towards Brekka with "
                "nothing gone over the side."
            )
        else:
            state.flags[flags.BOOKS_OVERBOARD] = True
            self.ui.showDialogue(
                "She drops them one at a time, nineteen years of Fridays, and the "
                "wake takes each one and turns it over and it is gone. When the "
                "box is empty she folds it flat and puts it under her arm. Up on "
                "the bridge Per rings the engines on again, and does not look aft."
            )
        self.remember("Ingrid")
        return self.after()


class Wheelhouse(LastBoatScene):
    id = "wheelhouse"
    travelTo = ("saloon", "cardeck", "corridor", "deck")

    def descriptor(self):
        if self.state.ingridOnTheBridge:
            return (
                "The wheelhouse: dark, warm, the radar sweeping green. Per Aasen "
                "at the wheel in epaulettes he has not got used to, and at the "
                "back, in the dark, with her hands behind her back, the captain."
            )
        return (
            "The wheelhouse: dark, warm, the radar sweeping green, Per Aasen at "
            "the wheel, and the back of the wheelhouse empty."
        )

    def run(self):
        state = self.state
        options, actions, unavailable = [], [], {}
        options.append("Talk to Per Aasen, the mate")
        actions.append(("per", None))
        if state.ingridOnTheBridge:
            options.append("Talk to the captain")
            actions.append(("ingrid", None))
        options.append("Read the night order book")
        actions.append(("book", None))
        self.addTravel(options, actions, unavailable)

        kind, arg = self.choose(self.descriptor(), options, actions, unavailable)
        common = self.common(kind, arg)
        if common is not None:
            return common
        if kind == "per":
            return self.talk(people.per(self.game))
        if kind == "ingrid":
            return self.talk(people.ingrid(self.game))
        if self.game.learn(facts.THE_STOP):
            self.ui.showDialogue(
                "The night order book, open at tonight. Per's orders in his "
                "careful hand, and under them, in the cramped capitals of a woman "
                "who is not master tonight: '0500 - STOP ENGINES, TWO MINUTES. "
                "I.H.' Per has initialled it."
            )
        else:
            self.ui.showDialogue(
                "0500 - STOP ENGINES, TWO MINUTES. I.H. Initialled, P.A."
            )
        return self.spend(1)


class Epilogue(LastBoatScene):
    """After the last night boat. Both last pages can be read again."""

    id = "epilogue"
    travelTo = ()

    def run(self):
        options = [
            "Read the last page again",
            "Read October's last page",
            "Open your notebook",
            "Quit",
        ]
        label = options[
            int(
                self.ui.showOptions(
                    "Brekka, six in the morning: %s. The last night boat is "
                    "alongside, and the ramp is down." % lastEndings.name(self.state),
                    options,
                )
            )
            - 1
        ]
        if label == "Read the last page again":
            self.ui.showDialogue(lastEndings.text(self.state))
            return self.id
        if label == "Read October's last page":
            self.ui.showDialogue(octoberPage(self.state))
            return self.id
        if label == "Open your notebook":
            self.game.returnTo = self.id
            return self.go("journal")
        return QUIT


class LastBoatJournal(Journal, LastBoatScene):
    pass


def build(game):
    return {
        "saloon": Saloon(game),
        "cardeck": CarDeck(game),
        "corridor": Corridor(game),
        "deck": Deck(game),
        "wheelhouse": Wheelhouse(game),
        "journal": LastBoatJournal(game),
        "epilogue": Epilogue(game),
    }
