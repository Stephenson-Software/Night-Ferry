# @author Daniel McCoy Stephenson
"""The people on the Kittiwake tonight, and what they will say to a steward
who knows enough.

Every conditional line is gated on a fact, a choice, or a property of the
state - never on the clock directly: what opens a door here is what you
know. Responses that teach something are callables, so the fact is learned
when the line is heard and not when the menu is built. Some questions are
choices, not questions - they set a flag that nothing forgets - and the
scene says "X will remember that" after them.

Every person has one question that is always on their menu, because tak
closes a conversation that has nothing left to ask.
"""

from tak import NPC

from nightferry import facts
from nightferry.flags import (
    AT_THE_DOOR,
    BROKE_YOUR_WORD,
    FENN_TELLS,
    HANNE_CHOSE_LIGHT,
    HANNE_KNOWS,
    HANNE_PREPARED,
    INGRID_ASKED_FOR_HANNE,
    INGRID_SAW_THE_SEAL,
    INGRID_TOLD_YOU,
    INGRID_WILL_STOP,
    JORY_TELLS,
    KEPT_INGRIDS_SECRET,
    LET_GUS_IN,
    LETTER_DELIVERED,
    OPENED_SIX,
    READ_THE_LETTER,
    TOLD_HANNE,
    TOLD_RASKE,
    TOVE_GAVE_LETTER,
    ASHES_IN_SIX,
)


def person(game, name, backstory, options):
    """An NPC whose every answer marks the conversation as time spent.

    Opening a conversation and backing straight out is free; asking anything
    costs a turn, charged by Scene.talk when the conversation closes."""

    def spoken(response):
        def answer():
            game.spoke = True
            return response() if callable(response) else response

        return answer

    wrapped = []
    for option in options:
        option = dict(option)
        option["response"] = spoken(option["response"])
        wrapped.append(option)
    return NPC(name, backstory, wrapped)


def undecided(state, flag):
    return flag not in state.flags


# --- the purser -------------------------------------------------------------
def oskar(game):
    state = game.state

    def cabinSix():
        game.learn(facts.CABIN_SIX)
        return (
            "Six. (He does not look up from the manifest.) Booked three weeks "
            "ago at the Brekka office. One berth, cash, M. Sollid. Nobody's "
            "come aboard for it and nobody will, I shouldn't think. It's made "
            "up, it stays made up, and it stays shut. That's the one thing I "
            "asked of you, and I'll ask it again: you have a master key, and "
            "six is not what it's for."
        )

    def whoIsSollid():
        return (
            "A passenger. Was. (He squares the manifest.) I'm from Brekka; I "
            "only sail to Halde. Ask somebody who lives there."
        )

    def harbourHouse():
        game.learn(facts.HARBOUR_HOUSE)
        return (
            "Harbour House? (A pause that is longer than the question.) The "
            "captain's. Ingrid Halvard. She's had it since her father. Why?"
        )

    def youveDoneTheSum():
        game.learn(facts.THE_CAPTAIN)
        return (
            "(He puts the pen down and looks at you properly for the first "
            "time tonight.) Then you've done the sum, and I'd rather it was said "
            "right than guessed. Mrs Sollid crossed home with us on the Friday "
            "boat every month for nineteen years, in six. When the mate took "
            "the watch at midnight, the captain went down to her. I wrote the "
            "bookings in my own hand so they'd never be in a computer, and the "
            "cash went in the till every time, to the krone. Mrs Sollid died in "
            "August. Three weeks ago the captain gave me the fare for six in an "
            "envelope and asked me to book it in Maren's name. She's in the "
            "saloon tonight, Maren is. In a bag. Her daughter doesn't know any "
            "of it. (He picks the pen up again.) That's the captain's to tell, "
            "not mine and not yours."
        )

    def raskesAudit():
        return (
            "I know what he thinks. (Flat.) Nineteen years of cash in my hand "
            "writing. I've a pension and a clean book except for one column, "
            "and I'd sooner lose the pension than explain the column. He can "
            "write what he likes."
        )

    def youOpenedIt():
        return (
            "I know. (He doesn't look up.) The sea-pink on the pillow was moved. "
            "I asked you one thing."
        )

    return person(
        game,
        "Oskar",
        "Oskar Brune, purser of the Kittiwake: fifty-eight, Brekka-born, "
        "the manifest, the cash box, the keys. He took you on this afternoon.",
        [
            {
                "question": "Anything that needs doing?",
                "response": "Coffee to the bridge when you think of it, black. "
                "The saloon's yours till the bar shuts, then it's sleepers and "
                "blankets. Don't wake anyone who's managed it.",
            },
            {
                "question": "What's the story with cabin 6?",
                "response": cabinSix,
                "condition": lambda: not state.knows(facts.CABIN_SIX),
            },
            {
                "question": "Who is M. Sollid?",
                "response": whoIsSollid,
                "condition": lambda: state.knows(facts.CABIN_SIX)
                and not state.knows(facts.THE_TEACHER),
            },
            {
                "question": "Whose is Harbour House?",
                "response": harbourHouse,
                "condition": lambda: state.knowsAny(facts.THE_PIANO, facts.THE_LETTER)
                and not state.knows(facts.HARBOUR_HOUSE),
            },
            {
                "question": "Nineteen years of Fridays in six, for a schoolteacher.",
                "response": youveDoneTheSum,
                "condition": lambda: state.knows(facts.THE_LEDGER)
                and state.knows(facts.THE_TEACHER)
                and not state.knows(facts.THE_CAPTAIN),
            },
            {
                "question": "Raske thinks you've been skimming.",
                "response": raskesAudit,
                "condition": lambda: state.knows(facts.RASKES_AUDIT),
            },
            {
                "question": "About cabin 6. I opened it.",
                "response": youOpenedIt,
                "condition": lambda: bool(state.flags.get(OPENED_SIX)),
            },
        ],
    )


