import os

import pytest

from tak import Prompt
from tak.ui import BaseUserInterface

REPOSITORY_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture(autouse=True)
def isolatedRun(monkeypatch, tmp_path):
    """Every test runs from the repository root (the schema path is
    cwd-relative, as it is under Pyodide) and saves into its own directory."""
    monkeypatch.chdir(REPOSITORY_ROOT)
    monkeypatch.setenv("NIGHTFERRY_SAVE_DIR", str(tmp_path / "saves"))


class ScriptedUI(BaseUserInterface):
    """A front-end driven by a script of menu labels.

    Each entry in the script is matched against the labels of the menu
    being shown (substring, first match wins); a label that is not on the
    menu fails the test with the menu printed, which is what makes a
    playthrough test readable when it breaks. Dialogues are recorded."""

    def __init__(self, script, header=None):
        super().__init__(Prompt(), header)
        self.script = list(script)
        self.menus = []
        self.headers = []
        self.dialogues = []
        self.cleanedUp = False

    def lotsOfSpace(self):
        pass

    def divider(self):
        pass

    def showOptions(self, descriptor, optionList, unavailableOptions=None):
        reasons = self.unavailableReasons(optionList, unavailableOptions)
        # Read the header the way a real front-end would, so the provider
        # runs on every menu and a typo in it fails the playthrough.
        self.headers.append(self.header())
        self.menus.append(
            (descriptor, list(optionList), reasons, self.currentPrompt.text)
        )
        if not self.script:
            raise AssertionError(
                "script ran out at menu %r: %r" % (descriptor, optionList)
            )
        wanted = self.script.pop(0)
        for index, label in enumerate(optionList):
            if wanted in label:
                if reasons[index] is not None:
                    raise AssertionError(
                        "%r is unavailable on menu %r (%s)"
                        % (label, descriptor, reasons[index])
                    )
                return str(index + 1)
        raise AssertionError(
            "%r is not on menu %r: %r" % (wanted, descriptor, optionList)
        )

    def showDialogue(self, text):
        self.dialogues.append(text)
        self.currentPrompt.reset()

    def promptForText(self, promptText):
        return self.script.pop(0)

    def timedKeyPress(self, message):
        return 0.0

    def cleanup(self):
        self.cleanedUp = True

    def saw(self, fragment):
        return any(fragment in text for text in self.dialogues)


class FakeGame:
    """Just enough of the game for the clock and the people: state, a
    prompt, learn() and a UI."""

    def __init__(self, ui=None):
        from nightferry.state import State

        self.state = State()
        self.prompt = Prompt()
        self.ui = ui if ui is not None else ScriptedUI([])
        self.spoke = False
        self.returnTo = "saloon"

    def learn(self, factId):
        return self.state.learn(factId)


@pytest.fixture
def scripted(monkeypatch):
    """Build Night Ferry against a ScriptedUI instead of a real front-end."""
    from nightferry import game as gameModule
    from nightferry.game import NightFerry

    holder = {}

    def fakeCreate(uiType, prompt, header, **kwargs):
        ui = ScriptedUI(holder["script"], header)
        ui.currentPrompt = prompt
        holder["ui"] = ui
        return ui

    monkeypatch.setattr(gameModule, "createUserInterface", fakeCreate)

    def make(script):
        holder["script"] = list(script)
        game = NightFerry()
        return game, holder["ui"]

    return make


FIXTURES = os.path.join(REPOSITORY_ROOT, "tests", "fixtures", "saves-0.1.0")


@pytest.fixture
def installSave():
    """Put a save file into slot 1 of this test's save directory, as the
    browser's IndexedDB mirror or a console player's data/ would hold it.
    Returns the path it was written to."""
    import shutil

    def install(name, slot=1):
        directory = os.path.join(os.environ["NIGHTFERRY_SAVE_DIR"], "slot_%d" % slot)
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, "save.json")
        shutil.copy(os.path.join(FIXTURES, name + ".json"), path)
        return path

    return install
