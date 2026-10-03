# @author Daniel McCoy Stephenson
"""The people on the last night boat, and what they will say.

The same rules as nightferry.people: every conditional line is gated on a
fact, a choice, a property of the state, or what the first crossing left
behind (lastboat.carried) - never on the clock directly. Choices set a flag
that nothing forgets, and the scene says who will remember it.
"""

from nightferry import endings as firstEndings
from nightferry import flags
from nightferry.flags import (
    BOOKS_TO_HANNE,
    COLUMN_TO_HANNE,
    GUS_OPENS_THE_LORRY,
    HANNE_KNOCKS,
    INGRID_GIVES_BOOKS,
    INGRID_HEARD_THE_PIANO,
    INGRID_TOLD_YOU_TONIGHT,
    JORY_PLAYS,
    LETTER_TO_HANNE,
    OSKAR_GAVE_COLUMN,
    PER_TELLS_HER,
    TOLD_HANNE_TONIGHT,
)
from nightferry.lastboat import carried, facts
from nightferry.people import person, undecided


# --- the purser -------------------------------------------------------------
def oskar(game):
    state = game.state

    def cabinSix():
        game.learn(facts.SIX_TONIGHT)
        return (
            "(He doesn't look up from the manifest, and then he does.) Six is "
            "booked. Halde office, cash, one berth: I. Halvard. She came up the "
            "ramp at seven with a suitcase and a box she wouldn't let me carry, "
            "put them both in six, and went up to the bridge, which isn't her "
            "bridge tonight. She's asked one thing: nobody disturbs six. (A "
            "pause.) Last time it was my rule. This time it's hers."
            + (
                " You didn't keep mine."
                if carried.firedInOctober(state)
                else " I'd keep it."
            )
        )

    def theLedgers():
        game.learn(facts.OSKARS_COLUMN)
        cost = (
            " That column cost me five months' suspension and I'd not explain it "
            "to an inquiry. I'll not have it read by a clerk in the south."
            if not carried.oskarCleared(state)
            else " Raske's seen it. The board's seen it. The buyer won't."
        )
        return (
            "They go to the buyer with the ship. Every book this boat ever kept "
            "goes south on Monday. (He puts his hand flat on the stack.) All but "
            "one column. Cabin 6, M. Sollid, a Friday a month for nineteen years, "
            "in my hand. I'm tearing it out tonight and putting it in the galley "
            "stove before we're in." + cost
        )

    def giveMeTheColumn():
        state.flags[OSKAR_GAVE_COLUMN] = True
        return (
            "(He looks at you for a long time. Then he opens the books one after "
            "another and runs his thumb down each gutter and tears, neatly, the "
            "way a purser tears, until nineteen years of one column are folded "
            "into an envelope.) Somebody. (He hands it over.) Mind who."
        )

    def burnIt():
        state.flags[OSKAR_GAVE_COLUMN] = False
        return (
            "(He nods, as if you'd passed something.) It was. (He puts the "
            "ledgers under his arm.) The galley stove's warm."
        )

    def theTicket():
        game.learn(facts.TICKET_SOUTH)
        return (
            "(He squares the manifest, which is square.) I booked it. A room at "
            "the Mission in Brekka on Monday, and Tuesday's train south, to her "
            "sister in Tromsund. Single. (He says it the way you'd put down "
            "something hot.) She asked me to tell nobody on Halde. You're not "
            "Halde."
        )

    def october():
        if carried.oskarCleared(state):
            board = (
                "Raske cleared me in October, because you told him what the "
                "column was. It put her name in front of the board. She's never "
                "once said it was your fault."
            )
        else:
            board = (
                "They suspended me at the quay in October. The inquiry sat in "
                "January and proved nothing, because I'd not explain one column, "
                "and I got the last month back. There's no purser on a day boat."
            )
        if carried.firedInOctober(state):
            job = (
                " I said I'd not keep you on, and I haven't. This is one night. "
                "(Nearly a smile.) The last one wanted somebody who'd met her."
            )
        else:
            job = " You've done the Friday boat every week since. Tonight's the last."
        return board + job

    return person(
        game,
        "Oskar",
        "Oskar Brune, purser, on his last night as one: the manifest, the cash "
        "box, the keys, and nineteen narrow ledgers tied in a stack for the buyer.",
        [
            {
                "question": "Anything that needs doing?",
                "response": "Coffee to the bridge: Mr Aasen's black, two sugars; the "
                "captain's, if she'll take it from you. The bar shuts at eleven, "
                "for the last time. After that it's blankets.",
            },
            {
                "question": "What's the story with cabin 6 tonight?",
                "response": cabinSix,
                "condition": lambda: not state.knows(facts.SIX_TONIGHT),
            },
            {
                "question": "What happens to your ledgers?",
                "response": theLedgers,
                "condition": lambda: state.knows(facts.SIX_TONIGHT)
                and not state.knows(facts.OSKARS_COLUMN),
            },
            # A choice, and he holds you to it.
            {
                "question": "Give me the column instead. Somebody has a right to it.",
                "response": giveMeTheColumn,
                "condition": lambda: state.knows(facts.OSKARS_COLUMN)
                and undecided(state, OSKAR_GAVE_COLUMN),
            },
            {
                "question": "Burn it. It was theirs.",
                "response": burnIt,
                "condition": lambda: state.knows(facts.OSKARS_COLUMN)
                and undecided(state, OSKAR_GAVE_COLUMN),
            },
            {
                "question": "Where's the captain going, after Brekka?",
                "response": theTicket,
                "condition": lambda: state.knows(facts.HOUSE_SOLD)
                and not state.knows(facts.TICKET_SOUTH),
            },
            {"question": "About October.", "response": october},
        ],
    )