# --- the woman holding two tickets ---------------------------------------
def hanne(game):
    state = game.state

    def theSecondTicket():
        game.learn(facts.THE_ASHES)
        return (
            "(She looks at the two tickets as if they had just been handed to "
            "her.) It's for my mother. (She moves her foot: there is a canvas "
            "bag against it.) She's in there. She died in August, in Brekka, "
            "and I'm taking her home - the funeral's tomorrow. I know you don't "
            "need a ticket for - for that. She always paid her own way. She'd "
            "have hated travelling on mine. I'm Hanne. Hanne Sollid."
        )

    def theChurchyard():
        game.learn(facts.THE_NOTE)
        return (
            "(She takes the folded paper out of her coat, and doesn't open it, "
            "and tells you anyway.) 'Not beside Arne. The water off the Halde "
            "light, from the boat, at first light.' That's all. With the will. "
            "My father's been in the churchyard nineteen years and the stone "
            "has her name cut on it already, under his, and the whole island "
            "will be there tomorrow. Off the light. From the boat. Like she was "
            "- like he wasn't good enough. (Quietly.) And the worst of it is "
            "I'd like to do what she says and I don't know why she said it. We "
            "didn't talk much, the last few years. I didn't get there in time "
            "at the end. A nurse did."
        )

    def tellHer():
        state.flags[TOLD_HANNE] = True
        state.flags[HANNE_KNOWS] = True
        if state.flags.get(KEPT_INGRIDS_SECRET) is True:
            state.flags[BROKE_YOUR_WORD] = True
        if state.flags.get(HANNE_PREPARED):
            opening = (
                "(She is very still.) Dr Fenn said she went somewhere every month "
                "that made her happy. He didn't know where. (A long breath.) The "
                "captain. "
            )
        else:
            opening = (
                "(She laughs, once, because it is the only thing her face can "
                "do.) The captain. The specialist. Every month. Nineteen years. "
            )
        return opening + (
            "(She looks at the bag.) She booked her the cabin. Tonight. For - "
            "(She stops.) And I was going to put her next to Dad because I "
            "thought that was what she'd want if she'd been thinking straight. "
            "(After a while:) Thank you for telling me. I think. Ask me again "
            "in a minute what I'm going to do."
        )

    def theLight():
        state.flags[HANNE_CHOSE_LIGHT] = True
        return (
            "(She nods slowly.) The light. From the boat. Like she said. (She "
            "puts the note back in her pocket and keeps her hand on it.) Somebody "
            "will have to ask the captain to stop. I don't think I can be the one "
            "who asks."
            + (
                ""
                if state.flags.get(INGRID_WILL_STOP)
                else " Will you?"
            )
        )

    def theChurchyardAfterAll():
        state.flags[HANNE_CHOSE_LIGHT] = False
        return (
            "(She nods.) The churchyard. She was my mother on Halde for "
            "forty-six years before she was anything else, and the island will "
            "be there, and Dad is there. (Not looking at you.) The captain can "
            "come. If she wants. At the back."
        )

    def undecidedAboutTheLight():
        return (
            state.flags.get(HANNE_KNOWS)
            and undecided(state, HANNE_CHOSE_LIGHT)
            and not state.lightPassed
        )

    def tea():
        if state.flags.get(HANNE_KNOWS):
            return "Please. (She holds the cup without drinking it.) Thank you."
        return (
            "Tea, please. Milk, no sugar. (She does not let go of the two "
            "tickets to take it.)"
        )

    return person(
        game,
        "Hanne",
        "A woman of about forty-five, in a good coat, holding two deck "
        "tickets in one hand, with a canvas bag at her feet she never lets "
        "out of touch.",
        [
            {"question": "Can I get you anything?", "response": tea},
            {
                "question": "Who's the second ticket for?",
                "response": theSecondTicket,
                "condition": lambda: not state.knows(facts.THE_ASHES),
            },
            {
                "question": "Something about tomorrow is wrong.",
                "response": theChurchyard,
                "condition": lambda: state.knows(facts.THE_ASHES)
                and not state.knows(facts.THE_NOTE),
            },
            {
                "question": "Cabin 6 was booked for your mother. By the captain.",
                "response": tellHer,
                "condition": lambda: state.knows(facts.THE_CAPTAIN)
                and not state.flags.get(HANNE_KNOWS),
            },
            # A choice, and she holds you to it.
            {
                "question": "Do what she asked. The light.",
                "response": theLight,
                "condition": undecidedAboutTheLight,
            },
            {
                "question": "Take her home to the churchyard. It's your decision, not hers.",
                "response": theChurchyardAfterAll,
                "condition": undecidedAboutTheLight,
            },
        ],
    )


