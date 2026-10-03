# @author Daniel McCoy Stephenson
from nightferry import endings
from nightferry.lastboat.premise import LAST_BOAT_LABEL
from nightferry.scenes.base import Scene


class Epilogue(Scene):
    """After the first crossing's ending. The last page can be read again,
    the notebook is still there, and the Kittiwake has one more night run in
    her: the last night boat, in March, sailed from this save with
    everything October left behind."""

    id = "epilogue"
    travelTo = ()

    def run(self):
        options = [
            "Read the last page again",
            "Open your notebook",
            LAST_BOAT_LABEL,
            "Quit",
        ]
        label = options[
            int(
                self.ui.showOptions(
                    "Halde, six in the morning: %s. The ramp is down and the "
                    "passengers are going ashore into the grey."
                    % endings.name(self.state),
                    options,
                )
            )
            - 1
        ]
        if label == "Read the last page again":
            self.ui.showDialogue(endings.text(self.state))
            return self.id
        if label == "Open your notebook":
            self.game.returnTo = self.id
            return self.go("journal")
        if label == LAST_BOAT_LABEL:
            return self.game.sailTheLastBoat()
        return "quit"
