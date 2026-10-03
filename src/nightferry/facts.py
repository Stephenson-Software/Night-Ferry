# @author Daniel McCoy Stephenson
"""Everything the player can come to know.

A fact is the unit of progress on the crossing: what opens a door is what
you know, never what time it is. Each fact has a title for the notebook and
the line the notebook shows under it. Order here is the order the notebook
lists them in, roughly the order a player is likely to learn them.

Facts point at each other. A fact's "leads" are the things it hints can be
learned next - each a target fact id and the line the notebook shows while
that target is still unknown. The line never names the target; it says
where to look, the way a rumour does.

There are sixteen, and all sixteen can be learned on one crossing. The
endings are not facts: they are what the night came to (state.ending).
"""

CABIN_SIX = "cabin_six"
THE_LEDGER = "the_ledger"
THE_ASHES = "the_ashes"
THE_TEACHER = "the_teacher"
THE_NOTE = "the_note"
THE_APPOINTMENTS = "the_appointments"
THE_LETTER = "the_letter"
THE_PIANO = "the_piano"
HARBOUR_HOUSE = "harbour_house"
THE_DOOR = "the_door"
INSIDE_SIX = "inside_six"
RASKES_AUDIT = "raskes_audit"
LAST_WINTER = "last_winter"
JORYS_TERM = "jorys_term"
THE_CAPTAIN = "the_captain"
WHAT_MAREN_WROTE = "what_maren_wrote"

