"""Scripted routes through the crossing, shared by the playthrough tests.

Every label is a menu row or a dialogue question; the ScriptedUI fails
loudly if one is missing or unavailable. Moving between places is free;
each conversation in which something is asked, and each action, is one
turn of twenty minutes. Times in the comments are after the step."""

NEW = ["Create New Save"]
PANTRY = "Sit in the steward's pantry"  # an hour


def waitInPantry(hours):
    return [PANTRY] * hours


# The canonical solve: all sixteen facts, every person's remembered choice,
# and Maren put into the water off the Halde light at five.
CANONICAL = NEW + [
    "Ask the purser about cabin 6",
    "What's the story with cabin 6",  # CABIN_SIX
    "[Back]",  # 8:20
    "Sit with the woman holding two tickets",
    "Who's the second ticket for",  # THE_ASHES
    "Something about tomorrow is wrong",  # THE_NOTE
    "[Back]",  # 8:40
    "Talk to the old man with the crossword",
    "Did you know Maren Sollid",  # THE_TEACHER
    "She crossed every month",  # THE_APPOINTMENTS
    "Hanne should hear that from you",  # FENN_TELLS
    "[Back]",  # 9:00
    "Talk to the man with the laptop",
    "You were asking Oskar about cabin 6",  # RASKES_AUDIT
    "Show me the bookings",  # THE_LEDGER
    "what sale",  # LAST_WINTER
    "[Back]",  # 9:20
    "Walk the lower deck",
    "Talk to the lorry driver",
    "What are you hauling",  # THE_PIANO
    "No. That cabin's spoken for",  # LET_GUS_IN = False
    "[Back]",  # 9:40
    "Go out on the open deck",
    "Talk to the boy at the rail",
    "Going home",  # JORYS_TERM
    "Seen anybody near cabin 6",  # THE_DOOR
    "Whose is Harbour House",  # HARBOUR_HOUSE
    "Tell them on the quay",  # JORY_TELLS
    "[Back]",  # 10:00
    "Go along the cabin corridor",
    "Knock at cabin 4",
    "What takes you to Halde",  # THE_LETTER
    "Give it to me",  # TOVE_GAVE_LETTER = True
    "[Back]",  # 10:20
    "Open cabin 6 with your master key",  # INSIDE_SIX, OPENED_SIX; 10:40
    "Go up to the wheelhouse",
    "Talk to the captain",
    "Who was cabin 6 for, captain",  # THE_CAPTAIN
    "Hanne should know",  # KEPT_INGRIDS_SECRET = False
    "This is from Maren",  # WHAT_MAREN_WROTE; she asks for Hanne
    "being sold",
    "[Back]",  # 11:00, the bar shuts
    "Go back to the saloon",
    "Take Hanne up to the wheelhouse",
    "Do what she asked. The light.",  # HANNE_CHOSE_LIGHT, INGRID_WILL_STOP; 11:20
    "Talk to Raske",
    "The bookings were the captain's",  # TOLD_RASKE = True
    "[Back]",  # 11:40
    "Go along the cabin corridor",
] + waitInPantry(6) + [  # 5:00: the light
    "Quit",
]

# The do-nothing crossing: a player who asks nobody anything still hears
# who cabin 6 was for, at four, in the corridor, and docks at six.
DO_NOTHING = NEW + ["Go along the cabin corridor"] + waitInPantry(8) + [
    # 4:00 - the door; the corridor again
] + waitInPantry(2) + ["Quit"]

# Promise the captain, and give Maren her hour in six while Hanne sleeps.
KEPT = NEW + [
    "Ask the purser about cabin 6",
    "What's the story with cabin 6",
    "[Back]",  # 8:20
    "Go out on the open deck",
    "Talk to the boy at the rail",
    "Seen anybody near cabin 6",  # THE_DOOR
    "[Back]",  # 8:40
    "Go up to the wheelhouse",
    "Talk to the captain",
    "Who was cabin 6 for, captain",
    "I'll keep it",
    "[Back]",  # 9:00
    "Go along the cabin corridor",
] + waitInPantry(4) + [  # 1:00, the saloon dark
    "Go back to the saloon",
    "Carry Hanne's bag to cabin 6",  # 2:00
    "Go along the cabin corridor",
] + waitInPantry(4) + ["Quit"]  # 6:00


