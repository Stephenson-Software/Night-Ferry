# @author Daniel McCoy Stephenson
"""Every key that may be set on State.flags, in one place.

A flag is something that happened on this crossing and that nothing
forgets: a choice someone will hold you to, a door you opened, a thing
that came out. The dict stays free-form in the save file (schemas/save.json
allows any object), but the game only ever writes these names, so a typo is
an import error rather than a silent no-op.

Two-way choices are one flag holding True or False - which way you went -
and absent while you have not chosen. people.REMEMBERED says who holds you
to each.
"""

# Choices people hold you to.
KEPT_INGRIDS_SECRET = "keptIngridsSecret"  # True: "I'll keep it"; False: "Hanne should know"
BROKE_YOUR_WORD = "brokeYourWord"  # promised Ingrid, then told Hanne anyway
TOLD_HANNE = "toldHanne"  # you told Hanne who cabin 6 was for
HANNE_CHOSE_LIGHT = "hanneChoseLight"  # True: the light; False: the churchyard
FENN_TELLS = "fennTells"  # True: he tells Hanne about the referrals; False: let it lie
TOLD_RASKE = "toldRaske"  # True: the truth about the bookings; False: "I don't know"
LET_GUS_IN = "letGusIn"  # True: he slept in cabin 6; False: you said no
JORY_TELLS = "joryTells"  # True: he tells his parents on the quay; False: after Saturday
TOVE_GAVE_LETTER = "toveGaveLetter"  # True: you carried it; False: she took it up herself
INGRID_SAW_THE_SEAL = "ingridSawTheSeal"  # you had read the letter before you handed it over
ASHES_IN_SIX = "ashesInSix"  # you carried Hanne's bag to cabin 6 for an hour

# Things done, and things that came out.
OPENED_SIX = "openedSix"  # the one rule the purser gave you
READ_THE_LETTER = "readTheLetter"
LETTER_DELIVERED = "letterDelivered"
INGRID_ASKED_FOR_HANNE = "ingridAskedForHanne"  # after the letter: bring her up
HANNE_KNOWS = "hanneKnows"  # who cabin 6 was for, by any road
MET_IN_WHEELHOUSE = "metInWheelhouse"  # you brought Hanne up and Ingrid told her
HANNE_PREPARED = "hannePrepared"  # Fenn told her about the referrals first
INGRID_WILL_STOP = "ingridWillStop"  # the engines stop at the Halde light
AT_THE_DOOR = "atTheDoor"  # four o'clock: it came out in the corridor
INGRID_TOLD_YOU = "ingridToldYou"  # she said it to you herself, on the bridge

# --- the last night boat ------------------------------------------------------
# The second crossing keeps its own flags, in a fresh dict: the first
# crossing's are kept, unchanged, in State.past.
OSKAR_GAVE_COLUMN = "oskarGaveColumn"  # True: he tore it out for you; False: burn it
JORY_PLAYS = "joryPlays"  # True: play her piano tonight; False: save it for Monday
GUS_OPENS_THE_LORRY = "gusOpensTheLorry"  # True: you answered for it; False: keep it strapped
PER_TELLS_HER = "perTellsHer"  # True: he tells her he always knew; False: let her think nobody did
INGRID_GIVES_BOOKS = "ingridGivesBooks"  # True: to Hanne, at five; False: "do what you came to do"
HANNE_KNOCKS = "hanneKnocks"  # True: she went down to six herself; False: leave her tonight
OPENED_SIX_AGAIN = "openedSixAgain"  # the captain's one rule tonight
READ_A_BOOK = "readABook"  # you untied the string and read one
TOLD_HANNE_TONIGHT = "toldHanneTonight"  # Hanne learned who cabin 6 was for, from you, in March
LETTER_TO_HANNE = "letterToHanne"  # you gave her Maren's letter, five months late
COLUMN_TO_HANNE = "columnToHanne"  # you gave her Oskar's column
PIANO_PLAYED = "pianoPlayed"  # Jory played Maren's piano on the car deck
INGRID_HEARD_THE_PIANO = "ingridHeardThePiano"  # she was in six, above it
INGRID_TOLD_YOU_TONIGHT = "ingridToldYouTonight"  # where she is going, from her
AT_THE_STERN = "atTheStern"  # five o'clock: Per sent for you
BOOKS_TO_HANNE = "booksToHanne"  # the crossword books went to Hanne
BOOKS_OVERBOARD = "booksOverboard"  # they went over the side
BOOKS_KEPT = "booksKept"  # she took them south with her

ALL = (
    KEPT_INGRIDS_SECRET,
    BROKE_YOUR_WORD,
    TOLD_HANNE,
    HANNE_CHOSE_LIGHT,
    FENN_TELLS,
    TOLD_RASKE,
    LET_GUS_IN,
    JORY_TELLS,
    TOVE_GAVE_LETTER,
    INGRID_SAW_THE_SEAL,
    ASHES_IN_SIX,
    OPENED_SIX,
    READ_THE_LETTER,
    LETTER_DELIVERED,
    INGRID_ASKED_FOR_HANNE,
    HANNE_KNOWS,
    MET_IN_WHEELHOUSE,
    HANNE_PREPARED,
    INGRID_WILL_STOP,
    AT_THE_DOOR,
    INGRID_TOLD_YOU,
    OSKAR_GAVE_COLUMN,
    JORY_PLAYS,
    GUS_OPENS_THE_LORRY,
    PER_TELLS_HER,
    INGRID_GIVES_BOOKS,
    HANNE_KNOCKS,
    OPENED_SIX_AGAIN,
    READ_A_BOOK,
    TOLD_HANNE_TONIGHT,
    LETTER_TO_HANNE,
    COLUMN_TO_HANNE,
    PIANO_PLAYED,
    INGRID_HEARD_THE_PIANO,
    INGRID_TOLD_YOU_TONIGHT,
    AT_THE_STERN,
    BOOKS_TO_HANNE,
    BOOKS_OVERBOARD,
    BOOKS_KEPT,
)