FACTS = {
    CABIN_SIX: {
        "title": "Cabin 6",
        "text": "Booked three weeks ago at the Brekka office, one berth, paid in "
        "cash, in the name of M. Sollid. Nobody has come aboard to claim it. "
        "Oskar keeps it made up and gave you one rule with the master key: "
        "cabin 6 is not to be opened.",
        "leads": [
            {
                "to": THE_ASHES,
                "text": "There is another Sollid on tonight's manifest: two deck "
                "tickets, sitting in the saloon.",
            },
            {
                "to": THE_LEDGER,
                "text": "When Oskar said the name he glanced at the old ledgers "
                "under his hatch, and then he put his elbow on them.",
            },
            {
                "to": THE_DOOR,
                "text": "Somebody on deck has been watching who comes and goes "
                "along the cabin corridor since before we sailed.",
            },
            {
                "to": INSIDE_SIX,
                "text": "You have a master key in your pocket, and a rule about "
                "the one door it is not for.",
            },
        ],
    },
    THE_LEDGER: {
        "title": "Nineteen years of Fridays",
        "text": "The old ledgers: cabin 6, the Friday crossing home to Halde, "
        "M. Sollid - once a month since March 2007, always cash, always in "
        "Oskar's hand and never in the company's computer. The entries stop "
        "in June. Tonight's is the first since.",
        "leads": [
            {
                "to": THE_TEACHER,
                "text": "Who was M. Sollid? Most of this boat is from Halde, and "
                "on Halde everyone knows everyone's mother.",
            },
            {
                "to": RASKES_AUDIT,
                "text": "Somebody else has been reading these columns lately, "
                "with a pencil, and not kindly.",
            },
        ],
    },
    THE_ASHES: {
        "title": "What Hanne is carrying",
        "text": "Hanne Sollid is taking her mother home. Maren Sollid died in "
        "August in a hospice in Brekka; her ashes are in the canvas bag at "
        "Hanne's feet. Hanne bought two tickets because her mother always paid "
        "her own way. The funeral is tomorrow, on Halde.",
        "leads": [
            {
                "to": THE_NOTE,
                "text": "Hanne keeps touching a folded paper in her coat pocket. "
                "Something about tomorrow is wrong, and she is ashamed of it.",
            },
            {
                "to": THE_APPOINTMENTS,
                "text": "'She crossed every month to see a specialist.' The "
                "island's old doctor is in the saloon, doing a crossword.",
            },
            {
                "to": THE_LETTER,
                "text": "Somebody sat with Maren at the end, in Brekka. It was "
                "not Hanne, and it is on her face.",
            },
        ],
    },
    THE_TEACHER: {
        "title": "Mrs Sollid",
        "text": "Maren Sollid taught at the Halde school for thirty-five years "
        "and gave half the island piano lessons. Widowed in 2006, when Arne's "
        "heart stopped on the slipway. From the spring after, she took the "
        "boat to Brekka once a month 'for the specialist', and always came "
        "home on the Friday night crossing.",
        "leads": [
            {
                "to": THE_PIANO,
                "text": "Her house was cleared in September. Somebody bought her "
                "piano, and it is coming back to the island tonight, on the car "
                "deck.",
            },
            {
                "to": JORYS_TERM,
                "text": "Her last piano pupil is on this boat, and he is not going "
                "home for the reason he says.",
            },
            {
                "to": THE_APPOINTMENTS,
                "text": "Nineteen years of a specialist, and she never looked ill "
                "a day of it. The man who sent her would know what for.",
            },
        ],
    },
    THE_NOTE: {
        "title": "Not beside Arne",
        "text": "Maren left a note with her will: 'Not beside Arne. The water "
        "off the Halde light, from the boat, at first light.' The island "
        "expects the churchyard, tomorrow, next to her husband; the stone is "
        "cut. Hanne does not understand the note and is ashamed of how much "
        "she wants to ignore it.",
        "leads": [
            {
                "to": THE_CAPTAIN,
                "text": "'From the boat, off the light.' Only one person on board "
                "can stop this ship at the Halde light, and Maren knew it.",
            },
        ],
    },
    THE_APPOINTMENTS: {
        "title": "The specialist in Brekka",
        "text": "Dr Fenn wrote Maren a referral to a Brekka specialist every "
        "month for nineteen years. There was nothing wrong with her - not "
        "until last year, when there was. She asked for the letters; he wrote "
        "them; he never asked where she went. 'She came home happier than she "
        "left. That is all the medicine I know.'",
        "leads": [
            {
                "to": THE_DOOR,
                "text": "Whatever she crossed for, she crossed for it on this "
                "boat, in the same cabin. Somebody who watches this boat will "
                "have seen something.",
            },
        ],
    },
    THE_LETTER: {
        "title": "A letter for I.H.",
        "text": "Tove Ness, the nurse who sat with Maren in the hospice, is "
        "carrying a sealed letter Maren gave her the week she died: 'For I.H. "
        "- on the Friday boat.' Tove does not know who I.H. is. She has been "
        "afraid to ask.",
        "leads": [
            {
                "to": HARBOUR_HOUSE,
                "text": "I.H. Two initials. Anybody from Halde would know whose "
                "they are.",
            },
            {
                "to": WHAT_MAREN_WROTE,
                "text": "The envelope is sealed, and what is in it is not yours.",
            },
        ],
    },
    THE_PIANO: {
        "title": "Maren's piano",
        "text": "In the back of Gus Tamm's lorry: an upright piano with HALDE "
        "SCHOOL stencilled on the back, from Maren Sollid's house clearance. "
        "Bought at the Brekka saleroom for cash by a woman who would not give "
        "a name. The docket says: deliver to Harbour House, Halde.",
        "leads": [
            {
                "to": HARBOUR_HOUSE,
                "text": "Harbour House. Anybody from Halde knows whose that is.",
            },
        ],
    },
    HARBOUR_HOUSE: {
        "title": "Ingrid Halvard's house",
        "text": "Harbour House is the captain's: Ingrid Halvard, master of the "
        "Kittiwake for twenty-two years. She lives alone. I.H.",
        "leads": [
            {
                "to": THE_CAPTAIN,
                "text": "The captain bought a dead schoolteacher's piano with "
                "cash and gave no name. She has a reason, and she is on the "
                "bridge.",
            },
        ],
    },
    THE_DOOR: {
        "title": "The captain at the door",
        "text": "Jory saw it before the boat sailed: the captain came down the "
        "cabin corridor alone, stopped at cabin 6, put her hand flat on the "
        "door the way you would feel a stove for heat, and went back up "
        "without opening it.",
        "leads": [
            {
                "to": THE_CAPTAIN,
                "text": "The captain stood at that door and did not go in. Ask "
                "her why.",
            },
        ],
    },
    INSIDE_SIX: {
        "title": "Inside cabin 6",
        "text": "Made up for one, with care. A sprig of sea-pink on the pillow. "
        "A cardigan on the hook with a Halde School badge. Two cups on the "
        "shelf, not one. In the drawer, nineteen years of crossword books, "
        "every one filled in by two hands: a schoolteacher's, and one that "
        "writes like a ship's log.",
        "leads": [
            {
                "to": THE_CAPTAIN,
                "text": "The second hand in the crossword books keeps a log for a "
                "living. There is one on the bridge.",
            },
        ],
    },
    RASKES_AUDIT: {
        "title": "Raske's audit",
        "text": "Leopold Raske is the company's man, riding tonight to look at "
        "the books. He has found nineteen years of cash bookings kept off the "
        "system in the purser's hand, and to him they look like a purser "
        "skimming. His report goes to the board when the boat docks; Oskar "
        "will be suspended. Raske said it all 'has to be clean before the sale "
        "goes through'.",
        "leads": [
            {
                "to": LAST_WINTER,
                "text": "'Before the sale goes through.' A sale of what?",
            },
            {
                "to": THE_LEDGER,
                "text": "The columns Raske is reading are under the purser's "
                "hatch. Oskar leaves it when he walks the boat.",
            },
        ],
    },
    LAST_WINTER: {
        "title": "The last winter",
        "text": "The night crossing ends in March. The Kittiwake is being sold "
        "and the Halde run goes to a day boat. Raske grew up on Halde - Maren "
        "Sollid taught him long division - and argued against it, and lost. "
        "The captain was told in June.",
    },
    JORYS_TERM: {
        "title": "Jory's term",
        "text": "Jory Pell, nineteen, left the conservatory in Brekka in "
        "September and has not told his parents, who are meeting the boat. "
        "Mrs Sollid got him the place. He has not touched a piano since she "
        "died, and he is going home for her funeral.",
    },
    THE_CAPTAIN: {
        "title": "Who cabin 6 was for",
        "text": "Cabin 6 was for Maren Sollid. For nineteen years she came home "
        "from Brekka on the Friday boat, in cabin 6, and when the mate took "
        "the watch at midnight Ingrid Halvard came down to her. The specialist "
        "was the crossing. Three weeks ago Ingrid paid cash for the cabin in "
        "Maren's name, so she could come home in it once more - in a canvas "
        "bag at her daughter's feet, two decks below, where Ingrid cannot go.",
    },
    WHAT_MAREN_WROTE: {
        "title": "What Maren wrote",
        "text": "'I. - If H. is on the boat, tell her. I never found the way to, "
        "and you were always braver on the water than I was. Tell her I was "
        "happy, and on which days. Then the light, if she will let you. Not "
        "beside Arne: he was a good man and he would understand, and it was "
        "never him I crossed for. - M.'",
    },
}

# The trail to the answer, in the order a careful player learns it: from
# the booking to the bridge. The notebook marks these so a player who has
# learned a few knows how far there is to go.
TRAIL = [CABIN_SIX, THE_LEDGER, THE_TEACHER, THE_PIANO, HARBOUR_HOUSE, THE_CAPTAIN]


def title(factId):
    return FACTS[factId]["title"]


def leads(factId):
    """The rumours a fact carries: [(targetFactId, line), ...]."""
    return [(lead["to"], lead["text"]) for lead in FACTS[factId].get("leads", [])]


def text(factId):
    return FACTS[factId]["text"]
