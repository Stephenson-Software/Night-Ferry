# @author Daniel McCoy Stephenson
"""The state of one crossing, and the save file that holds it.

One tier, because nothing resets: the time, where the player is, what they
know (facts, and the time each was learned), what has been done and chosen
(flags), and - once it has happened - which ending the night came to. The
save file is one JSON object, validated against schemas/save.json on every
load and save.

The clock is minutes since the ferry left Brekka at eight in the evening.
Every action costs a turn of twenty minutes; the crossing is six hundred
minutes long. The fixed hours of the night - when the bar shuts, when the
saloon goes dark, when the captain comes down, the light, the quay - are
named here and acted on only in crossing.py. Scenes and people never
compare the clock themselves; they ask the properties below.
"""

import random

from nightferry import facts
from nightferry.lastboat import facts as lastfacts

# 1: Night Ferry 0.1.0 - one crossing. 2: two crossings - the October one and
# the last night boat in March - with "crossing" and "past" (see migrate()).
SAVE_VERSION = 2
SAVE_FILENAME = "save.json"
SCHEMA_PATH = "schemas/save.json"

# The world seed. Constant on purpose: the same crossing says the same
# things to the same player, so a reload is not a reroll.
WORLD_SEED = 2007

# --- the clock --------------------------------------------------------------
DEPARTURE_HOUR = 20
TURN_MINUTES = 20
CROSSING_MINUTES = 10 * 60

# The hours of the night, in minutes after departure.
LAST_ORDERS = 3 * 60  # 11 pm: the bar shuts; Dr Fenn goes to his cabin
SALOON_DARK = 5 * 60  # 1 am: the lights go down; Hanne sleeps sitting up
HANNE_WAKES = 7 * 60  # 3 am
CAPTAIN_COMES_DOWN = 8 * 60  # 4 am: Ingrid goes down to cabin 6
THE_LIGHT = 9 * 60  # 5 am: the Halde light, abeam to port
DOCKING = CROSSING_MINUTES  # 6 am: Halde

# Oskar walks the boat twice a night and leaves the hatch.
OSKAR_ROUNDS = ((2 * 60, 3 * 60), (6 * 60, 7 * 60))
# Raske on the ship's phone to the company, in the foyer.
RASKE_ON_THE_PHONE = (2 * 60, 3 * 60)

START_LOCATION = "saloon"

# --- the last night boat (the second crossing) -------------------------------
# Halde to Brekka in March, on the same clock: away at eight, alongside at six.
# Named here like the first crossing's hours, fired only in lastboat/crossing.py.
LB_LIGHT_ASTERN = 40  # 8:40 pm: the Halde light abeam, then astern
LB_LAST_ORDERS = 3 * 60  # 11 pm: Oskar's last last orders
LB_THE_WATCH = 4 * 60  # midnight: Per takes the watch; Ingrid goes down to six
LB_SALOON_DARK = 5 * 60  # 1 am
LB_BREKKA_LIGHTS = 8 * 60  # 4 am: Brekka on the horizon
LB_THE_STERN = 9 * 60  # 5 am: the hour she always went back up
LB_DOCKING = CROSSING_MINUTES  # 6 am: Brekka

FIRST_CROSSING = 1
LAST_BOAT = 2


