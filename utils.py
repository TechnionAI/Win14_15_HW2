from __future__ import print_function
import abstract

TIE = 'tie'


class GameState(abstract.AbstractGameState):
    def __init__(self, board):
        abstract.AbstractGameState.__init__(self)
        self.board = board

    def perform_move(self, move):
        (i, j), player = move
        self.board[i][j] = player

    def draw(self):
        for row in self.board:
            for cell in row:
                print(cell if cell else ' ', end='')
            print()


def make_initial_state():
    return GameState([[None, None, None],
                      [None, None, None],
                      [None, None, None]])


def is_final_state(state):
    board_dim = len(state.board)

    def check_seq_winner(seq):
        first_cell = seq[0]
        if first_cell is not None and all([first_cell == c for c in seq[1:]]):
            return first_cell

        return None

    for row in state.board:
        seq_winner = check_seq_winner(row)
        if seq_winner:
            return seq_winner

    for col in [[state.board[i][j] for i in xrange(board_dim)] for j in xrange(board_dim)]:
        seq_winner = check_seq_winner(col)
        if seq_winner:
            return seq_winner

    seq_winner = check_seq_winner([state.board[i][i] for i in xrange(board_dim)])
    if seq_winner:
        return seq_winner

    seq_winner = check_seq_winner([state.board[i][board_dim - i - 1] for i in xrange(board_dim)])
    if seq_winner:
        return seq_winner

    if all([state.board[i][j] is not None for i in xrange(board_dim) for j in xrange(board_dim)]):
        return TIE

    return None


def get_possible_actions(state, player):
    successors = set()
    dim = len(state.board)
    for i in xrange(dim):
        for j in xrange(dim):
            if state.board[i][j] is None:
                successors.add(((i, j), player))

    return successors


if __name__ == '__main__':
    print(is_final_state(make_initial_state()))

    class TestPlayer(abstract.AbstractPlayer):
        def __init__(self, name):
            abstract.AbstractPlayer.__init__(self)
            self.name = name

        def __repr__(self):
            return self.name

    p1 = TestPlayer('p1')
    p2 = TestPlayer('p2')
    print(is_final_state(GameState([[p1, p2, p2],
                                    [p1, p1, None],
                                    [p2, p2, p2]])))