# --- the mate ---------------------------------------------------------------
def per(game):
    state = game.state

    def notInCommand():
        game.learn(facts.THE_PASSENGER)
        if carried.oskarCleared(state):
            why = (
                "The board read Raske's report in December: cabin 6 kept off the "
                "books 'by private arrangement of the master'. They retired her in "
                "January. Full pension and a letter. She asked to make the last "
                "crossing as a passenger, and they couldn't think of a reason to "
                "say no."
            )
        elif carried.octoberEnding(state) == firstEndings.OFF_THE_LIGHT:
            why = (
                "She stopped this ship off the Halde light in October with the "
                "company's man aboard, and the company wrote her a letter. She "
                "kept her command through the winter. Then she asked them to give "
                "me the last crossing. She'd sooner be a passenger than be the one "
                "who brings her in for the last time."
            )
        else:
            why = (
                "She asked the company to give me the last one. Twenty-two years "
                "she's brought the Kittiwake in. She said she'd not be the one to "
                "bring her in for the last time."
            )
        return why + (
            " (He glances back. She is at the back of the wheelhouse, looking at "
            "the dark ahead.) She's been standing there since we cast off. I "
            "could tell her to go below. I'm not going to."
        )

    def theWatch():
        game.learn(facts.MATES_WATCH)
        return (
            "(He keeps his voice down; she is ten feet away.) Nineteen years. "
            "Midnight, every Friday: 'Mr Aasen, you have the watch.' Back up at "
            "five. I wrote 'Master below' in the log every time, as if she'd gone "
            "to bed. I knew by the second month. Six, and the schoolteacher, and "
            "the crossword - you could hear them laughing through the deckhead "
            "if the wind was right. I never said. She'd have stopped, if she'd "
            "known anybody knew. So nobody knew."
        )

    def theNightBook():
        game.learn(facts.THE_STOP)
        return (
            "(He opens the night order book and turns it so you can read it: "
            "'0500 - STOP ENGINES, TWO MINUTES. I.H.') It's not her book tonight. "
            "I'll do it anyway; I've never refused her. I asked her what for. She "
            "said 'ballast'. (He closes the book.) We don't carry ballast."
        )

    def tellHer():
        state.flags[PER_TELLS_HER] = True
        return (
            "(He looks at the back of her head for a while.) At midnight, then. "
            "When she gives me the watch. (Very quietly.) Nineteen years I've been "
            "waiting for somebody to tell me I could."
        )

    def letHerGo():
        state.flags[PER_TELLS_HER] = False
        return (
            "(He nods.) That's what she wanted. That's what I've given her. (He "
            "doesn't sound sure, and he doesn't change his mind.)"
        )

    return person(
        game,
        "Per",
        "Per Aasen, fifty-eight, mate of the Kittiwake for nineteen years and "
        "master of her for one night: a heavy jersey with the epaulettes he has "
        "not got used to, and the wheel.",
        [
            {
                "question": "Evening, Mr Aasen.",
                "response": "Captain, tonight. (He tries the word and doesn't like "
                "it.) Mr Aasen'll do. Coffee's welcome.",
            },
            {
                "question": "Why isn't the captain in command?",
                "response": notInCommand,
                "condition": lambda: not state.knows(facts.THE_PASSENGER),
            },
            {
                "question": "You took the watch at midnight, on Fridays.",
                "response": theWatch,
                "condition": lambda: state.knows(facts.THE_PASSENGER)
                and not state.knows(facts.MATES_WATCH),
            },
            {
                "question": "What's in the night order book?",
                "response": theNightBook,
                "condition": lambda: state.knows(facts.THE_PASSENGER)
                and not state.knows(facts.THE_STOP),
            },
            # A choice, and he holds you to it.
            {
                "question": "Tell her you knew. Before she goes.",
                "response": tellHer,
                "condition": lambda: state.knows(facts.MATES_WATCH)
                and undecided(state, PER_TELLS_HER)
                and state.ingridOnTheBridge,
            },
            {
                "question": "Let her go thinking nobody knew.",
                "response": letHerGo,
                "condition": lambda: state.knows(facts.MATES_WATCH)
                and undecided(state, PER_TELLS_HER)
                and state.ingridOnTheBridge,
            },
        ],
    )


