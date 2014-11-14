from __future__ import print_function
import abstract


class Player(abstract.AbstractPlayer):
    def __init__(self, color):
        abstract.AbstractPlayer.__init__(self, color)

    def get_move(self, game_state, possible_moves):
        print('Available moves: ' + str([i for i in enumerate(possible_moves)]))
        while True:
            idx = raw_input('Enter the index of your move: ')
            try:
                idx = int(idx)
                if idx not in xrange(len(possible_moves)):
                    raise ValueError
                return idx
            except ValueError:
                # Ignoring
                pass

    def __repr__(self):
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), 'interactive')