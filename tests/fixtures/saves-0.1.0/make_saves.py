"""How the saves in this directory were made - kept for the record, not run
by the tests.

They are save.json files written by Night Ferry 0.1.0 itself (main 2c81298,
schema version 1, before the last night boat existed): its own NightFerry
game, its own save(), driven through scripted routes by its own test
ScriptedUI. test_save_compat.py loads them with the current game.

To remake them, check out 0.1.0 and run this file with that checkout on the
path:

    git worktree add /tmp/nf-0.1.0 2c81298
    python tests/fixtures/saves-0.1.0/make_saves.py /tmp/nf-0.1.0 <out-dir>
"""
import os
import shutil
import sys
import tempfile

ROOT, OUT = sys.argv[1], sys.argv[2]
os.chdir(ROOT)
sys.path[:0] = [ROOT + "/src", ROOT + "/tests"]
from conftest import ScriptedUI  # noqa: E402
from nightferry import game as gameModule  # noqa: E402
from routes import CANONICAL, DO_NOTHING, KEPT, NEW, PANTRY, waitInPantry  # noqa: E402


def run(name, script):
    os.environ["NIGHTFERRY_SAVE_DIR"] = tempfile.mkdtemp()

    def fake(uiType, prompt, header, **kwargs):
        ui = ScriptedUI(script, header)
        ui.currentPrompt = prompt
        return ui

    gameModule.createUserInterface = fake
    game = gameModule.NightFerry()
    game.play()
    shutil.copy(
        game.saveFileManager.get_save_path("save.json"),
        os.path.join(OUT, name + ".json"),
    )
    print(name, game.state.clock, game.state.ending, len(game.state.facts))


churchyard = list(CANONICAL)
churchyard[
    churchyard.index("Do what she asked. The light.")
] = "Take her home to the churchyard"
churchyard[-1:] = [PANTRY, "Quit"]
run("off_the_light", CANONICAL)
run("beside_arne", churchyard)
run("at_the_door", DO_NOTHING)
run("kept_crossing", KEPT)
# Kept, with Maren's letter still in the steward's pocket.
run(
    "kept_letter_in_pocket",
    NEW
    + [
        "Walk the lower deck",
        "Lift the tarpaulin",
        "Go out on the open deck",
        "Talk to the boy",
        "Whose is Harbour House",
        "[Back]",
        "Go along the cabin corridor",
        "Knock at cabin 4",
        "What takes you to Halde",
        "Give it to me",
        "[Back]",
        "Go up to the wheelhouse",
        "Talk to the captain",
        "Who was cabin 6 for, captain",
        "I'll keep it",
        "[Back]",
        "Go along the cabin corridor",
    ]
    + waitInPantry(9)
    + ["Quit"],
)
# Mid-crossing: 9:40 pm, nine facts, two choices made.
run("mid_crossing", CANONICAL[: CANONICAL.index("Go out on the open deck")] + ["Quit"])
