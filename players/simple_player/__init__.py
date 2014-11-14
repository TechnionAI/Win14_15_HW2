import abstract
from utils import MiniMaxWithAlphaBetaPruning, INFINITY
from gameconsts import *


class Player(abstract.AbstractPlayer):
    def __init__(self, color):
        abstract.AbstractPlayer.__init__(self, color)

    def get_move(self, game_state, possible_moves):
        if len(possible_moves) == 1:
            return 0

        minimax = MiniMaxWithAlphaBetaPruning(self.utility, self.color, self.no_more_time)
        _, move = minimax.search(game_state, 2, -INFINITY, INFINITY, True)
        try:
            return possible_moves.index(move)
        except ValueError:
            # Maybe we got None because time has run out
            return 0

    def utility(self, state):
        u = 0
        for square in state.board:
            if square[:1] in MY_COLORS[self.color]:
                # This tower belongs to me
                for piece in square:
                    if piece in OPPONENT_COLORS[self.color]:
                        # This piece is captured by me
                        u += 1

            if square[:1] in OPPONENT_COLORS[self.color]:
                # This tower belongs to the opponent
                for piece in square:
                    if piece in MY_COLORS[self.color]:
                        # This piece is captured by the opponent
                        u -= 1

        return u

    def no_more_time(self):
        return False

    def __repr__(self):
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), 'simple')