import abstract
import random

TYPE_RANDOM = 'random'


class Player(abstract.AbstractPlayer):
    def __init__(self, type_):
        abstract.AbstractPlayer.__init__(self)
        self.type_ = type_

    def get_action(self, state):
        dim = len(state.board)
        i, j = random.randrange(dim), random.randrange(dim)
        while state.board[i][j] is not None:
            i, j = random.randrange(dim), random.randrange(dim)

        return i, j

    def __repr__(self):
        return self.type_