def formatClock(minute):
    """Minutes after departure as a clock: 0 -> "8:00 pm", 300 -> "1:00 am"."""
    total = DEPARTURE_HOUR * 60 + minute
    hour = (total // 60) % 24
    suffix = "am" if hour < 12 else "pm"
    twelve = hour % 12 or 12
    return "%d:%02d %s" % (twelve, total % 60, suffix)


def _within(minute, window):
    start, end = window
    return start <= minute < end


def migrate(data):
    """A save as this version of the game reads it, from any earlier one.

    Version 1 (0.1.0) saves are one crossing and have no "crossing" or
    "past": they are the first crossing, with nothing before it. Nothing in a
    version 1 save is changed or dropped. Returns a new dict."""
    data = dict(data)
    if data.get("version", 1) < 2:
        data.setdefault("crossing", FIRST_CROSSING)
        data.setdefault("past", None)
        data["version"] = SAVE_VERSION
    return data


def registryFor(crossing):
    """The facts that can be learned on a crossing."""
    return lastfacts if crossing == LAST_BOAT else facts


class State:
    def __init__(self):
        # Which crossing this is: the first (October) or the last night boat.
        self.crossing = FIRST_CROSSING
        # The first crossing, as it ended, once the last boat has sailed:
        # {"ending", "facts", "flags"}. None on the first crossing.
        self.past = None
        self.minute = 0
        self.location = START_LOCATION
        self.facts = []
        # The minute each fact was learned, by fact id: the journal prints it.
        self.factMinutes = {}
        self.unlocked = []
        self.flags = {}
        self.ending = None
        # How many draws have been taken from the night's fixed sequence.
        self.rngDraws = 0

    # --- which crossing ---------------------------------------------------
    @property
    def lastBoat(self):
        return self.crossing == LAST_BOAT

    @property
    def registry(self):
        """The facts module for this crossing (FACTS, TRAIL, title, ...)."""
        return registryFor(self.crossing)

    def firstCrossing(self):
        """The first crossing's (ending, facts, flags), whichever crossing
        this is - live on the first, remembered on the last."""
        if self.past is not None:
            return (
                self.past.get("ending"),
                list(self.past.get("facts", [])),
                dict(self.past.get("flags", {})),
            )
        return self.ending, list(self.facts), dict(self.flags)

    def pastFlag(self, flag):
        """A flag from the first crossing (None on the first crossing)."""
        if self.past is None:
            return None
        return self.past.get("flags", {}).get(flag)

    def pastKnew(self, factId):
        return self.past is not None and factId in self.past.get("facts", [])

    @property
    def pastEnding(self):
        return None if self.past is None else self.past.get("ending")

    def sailAgain(self):
        """End the first crossing for good and begin the last night boat.

        The first crossing's ending, facts and flags are kept, unchanged, in
        past; the clock, the place, what is known and what has been done
        start again. The notebook stays unlocked: it is the same notebook."""
        if self.lastBoat or not self.over:
            raise ValueError("the last boat sails only after the first crossing ends")
        self.past = {
            "ending": self.ending,
            "facts": list(self.facts),
            "flags": dict(self.flags),
        }
        self.crossing = LAST_BOAT
        self.minute = 0
        self.location = START_LOCATION
        self.facts = []
        self.factMinutes = {}
        self.flags = {}
        self.ending = None
        self.rngDraws = 0

    # --- knowledge --------------------------------------------------------
    def knows(self, factId):
        return factId in self.facts

    def knowsAny(self, *factIds):
        return any(f in self.facts for f in factIds)

    def learn(self, factId):
        """Record a fact. Returns True if it was new."""
        if factId not in self.registry.FACTS:
            raise ValueError("unknown fact %r" % factId)
        if factId in self.facts:
            return False
        self.facts.append(factId)
        self.factMinutes[factId] = self.minute
        return True

    def learnedAt(self, factId):
        """The clock time a fact was learned, or None if not known."""
        minute = self.factMinutes.get(factId)
        return None if minute is None else formatClock(minute)

    # --- the clock, as the scenes may ask it -------------------------------
    @property
    def clock(self):
        return formatClock(min(self.minute, CROSSING_MINUTES))

    @property
    def hoursToDock(self):
        left = max(0, CROSSING_MINUTES - self.minute)
        return (left + 59) // 60

    @property
    def atDeparture(self):
        return self.minute == 0

    @property
    def barOpen(self):
        return self.minute < LAST_ORDERS

    @property
    def fennInHisCabin(self):
        return self.minute >= LAST_ORDERS

    @property
    def hanneAsleep(self):
        return SALOON_DARK <= self.minute < HANNE_WAKES

    @property
    def hanneAsleepForAnHour(self):
        """Long enough asleep that an hour can be borrowed and given back."""
        return SALOON_DARK <= self.minute and self.minute + 60 <= HANNE_WAKES

    @property
    def oskarOnRounds(self):
        return any(_within(self.minute, w) for w in OSKAR_ROUNDS)

    @property
    def raskeOnThePhone(self):
        return _within(self.minute, RASKE_ON_THE_PHONE)

    @property
    def lightPassed(self):
        return self.minute >= THE_LIGHT

    @property
    def lightInSight(self):
        """The Halde light is on the horizon from three; nobody misses it."""
        return self.minute >= HANNE_WAKES

    # --- the last boat's night, as its scenes may ask it ----------------------
    @property
    def ingridOnTheBridge(self):
        """Until midnight the captain stands at the back of the wheelhouse."""
        return self.minute < LB_THE_WATCH

    @property
    def ingridInSix(self):
        """From midnight until five she is in cabin 6."""
        return LB_THE_WATCH <= self.minute < LB_THE_STERN

    @property
    def ingridAtTheStern(self):
        """From five she is on deck, at the stern rail, until Brekka."""
        return self.minute >= LB_THE_STERN

    @property
    def quietHours(self):
        """After midnight the saloon is sleeping and a piano can be played."""
        return self.minute >= LB_THE_WATCH

    @property
    def haldeLightAstern(self):
        return self.minute < LB_LAST_ORDERS

    @property
    def brekkaInSight(self):
        return self.minute >= LB_BREKKA_LIGHTS

    @property
    def over(self):
        return self.ending is not None

    def draw(self, choices):
        """One draw from the night's fixed sequence.

        Each draw is a pure function of the world seed and its own index -
        a fresh generator seeded per draw - never the next output of one
        long-lived generator, whose replay is not position-faithful
        (random.choice rejection-samples)."""
        rng = random.Random(WORLD_SEED * 1000003 + self.rngDraws)
        self.rngDraws += 1
        return rng.choice(choices)

    # --- persistence ------------------------------------------------------
    def toDict(self):
        return {
            "version": SAVE_VERSION,
            "crossing": self.crossing,
            "past": None
            if self.past is None
            else {
                "ending": self.past.get("ending"),
                "facts": list(self.past.get("facts", [])),
                "flags": dict(self.past.get("flags", {})),
            },
            "minute": self.minute,
            "location": self.location,
            "facts": list(self.facts),
            "factMinutes": dict(self.factMinutes),
            "unlocked": list(self.unlocked),
            "flags": dict(self.flags),
            "ending": self.ending,
            "rngDraws": self.rngDraws,
        }

    @classmethod
    def fromDict(cls, data):
        data = migrate(data)
        state = cls()
        state.crossing = data.get("crossing") or FIRST_CROSSING
        past = data.get("past")
        if isinstance(past, dict):
            state.past = {
                "ending": past.get("ending"),
                "facts": [f for f in past.get("facts", []) if f in facts.FACTS],
                "flags": dict(past.get("flags", {})),
            }
        state.minute = data["minute"]
        state.location = data.get("location", START_LOCATION)
        registry = registryFor(state.crossing).FACTS
        state.facts = [f for f in data.get("facts", []) if f in registry]
        state.factMinutes = {
            f: int(n) for f, n in data.get("factMinutes", {}).items() if f in state.facts
        }
        state.unlocked = list(data.get("unlocked", []))
        state.flags = dict(data.get("flags", {}))
        state.ending = data.get("ending")
        state.rngDraws = data.get("rngDraws", 0)
        return state