# --- the last night boat ------------------------------------------------------
SAIL = "Sail the last night boat"


def lastBoatAfter(firstRoute):
    """A first-crossing route whose last step (Quit, at the epilogue) is
    replaced by sailing the last night boat."""
    assert firstRoute[-1] == "Quit"
    return list(firstRoute[:-1]) + [SAIL]


# The last boat's canonical solve: all thirteen facts, every person's
# remembered choice, Jory playing under the captain's floor, and Hanne
# knocking on six herself. Ends "on which days" at six.
LAST_CANONICAL = (
    [
        "Ask the purser about cabin 6",
        "What's the story with cabin 6 tonight",  # SIX_TONIGHT
        "What happens to your ledgers",  # OSKARS_COLUMN
        "Give me the column instead",  # OSKAR_GAVE_COLUMN = True
        "[Back]",  # 8:20
        "Sit with Hanne Sollid",
        "Crossing back to Brekka",  # THE_CROSSES
        "[Back]",  # 8:40, the light astern
        "Go out on the open deck",
        "Talk to the young man at the rail",
        "Going back to Brekka",  # JORYS_AUDITION
        "Anything new on Halde",  # HOUSE_SOLD
        "[Back]",  # 9:00
        "Walk the lower deck",
        "Talk to the lorry driver",
        "What are you hauling this time",  # PIANO_AGAIN
        "[Back]",  # 9:20
        "Go out on the open deck",
        "Talk to Jory",
        "Play it tonight",  # JORY_PLAYS = True
        "[Back]",  # 9:40
        "Walk the lower deck",
        "Talk to Gus",
        "Open the back for Jory",  # GUS_OPENS_THE_LORRY = True
        "[Back]",  # 10:00
        "Go back to the saloon",
        "Talk to Oskar",
        "Where's the captain going",  # TICKET_SOUTH
        "[Back]",  # 10:20
        "Go up to the wheelhouse",
        "Talk to Per Aasen",
        "Why isn't the captain in command",  # THE_PASSENGER
        "You took the watch at midnight",  # MATES_WATCH
        "What's in the night order book",  # THE_STOP
        "Tell her you knew",  # PER_TELLS_HER = True
        "[Back]",  # 10:40
        "Go along the cabin corridor",
        "Open cabin 6 with your master key",  # THE_BOX, OPENED_SIX_AGAIN; 11:00
        "Untie the string",  # THE_MARGINS; 11:20
        "Go up to the wheelhouse",
        "Talk to the captain",
        "Where are you going, Ingrid",  # THE_ANSWER
        "[Back]",  # 11:40
        "Go along the cabin corridor",
        PANTRY,  # 12:40; midnight - Per has the watch, she goes down to six
        "Walk the lower deck",
        "Fetch Jory down to the piano",  # 1:00; she hears it in six
        "Go back to the saloon",
        "Sit with Hanne Sollid",
        "Go and knock",  # HANNE_KNOCKS -> the books to Hanne
        "This is from the purser's ledgers",  # COLUMN_TO_HANNE
        "[Back]",  # 1:20
        "Go along the cabin corridor",
        "Knock at cabin 6",
        "Per always knew",
        "Jory played her piano",
        "[Back]",  # 1:40
    ]
    + waitInPantry(5)
    + [  # 5:00 the stern, 6:00 Brekka
        "Quit",
    ]
)

# The do-nothing last boat: ask nobody anything, and at five Per sends for
# you, and the captain tells you all of it at the stern rail.
LAST_DO_NOTHING_UNTIL_FIVE = ["Go along the cabin corridor"] + waitInPantry(9)
