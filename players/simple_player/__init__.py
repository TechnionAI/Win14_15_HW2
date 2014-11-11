import abstract


class Player(abstract.AbstractPlayer):
    def __init__(self, color):
        abstract.AbstractPlayer.__init__(self, color)

    def get_move(self, game_state, possible_moves):
        return abstract.AbstractPlayer.get_move(self, game_state, possible_moves)

    def __repr__(self):
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), 'simple')