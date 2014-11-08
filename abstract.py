"""Abstract classes. Your classes must inherit from these.
"""


class AbstractPlayer:
    def __init__(self):
        pass

    def get_move(self, game_state, possible_moves):
        """Chooses an action from the given actions.

        :param game_state: The current game state. It's always a gameutils.GameState object.
        :param possible_moves: A list of possible moves.
        :return: The desired index in the list of possible moves.
        """
        raise NotImplementedError