# --- the captain, a passenger -------------------------------------------------
def ingrid(game):
    state = game.state

    def coffee():
        if state.ingridInSix:
            return (
                "(The door opens a hand's width. She takes the cup.) Thank you, "
                "steward. (It closes.)"
            )
        return "Not captain. (She takes it anyway.) Black. Thank you, steward."

    def notInCommand():
        game.learn(facts.THE_PASSENGER)
        return (
            "Because she's Mr Aasen's tonight, and he's earned her. (She doesn't "
            "move.) And because I couldn't bring her in for the last time. You've "
            "met me, steward. You know the things I can't do."
        )

    def houseSold():
        return (
            "It was too big for one. (A pause.) It was always too big for one. "
            "It's sold."
        )

    def whereAreYouGoing():
        state.flags[INGRID_TOLD_YOU_TONIGHT] = True
        game.learn(facts.THE_ANSWER)
        game.learn(facts.THE_BOX)
        if state.knows(facts.THE_STOP):
            how = "Per's shown you the night book. (Not a question.) "
        elif state.knows(facts.TICKET_SOUTH):
            how = "Oskar. (She almost smiles.) I asked him to tell nobody on Halde. "
        else:
            how = "You've a way of finding things out on this boat. "
        if carried.hanneKnewInOctober(state):
            hanne = (
                " Hanne knows where her mother went: every month, since October "
                "she knows. Maren asked me to tell her which days, and I've never "
                "made my mouth say them."
            )
        elif carried.hanneKnows(state):
            hanne = (
                " And you've told her daughter, tonight. (Not a question; it is "
                "on your face.) Then she knows where. She doesn't know which days. "
                "Maren asked me to tell her that, and I never have."
            )
        elif carried.letterInYourPocket(state):
            hanne = (
                " Her daughter still doesn't know. Nobody has told her, and I "
                "haven't, and after Tuesday nobody will."
            )
        else:
            hanne = (
                " Her daughter still doesn't know. The nurse brought me Maren's "
                "letter a week after the funeral - 'if H. is on the boat, tell "
                "her' - and H. wasn't on the boat, and I didn't."
            )
        return how + (
            "Away. "
            + (
                "(She says it to the porthole.) "
                if state.ingridInSix
                else "(She says it to the dark ahead.) "
            )
            + "The house is sold. The piano's "
            "on the car deck going back to the saleroom. I've a single south on "
            "Tuesday, to my sister, who hasn't seen me since our father's funeral. "
            "(She turns round.) And in six there's a box. Every crossword we did - "
            "nineteen years of Fridays, both our hands. At five, when I'd go back "
            "up, Per stops her for two minutes, and they go over the side. "
            "Mid-channel. Not off the light; the light was Maren's. They're the "
            "only place any of it was ever written down, and I'll not have them "
            "read by a stranger at a house clearance when I'm dead."
            + hanne
            + " (A long pause.) So. Now you know what I know, steward. Again."
        )

    def giveThemToHanne():
        if not carried.persuadable(state):
            return (
                "(She shakes her head.) Hanne has never asked me for anything. She "
                "doesn't want a box of crosswords. She wants her mother, and I "
                "can't give her that. (She turns away.) No."
            )
        state.flags[INGRID_GIVES_BOOKS] = True
        if state.knows(facts.THE_CROSSES):
            why = (
                "(You tell her about the diaries: a pencil cross on one Friday a "
                "month, two hundred and twenty-six of them, and Hanne reading the "
                "empty pages on a night boat because she cannot stop.) She "
                "counted them. (She sits down, because there is nothing else to "
                "do.) She's been counting them, and I've been carrying the answer "
                "about in a box marked ballast. "
            )
        else:
            why = (
                "I heard him. Under the floor of six, the Grieg, the way she "
                "taught it - too fast on the second page, she'd have said. (She "
                "puts her hand flat on the bulkhead.) She'd not have let me throw "
                "a single one. "
            )
        return why + (
            "At five, then. Not over the side. Into her hands. Bring her to the "
            "stern, steward, and I'll tell her which days."
        )

    def doWhatYouCameToDo():
        state.flags[INGRID_GIVES_BOOKS] = False
        return (
            "(She nods once.) Thank you. (After a while.) It's the first thing "
            "anyone's let me decide for myself since June. Five o'clock."
        )

    def undecidedAboutTheBooks():
        return (
            state.knows(facts.THE_ANSWER)
            and undecided(state, INGRID_GIVES_BOOKS)
            and not carried.booksSettled(state)
            and (state.ingridOnTheBridge or state.ingridInSix)
        )

    def heardThePiano():
        return (
            "I heard. (She doesn't open the door any wider.) She'd have said he "
            "rushed the second page. She'd have been right. She'd have cried "
            "anyway."
        )

    def perKnew():
        return (
            "He told me. At the change of watch, as if it were the weather: 'I "
            "have the watch, captain. I always knew where you were. I was glad.' "
            "(A long pause.) Nineteen years, and the one who knew was the one "
            "who never said. I said 'Thank you, Mr Aasen,' and came down. I'd "
            "have liked to say more."
        )

    def october():
        ending = carried.octoberEnding(state)
        if state.pastFlag(flags.BROKE_YOUR_WORD):
            return (
                "You promised me, and then you told her. (Not unkindly.) I'd "
                "decided to forgive you before we docked. I've not told you so "
                "until now."
            )
        if ending == firstEndings.OFF_THE_LIGHT:
            return (
                "The light. (She looks astern, though it is long gone.) I've "
                "still the pencil mark on the chart. The company wrote me a "
                "letter. I have it framed."
            )
        if ending == firstEndings.AT_THE_DOOR:
            return (
                "A corridor, at four in the morning. (She looks at her hands.) "
                "Hanne hasn't spoken to me since. I don't blame her. I'd not "
                "have chosen it either."
            )
        if ending == firstEndings.BESIDE_ARNE:
            return (
                "She put her beside Arne. I stood at the back, as Hanne asked. "
                "It was a good stone. It had the wrong name next to hers."
            )
        hour = (
            " And the hour. I sat with her, in six, while her daughter slept. "
            "I've not thanked you for that."
            if state.pastFlag(flags.ASHES_IN_SIX)
            else ""
        )
        return "You kept it. I've thought about that every Friday since." + hour

    return person(
        game,
        "Ingrid",
        "Ingrid Halvard, sixty-five, for twenty-two years master of the "
        "Kittiwake and tonight a passenger in cabin 6: the same coat, no "
        "epaulettes, and her hands behind her back as if she still had a "
        "bridge.",
        [
            {"question": "Coffee, captain?", "response": coffee},
            {
                "question": "Why aren't you in command tonight?",
                "response": notInCommand,
                "condition": lambda: not state.knows(facts.THE_PASSENGER),
            },
            {
                "question": "Harbour House is sold.",
                "response": houseSold,
                "condition": lambda: state.knows(facts.HOUSE_SOLD)
                and not state.knows(facts.THE_ANSWER),
            },
            {
                "question": "Where are you going, Ingrid?",
                "response": whereAreYouGoing,
                "condition": lambda: carried.readyToTell(state)
                and not state.flags.get(INGRID_TOLD_YOU_TONIGHT),
            },
            # A choice, and she holds you to it.
            {
                "question": "Give the books to Hanne. They're the days her mother meant.",
                "response": giveThemToHanne,
                "condition": undecidedAboutTheBooks,
            },
            {
                "question": "They're yours. Do what you came to do.",
                "response": doWhatYouCameToDo,
                "condition": undecidedAboutTheBooks,
            },
            {
                "question": "Jory played her piano.",
                "response": heardThePiano,
                "condition": lambda: bool(state.flags.get(INGRID_HEARD_THE_PIANO)),
            },
            {
                "question": "Per always knew.",
                "response": perKnew,
                "condition": lambda: state.flags.get(PER_TELLS_HER) is True
                and state.ingridInSix,
            },
            {"question": "About October.", "response": october},
        ],
    )