# --- the doctor -------------------------------------------------------------
def fenn(game):
    state = game.state

    def mrsSollid():
        game.learn(facts.THE_TEACHER)
        return (
            "Maren Sollid? (He takes his glasses off.) Taught at the school for "
            "thirty-five years. Taught me nothing, I'm too old, but taught my "
            "children and their children to read and to play scales badly. "
            "Arne's heart stopped on the slipway in 2006 and I was the one who "
            "got there. The spring after that she started crossing to Brekka "
            "once a month, for the specialist. Home on the Friday boat. You "
            "could set a clock by her."
        )

    def theSpecialist():
        game.learn(facts.THE_APPOINTMENTS)
        return (
            "(He folds the newspaper very carefully.) I'll tell you, because "
            "she's dead and I'm seventy-nine and it no longer matters to "
            "anybody but her daughter. There was no specialist. She came to my "
            "surgery in the March after Arne and asked me for a referral to "
            "Brekka, every month, and I wrote one, every month, for nineteen "
            "years. There was nothing wrong with her. I never asked where she "
            "went. She came home happier than she left, and that is all the "
            "medicine I know. (A pause.) Last year there was something wrong "
            "with her, and I wrote a real one, and it was the last."
        )

    def harbourHouse():
        game.learn(facts.HARBOUR_HOUSE)
        return (
            "Harbour House is Ingrid Halvard's. The captain. Her father's "
            "before her. She's up on the bridge tonight, I'd think - she always "
            "takes the Friday."
        )

    def undecidedAboutTelling():
        return (
            state.knows(facts.THE_APPOINTMENTS)
            and undecided(state, FENN_TELLS)
            and not state.flags.get(HANNE_KNOWS)
        )

    def tellHanne():
        state.flags[FENN_TELLS] = True
        state.flags[HANNE_PREPARED] = True
        return (
            "(He looks across at the woman with the two tickets for a long "
            "time.) Yes. She's her mother's daughter; she'd rather know a hard "
            "thing than be kept from it. (He gets up, which takes a while.) I "
            "shall tell her I wrote nineteen years of lies for her mother and "
            "would write them again. She may not thank me. (He goes, and you "
            "see him lower himself into the seat beside her, and her face.)"
        )

    def letItLie():
        state.flags[FENN_TELLS] = False
        return (
            "(He nods, relieved, and is ashamed of being relieved.) It was "
            "between her and me. Let it go into the ground with her. (He picks "
            "up the crossword and does not fill anything in.)"
        )

    def crossword():
        if state.fennInHisCabin:
            return (
                "(He has the door on the latch and a book open.) I don't sleep "
                "on boats. I never have. Come in, if you're coming."
            )
        return (
            "Seven down: 'kept from the record', five letters. (He waits.) No? "
            "Nor me."
        )

    return person(
        game,
        "Dr Fenn",
        "Dr Aurel Fenn, seventy-nine: forty years the doctor on Halde, now "
        "retired, crossing home from his son's. He has delivered half the "
        "island and buried the other half.",
        [
            {"question": "Good crossword?", "response": crossword},
            {
                "question": "Did you know Maren Sollid?",
                "response": mrsSollid,
                "condition": lambda: state.knowsAny(facts.CABIN_SIX, facts.THE_ASHES)
                and not state.knows(facts.THE_TEACHER),
            },
            {
                "question": "She crossed every month to see a specialist?",
                "response": theSpecialist,
                "condition": lambda: state.knowsAny(facts.THE_ASHES, facts.THE_TEACHER)
                and not state.knows(facts.THE_APPOINTMENTS),
            },
            {
                "question": "Whose is Harbour House?",
                "response": harbourHouse,
                "condition": lambda: state.knowsAny(facts.THE_PIANO, facts.THE_LETTER)
                and not state.knows(facts.HARBOUR_HOUSE),
            },
            # A choice, and he holds you to it.
            {
                "question": "Hanne should hear that from you. Tonight.",
                "response": tellHanne,
                "condition": undecidedAboutTelling,
            },
            {
                "question": "Let it lie. It was between you and her.",
                "response": letItLie,
                "condition": undecidedAboutTelling,
            },
        ],
    )


