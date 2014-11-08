import abstract
import random


class Player(abstract.AbstractPlayer):
    def __init__(self):
        abstract.AbstractPlayer.__init__(self)

    def get_move(self, game_state, possible_moves):
        return random.choice(range(len(possible_moves)))

    def __repr__(self):
        return 'random'