# --- the daughter -------------------------------------------------------------
def theBooksToHanne(game, atTheStern):
    """Ingrid gives Hanne the crossword books. Returns what was seen."""
    state = game.state
    state.flags[BOOKS_TO_HANNE] = True
    game.learn(facts.THE_BOX)
    game.learn(facts.THE_MARGINS)
    game.learn(facts.THE_ANSWER)
    toldHer = ""
    if (
        not carried.hanneKnewInOctober(state)
        and not state.flags.get(TOLD_HANNE_TONIGHT)
        and not state.flags.get(LETTER_TO_HANNE)
    ):
        toldHer = (
            "Ingrid tells her first, all of it, the way Maren asked her to in a "
            "letter five months ago: the Friday boat, cabin 6, nineteen years, "
            "the mate taking the watch at midnight, the specialist who was a "
            "ferry. Hanne holds the diary shut with both hands until it is "
            "finished. "
        )
    where = (
        "At the stern rail, with the engines stopped and the dark going grey, "
        if atTheStern
        else "In cabin 6, on the bunk, with the door open on the corridor, "
    )
    return (
        where + toldHer + "Ingrid unties the string. She takes out the top book "
        "and opens it at a Friday in May, years ago, and puts her finger beside "
        "the margin: 'Happy. - M.' 'That one,' she says. She opens another. "
        "'And that one. Not that one; that was the winter her back was bad, she "
        "was cross all night. That one.' Hanne opens her mother's diary on her "
        "knee beside the box, and finds the cross, and the date, and the word, "
        "and does it again, and again, and it goes on for a long time, and "
        "neither of them notices the boat."
    )


