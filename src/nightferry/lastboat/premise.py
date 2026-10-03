# @author Daniel McCoy Stephenson
"""The last night boat, said plainly - the notebook's "What is happening to
you" page for the second crossing, growing as the player learns, in the same
shape as nightferry.premise."""

from nightferry import endings as firstEndings
from nightferry.lastboat import carried, endings, facts

LAST_BOAT_LABEL = "Sail the last night boat (March)"


def opening(state):
    """The first screen of the second crossing. It depends on October."""
    if carried.firedInOctober(state):
        job = (
            "Oskar Brune told you in October that he would not keep you on, and "
            "he didn't. On Thursday he rang. 'This isn't keeping you on,' he "
            "said. 'It's one night. The last one wants somebody who's met her.'"
        )
    else:
        job = (
            "You have done the Friday boat every week since October. Tonight is "
            "not a Friday, and there will not be another."
        )
    october = {
        firstEndings.OFF_THE_LIGHT: "In October, from this ship, Maren Sollid "
        "went into the water off the Halde light.",
        firstEndings.BESIDE_ARNE: "In October Maren Sollid was buried beside "
        "Arne, and her daughter knew why she had asked not to be.",
        firstEndings.AT_THE_DOOR: "In October it came out in the cabin corridor "
        "at four in the morning, between the fire hose and the linen cupboard.",
        firstEndings.KEPT_CROSSING: "In October you kept the captain's secret, "
        "and Hanne Sollid went ashore not knowing.",
    }.get(carried.octoberEnding(state), "")
    return (
        "March. The MV Kittiwake's last night crossing: Halde to Brekka, away at "
        "eight in the evening, alongside at six. On Monday the buyer's crew takes "
        "her south, and Halde gets a day boat."
        "\n\n" + october + " " + job + "\n\n"
        "Cabin 6 is booked tonight, cash, in the name of I. Halvard. The captain "
        "came up the ramp at seven as a passenger, with a suitcase and a "
        "cardboard box tied with string. The one rule tonight is hers: nobody "
        "disturbs six."
        "\n\n"
        "Everything still takes twenty minutes a turn. Whatever you do, by six "
        "o'clock you will know where the captain is going, and what is in the box."
    )


PARAGRAPHS = [
    (
        (),
        None,
        "WHERE YOU ARE. The last night boat, Halde to Brekka, eight in the evening "
        "to six in the morning. You are the steward again. October is in the "
        "notebook's first pages; this is the rest of it.",
    ),
    (
        (facts.SIX_TONIGHT,),
        None,
        "WHAT IS HAPPENING TO YOU. The captain is crossing as a passenger in cabin "
        "6, booked in her own name, with a suitcase and a box she would not let "
        "anyone carry. Nobody is to disturb six.",
    ),
    (
        (facts.THE_PASSENGER,),
        None,
        "WHO HAS THE SHIP. Per Aasen, the mate, for one night. Ingrid stands at "
        "the back of the wheelhouse until midnight, where nobody will tell her to "
        "go below.",
    ),
    (
        (facts.HOUSE_SOLD,),
        None,
        "WHAT HALDE KNOWS. Harbour House is sold. The captain has told nobody "
        "where she is going.",
    ),
    (
        (facts.PIANO_AGAIN,),
        None,
        "WHAT IS ON THE CAR DECK. Maren's piano, going back to the Brekka saleroom "
        "for the third time, consigned by the captain at any price.",
    ),
    (
        (facts.TICKET_SOUTH,),
        None,
        "WHERE SHE IS GOING. South, on Tuesday's train, single, to a sister she "
        "has not seen in thirty years.",
    ),
    (
        (facts.THE_STOP,),
        None,
        "FIVE O'CLOCK. The engines are to stop for two minutes, mid-channel, on "
        "the captain's order, for 'ballast'.",
    ),
    (
        (facts.THE_BOX,),
        None,
        "WHAT IS IN THE BOX. Nineteen years of crossword books from the drawer of "
        "six, in two hands, every one dated a Friday. The label says BALLAST.",
    ),
    (
        (facts.THE_CROSSES,),
        None,
        "WHAT HANNE IS CARRYING. Her mother's diaries: one pencil cross a month, "
        "two hundred and twenty-six of them, and nothing written beside any.",
    ),
    (
        (facts.THE_MARGINS,),
        None,
        "WHICH DAYS. In the margins of the crossword books, in Maren's print: "
        "'Happy. - M.' The books are the days the letter asked for.",
    ),
    (
        (facts.MATES_WATCH,),
        None,
        "WHO ELSE KNEW. Per, who took the midnight watch for nineteen years and "
        "never said.",
    ),
    (
        (facts.OSKARS_COLUMN,),
        None,
        "THE COLUMN. Oskar means to burn the cabin-6 column of his ledgers before "
        "the buyer has them. It is the only other record of those Fridays.",
    ),
    (
        (facts.JORYS_AUDITION,),
        None,
        "JORY. Maren's last pupil re-auditions on Monday and has not touched a "
        "piano since she died. Hers is on the car deck.",
    ),
    (
        (facts.THE_ANSWER,),
        None,
        "THE ANSWER. The captain is leaving Halde for good, and at five she means "
        "to put the books over the side: the only record of nineteen years, kept "
        "from the record. Maren asked her to tell Hanne which days. She never has.",
    ),
    (
        (),
        endings.ON_WHICH_DAYS,
        "HOW IT ENDED. The books went to Hanne, and Ingrid read her which days. "
        "The last page says what it cost.",
    ),
    (
        (),
        endings.THE_COLUMN,
        "HOW IT ENDED. The books went over the side, and Hanne has Oskar's column. "
        "The last page says what it cost.",
    ),
    (
        (),
        endings.OVER_THE_SIDE,
        "HOW IT ENDED. The books went over the side. The last page says what it "
        "cost.",
    ),
    (
        (),
        endings.KEPT_FROM_THE_RECORD,
        "HOW IT ENDED. The captain took the books south. The last page says what "
        "it cost.",
    ),
]


def _shown(state, needed, ending):
    if ending is not None and state.ending != ending:
        return False
    return all(state.knows(f) for f in needed)


def text(state):
    shown = [p for needed, ending, p in PARAGRAPHS if _shown(state, needed, ending)]
    storyParts = len(PARAGRAPHS) - len(endings.ENDINGS) + 1
    footer = "\n\n(%d of %d parts of the story known. The rest is on the boat.)" % (
        len(shown),
        storyParts,
    )
    return "\n\n".join(shown) + footer
