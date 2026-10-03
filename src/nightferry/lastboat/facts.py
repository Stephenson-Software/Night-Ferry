# @author Daniel McCoy Stephenson
"""Everything the player can come to know on the last night boat.

The same shape as nightferry.facts - a title, the notebook's line, and the
leads that say where to look next without naming what is there - for the
second crossing: Halde to Brekka in March, the Kittiwake's last night run.
The first crossing's facts are not here; they are remembered in State.past.

There are thirteen, and all thirteen can be learned on one crossing.
"""

SIX_TONIGHT = "six_tonight"
THE_PASSENGER = "the_passenger"
HOUSE_SOLD = "house_sold"
PIANO_AGAIN = "piano_again"
TICKET_SOUTH = "ticket_south"
THE_STOP = "the_stop"
THE_BOX = "the_box"
THE_MARGINS = "the_margins"
THE_CROSSES = "the_crosses"
MATES_WATCH = "mates_watch"
OSKARS_COLUMN = "oskars_column"
JORYS_AUDITION = "jorys_audition"
THE_ANSWER = "where_she_is_going"

FACTS = {
    SIX_TONIGHT: {
        "title": "Cabin 6, tonight",
        "text": "Booked at the Halde office, one berth, cash, in the name of I. "
        "Halvard. The captain came up the ramp at seven as a passenger, with a "
        "suitcase and a cardboard box tied with string, put them in six, and went "
        "up to the wheelhouse, where she is not in command. The one rule tonight "
        "is hers: nobody disturbs six.",
        "leads": [
            {
                "to": THE_PASSENGER,
                "text": "Somebody else has the ship tonight, and he has stood on "
                "that bridge every Friday for nineteen years.",
            },
            {
                "to": HOUSE_SOLD,
                "text": "A suitcase and a box, on a boat that is not coming back. "
                "Halde will have noticed something; the island always does.",
            },
            {
                "to": THE_BOX,
                "text": "You have a master key, and six stands empty until she "
                "goes down to it.",
            },
            {
                "to": THE_CROSSES,
                "text": "Hanne Sollid is on the passenger list again, crossing "
                "back to Brekka on her own.",
            },
        ],
    },
    THE_PASSENGER: {
        "title": "Not in command",
        "text": "Per Aasen, the mate for nineteen years, has the Kittiwake "
        "tonight: master for one crossing, the last. The captain is aboard as a "
        "passenger. She stands at the back of the wheelhouse with her hands "
        "behind her back, where he could tell her to go below, and he would not.",
        "leads": [
            {
                "to": MATES_WATCH,
                "text": "Per took the midnight watch every Friday for nineteen "
                "years, and nobody ever asked him why he was taking it.",
            },
            {
                "to": THE_STOP,
                "text": "There is an order in the night book in the captain's "
                "hand, and the mate does not like it.",
            },
        ],
    },
    HOUSE_SOLD: {
        "title": "Harbour House, sold",
        "text": "A SOLD board has been on the gate of Harbour House since "
        "February - to a company that lets houses to summer people. It was the "
        "captain's father's house, and Maren's piano was in it. Ingrid has not "
        "told anyone on Halde where she is going.",
        "leads": [
            {
                "to": PIANO_AGAIN,
                "text": "Everything in that house went somewhere. Some of it is on "
                "the car deck tonight.",
            },
            {
                "to": TICKET_SOUTH,
                "text": "Somebody booked the captain's onward travel. Somebody "
                "books everything on this boat.",
            },
        ],
    },
    PIANO_AGAIN: {
        "title": "The piano, again",
        "text": "Gus Tamm has Maren's piano in his lorry for the third time: Halde "
        "to Brekka in September, back to Halde in October, and tonight to Brekka "
        "again, consigned to the saleroom by I. Halvard, 'any price'. Two crates "
        "from Harbour House behind it. HALDE SCHOOL on the back.",
        "leads": [
            {
                "to": JORYS_AUDITION,
                "text": "Her last pupil is on this boat, going back to Brekka, and "
                "he has not touched a piano since August.",
            },
            {
                "to": THE_ANSWER,
                "text": "Nobody sells a piano like that at any price unless they "
                "mean never to hear it again.",
            },
        ],
    },
    TICKET_SOUTH: {
        "title": "A single",
        "text": "Oskar booked it for her: a room in Brekka on Monday night, and "
        "Tuesday's train south, single, to a sister in Tromsund she has not "
        "visited in thirty years. Not a return. She asked him to tell nobody on "
        "Halde. He has told you, because you asked the right way.",
        "leads": [
            {
                "to": THE_BOX,
                "text": "She would not let Oskar carry the cardboard one up the "
                "ramp. She carried it herself, like something that might spill.",
            },
        ],
    },
    THE_STOP: {
        "title": "Five o'clock",
        "text": "In the night order book, in the captain's cramped capitals: "
        "'0500 - STOP ENGINES, TWO MINUTES. I.H.' It is not her book to write in "
        "tonight, and Per will do it anyway; he has never refused her. She told "
        "him it was for ballast. Five was the hour she always went back up to "
        "bring the ship in.",
        "leads": [
            {
                "to": THE_BOX,
                "text": "Ballast. Whatever she means to put over the side, she "
                "brought it aboard in her own arms.",
            },
            {
                "to": THE_ANSWER,
                "text": "Two minutes, mid-channel, at the hour she always went "
                "back up. Ask her what for.",
            },
        ],
    },
    THE_BOX: {
        "title": "The box",
        "text": "In cabin 6, beside her suitcase, a cardboard box tied with "
        "string: the crossword books from the drawer of six, nineteen years of "
        "them, every one filled in by two hands and dated on the cover - always a "
        "Friday. A luggage label on the string, in her hand: BALLAST.",
        "leads": [
            {
                "to": THE_MARGINS,
                "text": "There is writing in those books that is not in the "
                "squares.",
            },
            {
                "to": THE_ANSWER,
                "text": "She means to put them over the side at five. Ask her why, "
                "while she will still answer.",
            },
        ],
    },
    THE_MARGINS: {
        "title": "In the margins",
        "text": "Beside the clues, two hands kept a log. 'SW 6, rain later. - I.' "
        "'Jory Pell played the Grieg at last. - M.' 'Fog. Stayed till half five. "
        "- I.' And more often than anything else, in Maren's round print, one word "
        "and an initial: 'Happy. - M.' Nineteen years of Fridays, and which ones.",
    },
    THE_CROSSES: {
        "title": "Maren's crosses",
        "text": "Hanne has her mother's diaries from clearing the house. One "
        "Friday in every month has a small pencil cross on it and nothing else, "
        "for nineteen years: two hundred and twenty-six crosses. Hanne has "
        "brought the last diary with her, because she cannot stop reading a page "
        "with nothing on it.",
        "leads": [
            {
                "to": THE_MARGINS,
                "text": "The crosses say when, and nothing else. Somebody kept "
                "the same Fridays with words.",
            },
            {
                "to": OSKARS_COLUMN,
                "text": "The same Fridays are written down once more on this "
                "boat, in a purser's hand, in a column.",
            },
        ],
    },
    MATES_WATCH: {
        "title": "The mate's watch",
        "text": "Every Friday for nineteen years, at midnight, the captain said "
        "'Mr Aasen, you have the watch,' and went below, and came back at five, "
        "and Per wrote 'Master below' in the log and never asked. He knew by the "
        "second month. He has never said so to her: 'She'd have stopped, if she'd "
        "known anybody knew. So nobody knew.'",
    },
    OSKARS_COLUMN: {
        "title": "The column",
        "text": "Oskar's nineteen narrow ledgers go to the buyer with the ship on "
        "Monday. One column - cabin 6, M. Sollid, a Friday every month since "
        "2007 - he means to tear out and burn in the galley stove before Brekka. "
        "It is the only record of those dates the company ever had, and it is in "
        "his hand.",
    },
    JORYS_AUDITION: {
        "title": "Monday",
        "text": "Jory Pell is going back to Brekka to audition again for the "
        "conservatory he left: Monday, ten o'clock, the Grieg. He has not touched "
        "a piano since Mrs Sollid died. He thinks he will freeze. He has the "
        "music in his coat.",
    },
    THE_ANSWER: {
        "title": "Where the captain is going",
        "text": "Away. Ingrid Halvard has sold Harbour House and Maren's piano, "
        "booked a single south, and is crossing tonight as a passenger in the "
        "cabin where she spent nineteen years of Fridays and never once a whole "
        "night. In the box are the crossword books: the only record of those "
        "nights in either of their hands. At five, the hour she always went back "
        "up, she means to put them over the side mid-channel - kept from the "
        "record - and then Brekka, and the train, and nobody will read them. "
        "Maren's letter asked her to tell Hanne 'on which days'. She told Hanne "
        "'every month'. She never told her which.",
    },
}

# The trail to the answer, for the notebook's count: from the booking to
# the box, and what she means to do with it.
TRAIL = [SIX_TONIGHT, HOUSE_SOLD, TICKET_SOUTH, THE_BOX, THE_ANSWER]

# What the notebook calls the trail on this crossing.
TRAIL_NAME = "the trail to the box"


def title(factId):
    return FACTS[factId]["title"]


def leads(factId):
    """The rumours a fact carries: [(targetFactId, line), ...]."""
    return [(lead["to"], lead["text"]) for lead in FACTS[factId].get("leads", [])]


def text(factId):
    return FACTS[factId]["text"]