def hanne(game):
    state = game.state

    def tea():
        return "Tea, please. Milk, no sugar. (She doesn't look up from the diary.)"

    def theCrosses():
        game.learn(facts.THE_CROSSES)
        ending = carried.octoberEnding(state)
        if ending == firstEndings.OFF_THE_LIGHT:
            opening = (
                "I come over once a month now. Friday boat to Halde, the night "
                "boat back. I stand at the stern when we pass the light. (She has "
                "a small diary on her knee.) "
            )
        elif ending == firstEndings.AT_THE_DOOR:
            opening = (
                "I haven't spoken to the captain since the corridor. I don't know "
                "if I'm going to. I saw her come up the ramp and I went and sat "
                "the other side of the saloon. (She has a small diary on her "
                "knee.) "
            )
        elif ending == firstEndings.BESIDE_ARNE:
            opening = (
                "Mum's stone was finished in January, with both their names on "
                "it the way the island wanted. (She has a small diary on her "
                "knee.) "
            )
        else:
            opening = (
                "We buried Mum in October, beside Dad. (She has a small diary on "
                "her knee.) "
            )
        if carried.hanneKnows(state):
            meaning = (
                "I know where she was. I know who with. 'Every month,' the "
                "captain said. And there they are, every month - and a cross is "
                "not a day. Mum asked her to tell me which days. I don't know "
                "what any of them were."
            )
        else:
            meaning = (
                "I don't know what they mean. I've asked half of Halde whether "
                "she saw a doctor in Brekka on Fridays. Dr Fenn changed the "
                "subject, and he never changes the subject."
            )
        return opening + (
            "Mum's. I've nineteen of them, from clearing the house. One Friday a "
            "month there's a little pencil cross, and nothing else on the page. "
            "Two hundred and twenty-six. I counted. (She closes it.) " + meaning
        )

    def tellHerTonight():
        state.flags[TOLD_HANNE_TONIGHT] = True
        return (
            "(She holds the diary shut with both hands while you tell her: the "
            "Friday boat, cabin 6, the captain going down at midnight, nineteen "
            "years.) The captain. (She looks along the saloon towards the "
            "stairs, as if Ingrid might be standing there.) Two hundred and "
            "twenty-six times. And I buried her next to Dad because I thought "
            "she wasn't thinking straight at the end. (After a long while.) "
            "Thank you. I think. Don't ask me yet what I'm going to do."
        )

    def theLetter():
        state.flags[LETTER_TO_HANNE] = True
        return (
            "(You give her the envelope from your inside pocket. It is soft at "
            "the corners. 'For I.H. - on the Friday boat.' She reads it twice, "
            "the second time aloud, very quietly.) 'If H. is on the boat, tell "
            "her. I never found the way to... Tell her I was happy, and on which "
            "days.' (She looks up.) I was on the boat. (She looks at the "
            "diary.) These are the days. (Then, not loudly:) You've had this "
            "since October."
        )

    def goAndKnock():
        state.flags[HANNE_KNOCKS] = True
        return (
            "(She stands up with the diary in her hand and goes, and you follow "
            "as far as the corridor. She knocks on six the way you knock at a "
            "door you are not sure you are allowed to knock at. It opens.) "
            "\n\n" + theBooksToHanne(game, atTheStern=False)
        )

    def leaveHer():
        state.flags[HANNE_KNOCKS] = False
        return (
            "(She nods, and opens the diary again.) Not tonight. She has a right "
            "to her last crossing. (She doesn't look towards the stairs.)"
        )

    def theColumn():
        state.flags[COLUMN_TO_HANNE] = True
        return (
            "(She unfolds the pages: cabin 6, M. Sollid, Friday, cash, paid in "
            "full, in a purser's square hand, nineteen years of it. She lays the "
            "diary beside them and runs her finger down both.) Every one. (She "
            "doesn't look up.) He wrote down every one, and so did she."
            + (
                " And so did they."
                if state.flags.get(BOOKS_TO_HANNE)
                else " Nobody wrote down what they were."
            )
        )

    def undecidedAboutKnocking():
        return (
            carried.hanneKnows(state)
            and state.knows(facts.THE_BOX)
            and state.ingridInSix
            and undecided(state, HANNE_KNOCKS)
            and not carried.booksSettled(state)
        )

    return person(
        game,
        "Hanne",
        "Hanne Sollid, in the same good coat, on her own this time: no tickets "
        "in her hand, no bag at her feet, and a small diary on her knee that "
        "she keeps opening at the same page.",
        [
            {"question": "Can I get you anything?", "response": tea},
            {
                "question": "Crossing back to Brekka?",
                "response": theCrosses,
                "condition": lambda: not state.knows(facts.THE_CROSSES),
            },
            {
                "question": "The crosses are the Fridays she came home in cabin 6. The captain went down to her.",
                "response": tellHerTonight,
                "condition": lambda: state.knows(facts.THE_CROSSES)
                and not carried.hanneKnows(state)
                and (carried.youKnewInOctober(state) or state.knows(facts.THE_ANSWER)),
            },
            {
                "question": "I have your mother's letter. I've had it since October.",
                "response": theLetter,
                "condition": lambda: carried.letterInYourPocket(state)
                and not state.flags.get(LETTER_TO_HANNE),
            },
            # A choice, and she holds you to it.
            {
                "question": "She's in six with nineteen years of your mother's Fridays. Go and knock.",
                "response": goAndKnock,
                "condition": undecidedAboutKnocking,
            },
            {
                "question": "Leave her tonight.",
                "response": leaveHer,
                "condition": undecidedAboutKnocking,
            },
            {
                "question": "This is from the purser's ledgers. Every Friday, in his hand.",
                "response": theColumn,
                "condition": lambda: state.flags.get(OSKAR_GAVE_COLUMN) is True
                and not state.flags.get(COLUMN_TO_HANNE)
                and carried.hanneKnows(state),
            },
        ],
    )


