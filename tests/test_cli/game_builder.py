from factories import random_factory
from game.game import Game

import source.library.factories.other_factories as other_fact


class GameBuilder:
    @staticmethod
    def get_game(rand_factory: random_factory.RandomFactory) -> Game:
        other_factories = other_fact.OtherFactories()
        curr_quad_factory = other_fact.CurrentQuadrantFactory()

        galaxy = other_factories.create_galaxy(rand_factory, curr_quad_factory)
        game = Game(galaxy, rand_factory, curr_quad_factory)
        game.skip_enemy_move = True

        return game
