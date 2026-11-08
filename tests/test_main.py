"""python -m nightferry: the terminal entry point builds the game on the
console front-end, plays it, and cleans the front-end up when it ends."""

import runpy
import sys

from tak.ui import UIType

from conftest import ScriptedUI
from routes import NEW


def _scriptedCreate(monkeypatch, script):
    from nightferry import game as gameModule

    made = {}

    def fakeCreate(uiType, prompt, header, **kwargs):
        ui = ScriptedUI(script, header)
        ui.currentPrompt = prompt
        made["uiType"] = uiType
        made["ui"] = ui
        return ui

    monkeypatch.setattr(gameModule, "createUserInterface", fakeCreate)
    return made


def test_main_plays_a_crossing_on_the_console_front_end(monkeypatch):
    from nightferry import __main__ as entry

    made = _scriptedCreate(monkeypatch, NEW + ["Quit"])
    entry.main()

    assert made["uiType"] == UIType.CONSOLE
    ui = made["ui"]
    assert ui.dialogues[0].startswith("MV Kittiwake, the Halde crossing")
    assert ui.cleanedUp


def test_running_the_package_as_a_module_calls_main(monkeypatch):
    made = _scriptedCreate(monkeypatch, ["Quit"])
    # Run it fresh, as `python -m` would, even if another test imported it.
    monkeypatch.delitem(sys.modules, "nightferry.__main__", raising=False)
    runpy.run_module("nightferry", run_name="__main__")

    assert made["uiType"] == UIType.CONSOLE
    assert made["ui"].cleanedUp