# --- the lorry driver -------------------------------------------------------
def gus(game):
    state = game.state

    def theBack():
        if state.pastFlag(flags.LET_GUS_IN) is True:
            return "Never better since a certain cabin. (He winks.) Not a word."
        if state.pastFlag(flags.LET_GUS_IN) is False:
            return "It remembers you, my back does. (He grins, mostly.)"
        return "Like a dropped crate. (He shifts.) Last night boat. Day boat Monday."

    def theLoad():
        game.learn(facts.PIANO_AGAIN)
        slept = (
            " And it turned out I'd slept in her cabin, the first time. I've not "
            "stopped apologising."
            if state.pastFlag(flags.LET_GUS_IN) is True
            else ""
        )
        return (
            "You'll laugh. (He doesn't.) Same piano. Third time. Halde to Brekka "
            "in September, back to Halde in October, and tonight to Brekka again: "
            "consigned to the saleroom by I. Halvard, 'any price', and two crates "
            "of her house behind it. HALDE SCHOOL on the back. In October I "
            "delivered it to Harbour House and the captain opened the door and "
            "put her hand on the lid and didn't say anything for a minute, and "
            "tipped me forty." + slept
        )

    def openTheBack():
        state.flags[GUS_OPENS_THE_LORRY] = True
        return (
            "(He looks at you, and at the boy on the stairs, and gets the knife "
            "out for the straps.) On your head, steward. It's sold, and insured "
            "strapped. (He folds the blankets like flags.) I'll want to hear it, "
            "mind."
        )

    def keepItStrapped():
        state.flags[GUS_OPENS_THE_LORRY] = False
        return "(Relieved.) Sold's sold. (He pats the tarpaulin.) Sorry, son."

    def undecidedAboutTheBack():
        return (
            state.knows(facts.PIANO_AGAIN)
            and state.flags.get(JORY_PLAYS) is True
            and undecided(state, GUS_OPENS_THE_LORRY)
        )

    return person(
        game,
        "Gus",
        "Gus Tamm, driving: the same lorry, the same flask, the same radio, "
        "and a back that has done thirty years of night boats and has one left.",
        [
            {"question": "How's the back?", "response": theBack},
            {
                "question": "What are you hauling this time?",
                "response": theLoad,
                "condition": lambda: not state.knows(facts.PIANO_AGAIN),
            },
            # A choice, and he holds you to it.
            {
                "question": "Open the back for Jory. I'll answer for it.",
                "response": openTheBack,
                "condition": undecidedAboutTheBack,
            },
            {
                "question": "Keep it strapped. It's sold.",
                "response": keepItStrapped,
                "condition": undecidedAboutTheBack,
            },
        ],
    )