# --- the company's man ------------------------------------------------------
def raske(game):
    state = game.state

    def theAudit():
        game.learn(facts.RASKES_AUDIT)
        return (
            "(He turns the laptop so you can see a column of figures.) Leopold "
            "Raske, for the company. I'm going through the books before the "
            "sale. And your cabin 6 isn't a one-off. Nineteen years of cash "
            "bookings, the same berth, the same name, kept in the purser's own "
            "hand and never once entered on the system. That's how a purser "
            "skims. My report goes in when we dock, and Mr Brune will be "
            "suspended. It has to be clean before the sale goes through. "
            "(He doesn't sound as if he enjoys it.)"
        )

    def showMe():
        game.learn(facts.THE_LEDGER)
        return (
            "(He shows you photographs of ledger pages.) Cabin 6, the Friday "
            "crossing home, M. Sollid. March 2007 and every month after. Cash. "
            "It stops in June this year, and starts again tonight. Whoever M. "
            "Sollid is, they're very regular and very private."
        )

    def theSale():
        game.learn(facts.LAST_WINTER)
        return (
            "(He shuts the laptop halfway.) The night crossing ends in March. "
            "The Kittiwake goes to a buyer in the south and Halde gets a day "
            "boat. I was born on Halde. I argued against it for two years and "
            "lost. Maren Sollid taught me long division and I've never forgiven "
            "her. (He opens the laptop again.) The captain was told in June."
        )

    def undecidedAboutTheTruth():
        return (
            state.knows(facts.RASKES_AUDIT)
            and state.knows(facts.THE_CAPTAIN)
            and undecided(state, TOLD_RASKE)
        )

    def tellHim():
        state.flags[TOLD_RASKE] = True
        return (
            "(He listens without typing. When you are finished he sits back.) "
            "Mrs Sollid. (A long pause.) The cash is all there, then. It was "
            "never Brune's. (He types for a minute.) I can clear him, and I "
            "will. But the board will ask what the bookings were, and I can't "
            "write 'a private matter'. It'll say they were the master's "
            "personal arrangement, kept off the books with the purser's help. "
            "They'll read her name. With the sale coming, they'll want her "
            "ashore before March. (He doesn't look up.) You knew that when you "
            "told me."
        )

    def lieToHim():
        state.flags[TOLD_RASKE] = False
        return (
            "(He looks at you for a moment longer than is comfortable.) No. Of "
            "course you don't; it's your first night. (He goes back to the "
            "column.) Then it goes in as it is. Irregular cash bookings, purser "
            "responsible."
        )

    def workingLate():
        return (
            "The company pays me by the report, not the hour. (He doesn't look "
            "up.) Coffee would be welcome."
        )

    return person(
        game,
        "Raske",
        "Leopold Raske, fifty-two, the ferry company's man: a laptop, a "
        "folder of photocopies, and a suit that has not been on a boat before.",
        [
            {"question": "Working late?", "response": workingLate},
            {
                "question": "You were asking Oskar about cabin 6.",
                "response": theAudit,
                "condition": lambda: state.knows(facts.CABIN_SIX)
                and not state.knows(facts.RASKES_AUDIT),
            },
            {
                "question": "Show me the bookings.",
                "response": showMe,
                "condition": lambda: state.knows(facts.RASKES_AUDIT)
                and not state.knows(facts.THE_LEDGER),
            },
            {
                "question": "'Before the sale goes through' - what sale?",
                "response": theSale,
                "condition": lambda: state.knows(facts.RASKES_AUDIT)
                and not state.knows(facts.LAST_WINTER),
            },
            # A choice, and he holds you to it.
            {
                "question": "The bookings were the captain's. Mrs Sollid's cabin. Every krone paid.",
                "response": tellHim,
                "condition": undecidedAboutTheTruth,
            },
            {
                "question": "I don't know anything about the bookings.",
                "response": lieToHim,
                "condition": undecidedAboutTheTruth,
            },
        ],
    )


