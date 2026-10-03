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

SAVE_VERSION = 1
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


class State:
    def __init__(self):
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

    # --- knowledge --------------------------------------------------------
    def knows(self, factId):
        return factId in self.facts

    def knowsAny(self, *factIds):
        return any(f in self.facts for f in factIds)

    def learn(self, factId):
        """Record a fact. Returns True if it was new."""
        if factId not in facts.FACTS:
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
        state = cls()
        state.minute = data["minute"]
        state.location = data.get("location", START_LOCATION)
        state.facts = [f for f in data.get("facts", []) if f in facts.FACTS]
        state.factMinutes = {
            f: int(n) for f, n in data.get("factMinutes", {}).items() if f in state.facts
        }
        state.unlocked = list(data.get("unlocked", []))
        state.flags = dict(data.get("flags", {}))
        state.ending = data.get("ending")
        state.rngDraws = data.get("rngDraws", 0)
        return state