# --- the student ------------------------------------------------------------
def jory(game):
    state = game.state

    def cold():
        if state.haldeLightAstern:
            return (
                "That's the Halde light, going. (He doesn't look at it.) Last time "
                "anyone'll see it from a night boat."
            )
        if state.brekkaInSight:
            return "Brekka. (He puts his hands in his pockets.) Monday."
        return "Better than inside. (He means it differently from last time.)"

    def goingBack():
        game.learn(facts.JORYS_AUDITION)
        told = state.pastFlag(flags.JORY_TELLS)
        if told is True:
            home = (
                "I told Mum and Dad on the quay in October, before the banner. Mum "
                "cried, Dad said 'well, then'. In January Dad drove me to the boat "
                "and said 'try again', so. "
            )
        elif told is False:
            home = (
                "I told them after the funeral, like I said. It went worse than it "
                "would've on the quay. They're speaking to me now. "
            )
        else:
            home = (
                "They still think I'm in my second year. If I get back in on "
                "Monday they'll never know I left. "
            )
        return home + (
            "(He takes a folded sheaf of music out of his coat and doesn't open "
            "it.) Monday, ten o'clock, the conservatory. The Grieg. I haven't "
            "touched a piano since August. I think I'll freeze."
        )

    def harbourHouse():
        game.learn(facts.HOUSE_SOLD)
        return (
            "Harbour House? There's a SOLD board on the gate since February. "
            "Holiday lets. (He kicks the rail.) My mum says the captain's leaving "
            "and hasn't told anybody, which is how my mum knows."
        )

    def playIt():
        state.flags[JORY_PLAYS] = True
        return (
            "(He goes white, and then he takes the music out of his coat.) After "
            "midnight. When they're all asleep. (He swallows.) If the driver'll "
            "open it. Ask him? I can't ask him."
        )

    def saveIt():
        state.flags[JORY_PLAYS] = False
        return "(Relieved.) Monday. (He puts the music away.) Yeah. Monday."

    def undecidedAboutPlaying():
        return (
            state.knows(facts.JORYS_AUDITION)
            and state.knows(facts.PIANO_AGAIN)
            and undecided(state, JORY_PLAYS)
        )

    return person(
        game,
        "Jory",
        "Jory Pell, twenty, at the stern rail again: the student's coat, the "
        "headphones, no cigarette this time, and a sheaf of music in his "
        "pocket.",
        [
            {"question": "Cold out here.", "response": cold},
            {
                "question": "Going back to Brekka?",
                "response": goingBack,
                "condition": lambda: not state.knows(facts.JORYS_AUDITION),
            },
            {
                "question": "Anything new on Halde?",
                "response": harbourHouse,
                "condition": lambda: state.knowsAny(
                    facts.SIX_TONIGHT, facts.THE_PASSENGER
                )
                and not state.knows(facts.HOUSE_SOLD),
            },
            # A choice, and he holds you to it.
            {
                "question": "Her piano's on the car deck. Play it tonight.",
                "response": playIt,
                "condition": undecidedAboutPlaying,
            },
            {
                "question": "Save it for Monday.",
                "response": saveIt,
                "condition": undecidedAboutPlaying,
            },
        ],
    )


# Who says "will remember that" when a flag is set.
REMEMBERED = {
    OSKAR_GAVE_COLUMN: "Oskar",
    flags.OPENED_SIX_AGAIN: "Oskar",
    PER_TELLS_HER: "Per",
    INGRID_GIVES_BOOKS: "Ingrid",
    HANNE_KNOCKS: "Hanne",
    TOLD_HANNE_TONIGHT: "Hanne",
    LETTER_TO_HANNE: "Hanne",
    GUS_OPENS_THE_LORRY: "Gus",
    JORY_PLAYS: "Jory",
}