# --- the lorry driver -------------------------------------------------------
def gus(game):
    state = game.state

    def theLoad():
        game.learn(facts.THE_PIANO)
        return (
            "A piano. (He jerks a thumb at the lorry.) Upright, from a house "
            "clearance on Halde - went over to the Brekka saleroom in September "
            "and now it's coming straight back, which is the kind of thing that "
            "keeps me in work. Says HALDE SCHOOL on the back. Some woman bought "
            "it for cash, wouldn't give a name, paid for delivery to Harbour "
            "House, Halde. Whoever that is."
        )

    def undecidedAboutTheCabin():
        return (
            state.knows(facts.CABIN_SIX)
            and undecided(state, LET_GUS_IN)
            and not state.flags.get(AT_THE_DOOR)
        )

    def letHimIn():
        state.flags[LET_GUS_IN] = True
        state.flags[OPENED_SIX] = True
        game.learn(facts.INSIDE_SIX)
        return (
            "(He is up out of the cab before you've finished.) You're a saint. "
            "(At the door of six he goes quiet, because you have opened it and "
            "you can both see it: made up for one, a sprig of sea-pink on the "
            "pillow, a cardigan on the hook, two cups on the shelf.) Somebody's - "
            "(He takes his boots off in the corridor and puts the sea-pink on "
            "the shelf, carefully, and the cardigan on the chair.) I'll not "
            "touch anything. I'll be gone by five. You never saw me."
        )

    def sayNo():
        state.flags[LET_GUS_IN] = False
        return (
            "(He takes it well, mostly.) Spoken for. Right. (He settles back into "
            "the cab and puts the radio on low.) My back'll remember you, if I "
            "don't."
        )

    def theBack():
        if state.flags.get(LET_GUS_IN):
            return "Like a new man. Don't tell anyone."
        return (
            "Like a dropped crate. Eleven hours in a cab seat. (He shifts.) They "
            "say there's a cabin going spare down there."
        )

    return person(
        game,
        "Gus",
        "Gus Tamm, fifty-five, driving: one lorry on the car deck, a flask, "
        "a radio, and a back that has done thirty years of night boats.",
        [
            {"question": "How's the back?", "response": theBack},
            {
                "question": "What are you hauling?",
                "response": theLoad,
                "condition": lambda: not state.knows(facts.THE_PIANO),
            },
            # A choice, and he holds you to it.
            {
                "question": "All right. Cabin 6, till Halde. Not a word.",
                "response": letHimIn,
                "condition": undecidedAboutTheCabin,
            },
            {
                "question": "No. That cabin's spoken for.",
                "response": sayNo,
                "condition": undecidedAboutTheCabin,
            },
        ],
    )


# --- the student ------------------------------------------------------------
def jory(game):
    state = game.state

    def goingHome():
        game.learn(facts.JORYS_TERM)
        return (
            "For the funeral. (He pulls his headphones down round his neck.) "
            "And because I left. The conservatory. In September. Mum and Dad "
            "think I'm on a reading week, and they're meeting the boat with a "
            "banner, probably. Mrs Sollid got me in there - she wrote the letter, "
            "she drove me to the audition - and she died in August and I sat at "
            "a piano in a practice room in Brekka and couldn't. I haven't "
            "touched one since. (He laughs at nothing.) I'm going to stand at "
            "her grave tomorrow in a suit they bought me for recitals."
        )

    def mrsSollid():
        game.learn(facts.THE_TEACHER)
        return (
            "Mrs Sollid taught everybody. School, then piano, Tuesdays. "
            "Thirty-five years. Her husband died when I was tiny. She crossed "
            "to Brekka once a month for some doctor and came back on the Friday "
            "boat - this boat - in a cabin, always. I used to see her on the "
            "corridor when I was little and we were going to my gran's."
        )

    def theDoor():
        game.learn(facts.THE_DOOR)
        return (
            "Funny you should ask. (He nods at the stairwell.) Before we sailed, "
            "I was out here and you can see straight down the corridor through "
            "that door. The captain came down. On her own. Stopped at six, put "
            "her hand flat on the door, like you'd feel if a stove was hot. "
            "Stood there maybe a minute. Didn't open it. Went back up. I thought "
            "it was a ship thing."
        )

    def harbourHouse():
        game.learn(facts.HARBOUR_HOUSE)
        return (
            "Harbour House? That's the captain's. Ingrid Halvard. Big white "
            "house on the mole. She used to let us jump off her slipway."
        )

    def undecidedAboutTelling():
        return state.knows(facts.JORYS_TERM) and undecided(state, JORY_TELLS)

    def tellThem():
        state.flags[JORY_TELLS] = True
        return (
            "(He breathes out.) On the quay. Before the banner. Before the suit. "
            "Yes. (He puts the headphones back on and doesn't play anything.) "
            "She'd have said the same, she'd just have said it quicker."
        )

    def afterSaturday():
        state.flags[JORY_TELLS] = False
        return (
            "After Saturday. (Relieved.) One thing at a time. They'll have "
            "enough on, with the funeral. (He believes it about halfway.)"
        )

    def cold():
        if state.lightInSight:
            return (
                "That's the Halde light, there. (He points.) You can see it from "
                "three, if you know where to look. I always know where to look."
            )
        return "Better than inside. (He doesn't elaborate.)"

    return person(
        game,
        "Jory",
        "Jory Pell, nineteen, a Halde boy: a student's coat, headphones, the "
        "stern rail, and a cigarette he isn't smoking.",
        [
            {"question": "Cold out here.", "response": cold},
            {
                "question": "Going home?",
                "response": goingHome,
                "condition": lambda: not state.knows(facts.JORYS_TERM),
            },
            {
                "question": "Did you know Maren Sollid?",
                "response": mrsSollid,
                "condition": lambda: state.knowsAny(facts.CABIN_SIX, facts.THE_ASHES)
                and not state.knows(facts.THE_TEACHER),
            },
            {
                "question": "Seen anybody near cabin 6?",
                "response": theDoor,
                "condition": lambda: state.knows(facts.CABIN_SIX)
                and not state.knows(facts.THE_DOOR),
            },
            {
                "question": "Whose is Harbour House?",
                "response": harbourHouse,
                "condition": lambda: state.knowsAny(facts.THE_PIANO, facts.THE_LETTER)
                and not state.knows(facts.HARBOUR_HOUSE),
            },
            # A choice, and he holds you to it.
            {
                "question": "Tell them on the quay. Before the funeral.",
                "response": tellThem,
                "condition": undecidedAboutTelling,
            },
            {
                "question": "Let it wait till after Saturday.",
                "response": afterSaturday,
                "condition": undecidedAboutTelling,
            },
        ],
    )


