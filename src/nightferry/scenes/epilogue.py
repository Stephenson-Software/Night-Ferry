# @author Daniel McCoy Stephenson
from nightferry import endings
from nightferry.scenes.base import Scene


class Epilogue(Scene):
    """After the ending. The last page can be read again, the notebook is
    still there, and there is nothing else to do but go ashore."""

    id = "epilogue"
    travelTo = ()

    def run(self):
        options = ["Read the last page again", "Open your notebook", "Quit"]
        choice = int(
            self.ui.showOptions(
                "Halde, six in the morning: %s. The ramp is down and the "
                "passengers are going ashore into the grey." % endings.name(self.state),
                options,
            )
        )
        if choice == 1:
            self.ui.showDialogue(endings.text(self.state))
            return self.id
        if choice == 2:
            self.game.returnTo = self.id
            return self.go("journal")
        return "quit"
