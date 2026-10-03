import json
import os

from nightferry import endings, facts, flags
from nightferry.game import describeSlot
from nightferry.state import DOCKING, THE_LIGHT

from routes import CANONICAL, NEW


def test_the_canonical_solve_learns_everything_and_ends_off_the_light(scripted):
    game, ui = scripted(CANONICAL)
    game.play()
    state = game.state

    assert state.ending == endings.OFF_THE_LIGHT
    assert state.minute == THE_LIGHT
    # Every one of the sixteen facts, on one crossing.
    for fact in facts.FACTS:
        assert state.knows(fact), fact
    assert len(state.facts) == 16
    # Every person's remembered choice, and the beat that says so.
    for who in ("Oskar", "Hanne", "Dr Fenn", "Raske", "Gus", "Jory", "Tove", "Ingrid"):
        assert ui.saw("[%s will remember that.]" % who), who
    assert state.flags[flags.HANNE_CHOSE_LIGHT] is True
    assert state.flags[flags.INGRID_WILL_STOP] is True
    assert state.flags[flags.MET_IN_WHEELHOUSE] is True
    assert flags.AT_THE_DOOR not in state.flags
    # The last page says what happened, who the cabin was for, what you did,
    # and what it cost whom.
    assert ui.saw("WHAT HAPPENED. At five o'clock the Kittiwake stopped her engines")
    assert ui.saw("WHO CABIN 6 WAS FOR. Maren Sollid")
    assert ui.saw("WHAT YOU DID. You found out who cabin 6 was for")
    assert ui.saw("OSKAR. Cleared.")
    assert ui.saw("YOU. You opened cabin 6 - the one thing Oskar asked you not to")
    assert ui.cleanedUp


def test_the_opening_screen_is_the_one_the_owner_picked(scripted):
    game, ui = scripted(NEW + ["Quit"])
    game.play()
    assert ui.dialogues[0].startswith("MV Kittiwake, the Halde crossing")
    assert "You are the night steward" in ui.dialogues[0]
    descriptor, options, reasons, _ = ui.menus[1]
    assert descriptor.startswith("8:00 pm, the Halde crossing. The ferry leaves on time.")
    assert options[:4] == [
        "Walk the lower deck",
        "Ask the purser about cabin 6",
        "Sit with the woman holding two tickets",
        "Go up to the wheelhouse",
    ]
    header = ui.headers[1]
    assert header["title"] == "Night Ferry - 8:00 pm"
    texts = [chip["text"] for chip in header["chips"]]
    assert texts == ["8:00 pm", "The Saloon", "Hours to dock: 10", "Known: 0/16"]


def test_the_crossing_is_saved_after_every_action_and_the_slot_describes_it(scripted):
    game, ui = scripted(CANONICAL)
    game.play()
    path = game.saveFileManager.get_save_path("save.json")
    with open(path) as f:
        data = json.load(f)
    assert data["ending"] == endings.OFF_THE_LIGHT
    metadata = game.saveFileManager.list_save_files()[0]["metadata"]
    assert describeSlot(metadata) == "docked - off the light, 16 known"


def test_a_saved_crossing_resumes_where_it_was(scripted):
    script = NEW + [
        "Ask the purser about cabin 6",
        "What's the story with cabin 6",
        "[Back]",
        "Go out on the open deck",
        "Quit",
    ]
    game, ui = scripted(script)
    game.play()
    assert game.state.minute == 20
    game2, ui2 = scripted(["Load Slot 1", "Quit"])
    game2.play()
    assert game2.state.minute == 20
    assert game2.state.facts == [facts.CABIN_SIX]
    assert game2.state.location == "deck"
    assert ui2.menus[0][1][0] == "Load Slot 1 (8:20 pm, 1 known)"
    assert not any(d.startswith("MV Kittiwake") for d in ui2.dialogues)


def test_talking_costs_a_turn_only_if_something_was_asked(scripted):
    game, ui = scripted(NEW + ["Ask the purser", "[Back]", "Quit"])
    game.play()
    assert game.state.minute == 0
    game, ui = scripted(NEW + ["Ask the purser", "Anything that needs doing", "[Back]", "Quit"])
    game.play()
    assert game.state.minute == 20


def test_the_header_counts_down_and_counts_up(scripted):
    game, ui = scripted(NEW + ["Ask the purser", "cabin 6", "[Back]", "Quit"])
    game.play()
    texts = [chip["text"] for chip in ui.headers[-1]["chips"]]
    assert "Known: 1/16" in texts and "Hours to dock: 10" in texts
    assert ui.headers[-1]["title"] == "Night Ferry - 8:20 pm"


def test_quitting_the_save_menu_still_cleans_up(scripted):
    game, ui = scripted(["Quit"])
    game.play()
    assert ui.cleanedUp
    assert game.running is False


def test_a_damaged_save_is_kept_aside_and_a_fresh_crossing_starts(scripted):
    game, ui = scripted(NEW + ["Quit"])
    game.play()
    path = game.saveFileManager.get_save_path("save.json")
    with open(path, "w") as f:
        f.write('{"version": 1, "minute": "ten", "facts": []}')

    game2, ui2 = scripted(["Load Slot 1", "Quit"])
    # The slot menu describes it without crashing, before load() refuses it.
    assert ui2.menus[0][1][0].startswith("Load Slot 1 (damaged, 0 known)")
    game2.play()
    assert game2.failedLoad
    assert ui2.saw("This save could not be read")
    damaged = [n for n in os.listdir(os.path.dirname(path)) if "damaged" in n]
    assert damaged
    assert game2.state.minute == 0


def test_the_notebook_is_free_and_returns_where_it_was_opened(scripted):
    script = NEW + [
        "Ask the purser",
        "cabin 6",
        "[Back]",
        "Go out on the open deck",
        "Open your notebook",
        "What is happening to you",
        "What you know",
        "The night, as you know it",
        "Close the notebook",
        "Quit",
    ]
    game, ui = scripted(script)
    game.play()
    assert game.state.minute == 20
    assert game.state.location == "deck"
    assert ui.saw("WHAT IS HAPPENING TO YOU. Cabin 6 was booked")
    assert ui.saw("There's more to learn:")
    assert ui.saw("The Halde light, abeam to port.")