# --- the nurse --------------------------------------------------------------
def deliverTheLetter(game, byTove):
    """The letter reaches I.H. Returns what was seen, for whoever carried it."""
    state = game.state
    state.flags[LETTER_DELIVERED] = True
    state.flags[INGRID_ASKED_FOR_HANNE] = True
    game.learn(facts.THE_CAPTAIN)
    game.learn(facts.WHAT_MAREN_WROTE)
    if not byTove and state.flags.get(READ_THE_LETTER):
        state.flags[INGRID_SAW_THE_SEAL] = True
    seal = (
        " She turns it over before she opens it and sees that the flap has "
        "been lifted and pressed down again. She looks at you once, and opens "
        "it anyway."
        if state.flags.get(INGRID_SAW_THE_SEAL)
        else ""
    )
    told = ""
    if not state.flags.get(INGRID_TOLD_YOU):
        state.flags[INGRID_TOLD_YOU] = True
        told = (
            "\n\n(To you, because you are the one standing there.) She came home "
            "with me on the Friday boat every month for nineteen years. Cabin "
            "6. When the mate took the watch at midnight I went down to her. "
            "The island thought she had a specialist. I booked six tonight so "
            "she could come home in it once more, and then I couldn't make my "
            "feet go down the stairs."
        )
    return (
        "(The captain takes the envelope and reads 'For I.H.' in a hand she "
        "has known for nineteen years, and sits down on the chart stool, "
        "which you suspect she has never done on watch.%s She reads it twice. "
        "Then she reads it aloud, because she cannot keep it in.)\n\n%s\n\n"
        "(She folds it along the old folds.) Nineteen years she couldn't tell "
        "her own daughter, and now she wants me to. That's Maren.%s (She "
        "stands up.) Bring Hanne up to me. Please. Before I think better of it."
        % (seal, facts.text(facts.WHAT_MAREN_WROTE), told)
    )


