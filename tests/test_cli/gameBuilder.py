# region imports
import sys

sys.path.append("/pythontrek/source/library/")
from factories import randomFactory
from game.game import Game

import source.library.factories.otherFactories as otherFact

# endregion


class GameBuilder:
    @staticmethod
    def getGame(randFactory: randomFactory.RandomFactory) -> Game:
        otherFactories = otherFact.otherFactories()
        currQuadFactory = otherFact.CurrentQuadrantFactory()

        galaxy = otherFactories.createGalaxy(randFactory, currQuadFactory)
        game = Game(galaxy, randFactory, currQuadFactory)
        game.skipEnemyMove = True

        return game
