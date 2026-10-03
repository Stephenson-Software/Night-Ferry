# @author Daniel McCoy Stephenson
"""The game: a save slot, the state, the scenes, and the loop that runs
them. Front-end agnostic - see tak.ui."""

import json
import os
import shutil
from datetime import datetime

from jsonschema.exceptions import ValidationError

from tak import Prompt
from tak.saves import (
    SaveFileManager,
    chooseSlot,
    syncBrowserSaves,
    validateAgainstSchema,
)
from tak.ui import UIType, createUserInterface

from nightferry import endings, premise, progression, scenes
from nightferry.config import Config
from nightferry.header import buildHeader
from nightferry.state import SAVE_FILENAME, SCHEMA_PATH, State, formatClock

TITLE = "Night Ferry"
TAGLINE = "one crossing, six passengers, and a cabin booked but empty"
ENV_PREFIX = "NIGHTFERRY"
OPENING_PROMPT = "The ramp is up and the engines are turning. What would you like to do?"

# Which front-end the game runs. The rest of the game is front-end agnostic.
INTERFACE_TYPE = UIType.CONSOLE


def describeSlot(metadata):
    """The save menu's summary of a slot: "1:20 am, 6 known"."""
    if metadata.get("ending"):
        return "docked - %s, %d known" % (metadata["ending"], metadata.get("known", 0))
    return "%s, %d known" % (metadata.get("time", "?"), metadata.get("known", 0))


def slotMetadata(slotPath, data):
    """The save menu's fields for a slot. The manager only calls this once
    the file has parsed as JSON; a file that parses but is not a save (a
    minute of "ten") is described as damaged rather than raising here, and
    load() will refuse it properly against the schema."""
    try:
        state = State.fromDict(data)
        if not isinstance(state.minute, int) or isinstance(state.minute, bool):
            raise TypeError("minute is not a number")
        if not isinstance(state.facts, list):
            raise TypeError("facts is not a list")
        return {
            "time": formatClock(max(0, state.minute)),
            "known": len(state.facts),
            "ending": endings.name(state) if state.over else None,
        }
    except (KeyError, TypeError, ValueError, AttributeError):
        return {"time": "damaged", "known": 0, "ending": None}


# @author Daniel McCoy Stephenson
class NightFerry:
    def __init__(self, interfaceType=INTERFACE_TYPE):
        self.running = True
        self.spoke = False
        # Where closing the notebook goes back to.
        self.returnTo = "saloon"
        self.config = Config()
        self.saveFileManager = SaveFileManager(
            self.config.dataDirectory,
            primaryFile=SAVE_FILENAME,
            readMetadata=slotMetadata,
        )
        self.failedLoad = None

        self.state = State()
        self.prompt = Prompt(OPENING_PROMPT)
        self.ui = createUserInterface(
            interfaceType,
            self.prompt,
            lambda: buildHeader(self),
            title=TITLE,
            tagline=TAGLINE,
            envPrefix=ENV_PREFIX,
        )

        chosen = chooseSlot(
            self.ui, self.saveFileManager, TITLE + " - Save Files", describeSlot
        )
        if chosen is None:
            # Ending the run rather than the process, so the front-end still
            # gets its cleanup() - play() does nothing but that.
            self.running = False
            return

        kind, _ = chosen
        savePath = self.saveFileManager.get_save_path(SAVE_FILENAME)
        if kind == "load" and os.path.exists(savePath):
            self.load(savePath)
            if self.failedLoad:
                self._preserveDamagedSave(savePath)
            elif self.state.minute > 0 or self.state.facts:
                self.prompt.text = "%s. What would you like to do?" % self.state.clock
        # A loaded save may predate an unlock, or have earned one since.
        progression.catchUp(self.state)
        self.scenes = scenes.build(self)
        # A brand-new crossing opens on who you are and why, once.
        self.showOpening = kind == "new" or (
            self.state.minute == 0 and not self.state.facts
        )

    # --- the scenes' hooks ------------------------------------------------
    def learn(self, factId):
        """Promote something to knowledge. Returns True if it was new."""
        return self.state.learn(factId)

    # --- play -------------------------------------------------------------
    def play(self):
        try:
            if self.running:
                self._runGameLoop()
        finally:
            self.ui.cleanup()

    def _runGameLoop(self):
        if self.showOpening:
            self.ui.showDialogue(premise.OPENING)
            self.showOpening = False
        while self.running:
            unlock = progression.getNextUnlock(self.state)
            if unlock is not None:
                self.ui.showDialogue("[%s]" % unlock["announcement"])
            current = self.state.location
            if current not in self.scenes:
                current = self.state.location = (
                    "epilogue" if self.state.over else "saloon"
                )
            nextScene = self.scenes[current].run()
            self.save()
            if nextScene == scenes.QUIT:
                self.running = False

    # --- persistence ------------------------------------------------------
    def save(self):
        data = self.state.toDict()
        validateAgainstSchema(data, SCHEMA_PATH)
        path = self.saveFileManager.get_save_path(SAVE_FILENAME)
        with open(path, "w", encoding="utf-8") as saveFile:
            json.dump(data, saveFile, indent=2)
        syncBrowserSaves()

    def load(self, path):
        try:
            with open(path, "r", encoding="utf-8") as saveFile:
                data = json.load(saveFile)
            validateAgainstSchema(data, SCHEMA_PATH)
            self.state = State.fromDict(data)
        except (ValueError, ValidationError, OSError, KeyError, TypeError) as error:
            # A failed load leaves a fresh state in place of the player's run,
            # and save() writes it back after the very next action - so the
            # bytes that failed are copied aside before play() is reached.
            self.failedLoad = "%s: %s" % (os.path.basename(path), error)
            self.state = State()

    def _preserveDamagedSave(self, path):
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = "%s.damaged-%s" % (path, stamp)
        try:
            shutil.copy2(path, backup)
            where = "A copy was kept at %s." % backup
        except OSError:
            where = "It could not be copied aside."
        self.ui.showDialogue(
            "This save could not be read (%s). You'll start a fresh crossing in "
            "this slot. %s" % (self.failedLoad, where)
        )