def tove(game):
    state = game.state

    def whatTakesYou():
        game.learn(facts.THE_LETTER)
        return (
            "(She has a sealed envelope on her knee and puts her hand over it "
            "when you look.) Tove. I'm a nurse - was, at the hospice in Brekka. "
            "There's a job going at the care home on Halde and I said I'd look "
            "at it. (She lifts her hand.) And this. A patient gave it to me the "
            "week she died. Maren. 'For I.H. - on the Friday boat.' She said "
            "I'd know them. I don't. I've been sitting in here since Brekka "
            "trying to work out how you ask a whole boat if anyone's I.H."
        )

    def undecidedAboutTheLetter():
        return (
            state.knows(facts.THE_LETTER)
            and state.knowsAny(facts.HARBOUR_HOUSE, facts.THE_CAPTAIN)
            and undecided(state, TOVE_GAVE_LETTER)
            and not state.flags.get(LETTER_DELIVERED)
        )

    def giveItToMe():
        state.flags[TOVE_GAVE_LETTER] = True
        return (
            "(She looks at you, and at the envelope, and you can see her "
            "deciding that a steward's jacket is good enough.) All right. (She "
            "holds it out.) She said it mattered more than anything she'd left. "
            "Don't open it. Promise. (You take it. She watches it go into your "
            "inside pocket as if it were one of her patients being wheeled away.)"
        )

    def comeUpWithMe():
        state.flags[TOVE_GAVE_LETTER] = False
        state.location = "wheelhouse"
        return (
            "(She stands up so fast she has to hold the bunk.) Now, before I lose "
            "my nerve. (You take her up the two ladders to the bridge, and she "
            "says 'Are you I.H.?' before the captain has turned round.)\n\n"
            + deliverTheLetter(game, byTove=True)
            + "\n\n(Tove goes back down alone, lighter, and you stay.)"
        )

    def needAnything():
        if state.flags.get(LETTER_DELIVERED):
            return "No. (She smiles for the first time.) Not now."
        return "No. Thank you. (Her hand stays on the envelope.)"

    return person(
        game,
        "Tove",
        "Tove Ness, thirty-one, in cabin 4 with the door open: a nurse's "
        "sensible shoes, a holdall, and a sealed envelope.",
        [
            {"question": "Do you need anything?", "response": needAnything},
            {
                "question": "What takes you to Halde?",
                "response": whatTakesYou,
                "condition": lambda: not state.knows(facts.THE_LETTER),
            },
            # A choice, and she holds you to it.
            {
                "question": "I know who I.H. is. Give it to me; I'll see she gets it.",
                "response": giveItToMe,
                "condition": undecidedAboutTheLetter,
            },
            {
                "question": "She's on the bridge. Come up with me and give it to her yourself.",
                "response": comeUpWithMe,
                "condition": undecidedAboutTheLetter,
            },
        ],
    )


