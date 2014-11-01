

class AbstractPlayer:
    def __init__(self):
        pass

    def get_action(self, state):
        raise NotImplementedError


class AbstractGameState:
    def __init__(self):
        pass

    def perform_move(self, move):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError