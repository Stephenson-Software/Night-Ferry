# @author Daniel McCoy Stephenson
"""The story, said plainly.

Everything here is also in the facts, people's mouths and the endings - but
scattered, in character, in the order the player happens to find it. This
is the same story told straight, in the notebook, growing as the player
learns: each paragraph is shown once its facts are known, so it never says
more than the player has earned, and never less than they have.

It exists because a playtester of an earlier game finished an ending and
said: I got no answers. This page is built in from the first minute.
"""

from nightferry import endings, facts

OPENING = (
    "MV Kittiwake, the Halde crossing: ten hours of open water from Brekka to "
    "the island of Halde, away at eight in the evening, alongside at six in "
    "the morning."
    "\n\n"
    "You are the night steward. It is your first crossing. You were taken on "
    "this afternoon on Brekka quay because the regular steward broke her "
    "wrist, and you said yes because it was work, and because a night boat is "
    "a place where nobody asks where you have been. Oskar Brune, the purser, "
    "gave you a white jacket, a master key to every cabin, and one rule: "
    "cabin 6 is not to be opened."
    "\n\n"
    "Cabin 6 was paid for in cash. Nobody has come aboard to claim it."
    "\n\n"
    "Everything you do takes time - twenty minutes a turn, ten hours to the "
    "quay. Talk to people. Listen at doors. Open what you shouldn't. Whatever "
    "you do, by six o'clock you will know who the empty cabin was for."
)

# (needed facts, ending or None, paragraph). Shown in order; a paragraph
# appears once every fact it needs is known and, if it names an ending,
# once the night has come to that ending. The first needs nothing.
PARAGRAPHS = [
    (
        (),
        None,
        "WHERE YOU ARE. The night ferry to Halde, eight in the evening to six in "
        "the morning. You are the new night steward: coffee, blankets, a master "
        "key, and one rule - cabin 6 stays shut. Everything in this notebook "
        "is something you found out; under each thing is where it points that "
        "you have not been yet.",
    ),
    (
        (facts.CABIN_SIX,),
        None,
        "WHAT IS HAPPENING TO YOU. Cabin 6 was booked three weeks ago, cash, "
        "one berth, in the name of M. Sollid, and is made up and empty. The "
        "purser will not say why, and has told you twice not to open it. "
        "Somebody paid for a bed for someone who is not here.",
    ),
    (
        (facts.THE_ASHES,),
        None,
        "WHO IS ON THE MANIFEST. Hanne Sollid, the woman with two tickets, is "
        "taking her mother home: Maren Sollid's ashes are in the canvas bag at "
        "her feet, and the funeral is tomorrow on Halde. The second ticket is "
        "for her mother, who always paid her own way.",
    ),
    (
        (facts.THE_LEDGER,),
        None,
        "NINETEEN YEARS. Cabin 6 has been booked to M. Sollid on the Friday "
        "crossing home every month since 2007, in cash, in the purser's own "
        "hand, never in the computer. It stopped in June. It started again "
        "tonight.",
    ),
    (
        (facts.THE_TEACHER,),
        None,
        "WHO M. SOLLID WAS. Maren Sollid taught at the Halde school for "
        "thirty-five years. After her husband Arne died in 2006 she crossed to "
        "Brekka once a month 'for the specialist', and always came home on the "
        "Friday boat. This boat.",
    ),
    (
        (facts.THE_NOTE,),
        None,
        "WHAT MAREN ASKED. Not to be buried beside Arne, though the stone is "
        "cut: 'the water off the Halde light, from the boat, at first light.' "
        "The light is at five. Only the captain can stop the ship there.",
    ),
    (
        (facts.THE_APPOINTMENTS,),
        None,
        "THE SPECIALIST. There wasn't one. Dr Fenn wrote her a false referral "
        "every month for nineteen years because she asked, and never asked "
        "where she went. She came home happier than she left.",
    ),
    (
        (facts.THE_PIANO, facts.HARBOUR_HOUSE),
        None,
        "WHERE HER PIANO IS GOING. Maren's piano was sold in the house clearance "
        "and bought for cash, no name given, for delivery to Harbour House: the "
        "captain's house.",
    ),
    (
        (facts.THE_LETTER,),
        None,
        "THE LETTER. The nurse who sat with Maren as she died is carrying a "
        "sealed letter from her, 'For I.H. - on the Friday boat.' She does not "
        "know who I.H. is.",
    ),
    (
        (facts.THE_DOOR, facts.INSIDE_SIX),
        None,
        "WHAT THE CABIN SHOWS. The captain stood at the door of six before the "
        "boat sailed and did not go in. Inside: two cups, a schoolteacher's "
        "cardigan, nineteen years of crosswords filled in by two hands.",
    ),
    (
        (facts.THE_CAPTAIN,),
        None,
        "THE ANSWER. Cabin 6 was for Maren Sollid. She came home in it every "
        "month for nineteen years, and the captain, Ingrid Halvard, went down to "
        "her when the mate took the watch. The specialist was the crossing. "
        "Ingrid booked it tonight so Maren could come home in it once more; "
        "Maren is in a bag at her daughter's feet, and her daughter knows none "
        "of it unless somebody tells her.",
    ),
    (
        (facts.WHAT_MAREN_WROTE,),
        None,
        "IN HER OWN WORDS. Maren's letter asked Ingrid to tell Hanne - that she "
        "was happy, and on which days - and then the light, if Hanne would let "
        "her. 'It was never him I crossed for.'",
    ),
    (
        (facts.RASKES_AUDIT,),
        None,
        "WHAT IT COSTS OSKAR. The company's man has read the same columns and "
        "thinks the purser was skimming. His report goes in at the quay. Only "
        "the truth clears Oskar, and the truth has the captain's name in it.",
    ),
    (
        (facts.LAST_WINTER,),
        None,
        "THE LAST WINTER. The night crossing ends in March and the Kittiwake "
        "is being sold. The captain has known since June. This was the last "
        "Friday boat she would have that Maren knew.",
    ),
    (
        (facts.JORYS_TERM,),
        None,
        "JORY. Maren's last piano pupil has left the conservatory she got him "
        "into, and has not told his parents, who are meeting the boat.",
    ),
    (
        (),
        endings.OFF_THE_LIGHT,
        "HOW IT ENDED. Off the light, at five: Hanne and Ingrid put Maren into "
        "the water together, as she asked. The last page says what it cost.",
    ),
    (
        (),
        endings.BESIDE_ARNE,
        "HOW IT ENDED. Hanne knows, and the light went by; Maren will be buried "
        "beside Arne. The last page says what it cost.",
    ),
    (
        (),
        endings.AT_THE_DOOR,
        "HOW IT ENDED. It came out at four in the corridor, at the door of six, "
        "because nobody else had said it. The last page says what it cost.",
    ),
    (
        (),
        endings.KEPT_CROSSING,
        "HOW IT ENDED. You kept the captain's secret, and Hanne went ashore not "
        "knowing. The last page says what it cost.",
    ),
]


def _shown(state, needed, ending):
    if ending is not None and state.ending != ending:
        return False
    return all(state.knows(f) for f in needed)


def text(state):
    """The story so far, in plain words, for the notebook."""
    shown = [p for needed, ending, p in PARAGRAPHS if _shown(state, needed, ending)]
    storyParts = len(PARAGRAPHS) - len(endings.ENDINGS) + 1
    footer = "\n\n(%d of %d parts of the story known. The rest is on the boat.)" % (
        len(shown),
        storyParts,
    )
    return "\n\n".join(shown) + footer