# --- the captain ------------------------------------------------------------
def ingrid(game):
    state = game.state

    def bookedToSollid():
        return (
            "Then it's booked. (She does not take her eyes off the radar.) "
            "Bookings are Mr Brune's. The bridge is mine. Was there coffee?"
        )

    def whoWasItFor():
        state.flags[INGRID_TOLD_YOU] = True
        if state.knows(facts.THE_CAPTAIN):
            how = "Oskar's told you, or you'd not be asking it like that. Then hear it from me. "
        elif state.knows(facts.INSIDE_SIX):
            how = "You've been in six. (Not a question.) Then you've seen the cups. "
        elif state.knows(facts.THE_DOOR):
            how = "Somebody saw me at the door. (She almost smiles.) Jory Pell, I'd guess; he never did go below when he was told. "
        else:
            how = "Harbour House. The piano. (She closes her eyes for a second.) I'm not as careful as I was. "
        game.learn(facts.THE_CAPTAIN)
        return how + (
            "(She hands the wheel to the autopilot and turns round.) Maren "
            "Sollid. She came home with me on the Friday boat every month for "
            "nineteen years. When the mate took the watch at midnight I went "
            "down to six, and we did the crossword, and she told me about her "
            "pupils, and I told her about the weather, and at five I came back "
            "up to bring her in. That was all of it and it was everything. The "
            "island thought she had a specialist. Her daughter thinks so still. "
            "(She looks at the dark.) Three weeks ago I paid for six in her "
            "name, because she always came home in it and I couldn't stand the "
            "thought of her coming home in a bag on the deck. And then her "
            "daughter booked two deck tickets, and I have not been able to make "
            "my feet go down those stairs. (A long pause.) So. Now you know what "
            "I know, steward. What are you going to do with it?"
        )

    def undecidedAboutTheSecret():
        return (
            state.flags.get(INGRID_TOLD_YOU)
            and undecided(state, KEPT_INGRIDS_SECRET)
            and not state.flags.get(LETTER_DELIVERED)
            and not state.flags.get(HANNE_KNOWS)
        )

    def keepIt():
        state.flags[KEPT_INGRIDS_SECRET] = True
        return (
            "(She nods once, and turns back to the glass.) Thank you. It was "
            "hers to tell and she never did, and I find I can't do it for her. "
            "(After a while, not turning round:) If there were an hour - when "
            "the saloon's dark and her daughter's asleep - that she could be in "
            "six, where she always was. I'd not ask it. I'm only saying it."
        )

    def hanneShouldKnow():
        state.flags[KEPT_INGRIDS_SECRET] = False
        return (
            "(She doesn't turn round.) Then tell her. I've had nineteen years to "
            "and I couldn't, and I can't now. If you tell her, tell her it was "
            "good. (Quietly:) It was so good."
        )

    def theLetter():
        return deliverTheLetter(game, byTove=False)

    def stopAtTheLight():
        state.flags[INGRID_WILL_STOP] = True
        return (
            "(She looks at the chart, though she knows it better than her own "
            "hand.) Five o'clock, the light abeam to port. I'll stop her. "
            "Engines off, two minutes, nobody asks why. (She marks the chart "
            "with a pencil.) The company won't like it. The company is selling "
            "her in March; the company can write me a letter."
        )

    def theSale():
        return (
            "March. (Unsurprised.) I was told in June. Why do you think I booked "
            "the cabin tonight? It's the last Friday boat I'll have that she'd "
            "have known."
        )

    def theHour():
        return (
            "(She doesn't turn round for a while.) Thank you. I sat with her. "
            "It was the right cabin."
        )

    def theDoor():
        return (
            "(She has the letter in her breast pocket.) Not the way either of us "
            "would have chosen. In a corridor, at four, with a man in socks "
            "behind a door. But it's said. She'd have laughed at that, Maren."
            if state.flags.get(LET_GUS_IN)
            else "(She has the letter in her breast pocket.) Not the way either "
            "of us would have chosen. In a corridor, at four. But it's said."
        )

    def coffee():
        return "Black. Put it there. (She doesn't look round.) Thank you, steward."

    return person(
        game,
        "Ingrid",
        "Captain Ingrid Halvard, sixty-four, master of the Kittiwake for "
        "twenty-two years. She keeps the Friday night watch herself and "
        "always has.",
        [
            {"question": "Coffee, captain?", "response": coffee},
            {
                "question": "Cabin 6 is booked to an M. Sollid.",
                "response": bookedToSollid,
                "condition": lambda: state.knows(facts.CABIN_SIX)
                and not state.knows(facts.THE_CAPTAIN)
                and not state.knowsAny(
                    facts.THE_DOOR, facts.INSIDE_SIX, facts.HARBOUR_HOUSE
                ),
            },
            {
                "question": "Who was cabin 6 for, captain?",
                "response": whoWasItFor,
                "condition": lambda: state.knowsAny(
                    facts.THE_DOOR, facts.INSIDE_SIX, facts.HARBOUR_HOUSE, facts.THE_CAPTAIN
                )
                and not state.flags.get(INGRID_TOLD_YOU)
                and not state.flags.get(LETTER_DELIVERED)
                and not state.flags.get(HANNE_KNOWS),
            },
            # A choice, and she holds you to it.
            {
                "question": "I'll keep it.",
                "response": keepIt,
                "condition": undecidedAboutTheSecret,
            },
            {
                "question": "Hanne should know.",
                "response": hanneShouldKnow,
                "condition": undecidedAboutTheSecret,
            },
            {
                "question": "This is from Maren. The nurse who sat with her brought it.",
                "response": theLetter,
                "condition": lambda: state.flags.get(TOVE_GAVE_LETTER) is True
                and not state.flags.get(LETTER_DELIVERED),
            },
            {
                "question": "Hanne wants the light. Will you stop the ship at five?",
                "response": stopAtTheLight,
                "condition": lambda: state.flags.get(HANNE_CHOSE_LIGHT) is True
                and not state.flags.get(INGRID_WILL_STOP)
                and not state.lightPassed,
            },
            {
                "question": "Raske says the Kittiwake's being sold.",
                "response": theSale,
                "condition": lambda: state.knows(facts.LAST_WINTER)
                and state.knows(facts.THE_CAPTAIN),
            },
            {
                "question": "She was in six for an hour.",
                "response": theHour,
                "condition": lambda: bool(state.flags.get(ASHES_IN_SIX)),
            },
            {
                "question": "About the corridor.",
                "response": theDoor,
                "condition": lambda: bool(state.flags.get(AT_THE_DOOR)),
            },
        ],
    )


# Who says "will remember that" when a flag is set.
REMEMBERED = {
    KEPT_INGRIDS_SECRET: "Ingrid",
    BROKE_YOUR_WORD: "Ingrid",
    INGRID_SAW_THE_SEAL: "Ingrid",
    ASHES_IN_SIX: "Ingrid",
    TOLD_HANNE: "Hanne",
    HANNE_CHOSE_LIGHT: "Hanne",
    FENN_TELLS: "Dr Fenn",
    TOLD_RASKE: "Raske",
    LET_GUS_IN: "Gus",
    JORY_TELLS: "Jory",
    TOVE_GAVE_LETTER: "Tove",
    OPENED_SIX: "Oskar",
}
