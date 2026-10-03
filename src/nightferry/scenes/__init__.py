# @author Daniel McCoy Stephenson
"""One class per place on the boat. Each has run(), which shows the place's
menu once, acts on the choice, and returns the id of the place to show next
- usually the same one - or "quit"."""

from nightferry.scenes.saloon import Saloon
from nightferry.scenes.cardeck import CarDeck
from nightferry.scenes.corridor import Corridor
from nightferry.scenes.deck import Deck
from nightferry.scenes.wheelhouse import Wheelhouse
from nightferry.scenes.journal import Journal
from nightferry.scenes.epilogue import Epilogue

QUIT = "quit"


def build(game):
    return {
        "saloon": Saloon(game),
        "cardeck": CarDeck(game),
        "corridor": Corridor(game),
        "deck": Deck(game),
        "wheelhouse": Wheelhouse(game),
        "journal": Journal(game),
        "epilogue": Epilogue(game),
    }
