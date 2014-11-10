"""A game-specific implementations of utility functions.
"""
from __future__ import print_function, division


# White and black soldiers and officers. Empty spaces.
WS = 'w'
WO = 'W'
BS = 'b'
BO = 'B'
EM = ''
WHITE_PLAYER = 'white'
BLACK_PLAYER = 'black'

# Generating the possible single moves. The weird 'if' is making sure we don't go out of board.
DOWN_RIGHT_SINGLE_MOVES = [(i, i + 4) for i in xrange(25) if i % 7 != 3 and i + 4 < 25]
DOWN_LEFT_SINGLE_MOVES = [(i, i + 3) for i in xrange(25) if i % 7 != 0 and i + 3 < 25]
UP_RIGHT_SINGLE_MOVES = [(j, i) for (i, j) in DOWN_LEFT_SINGLE_MOVES]
UP_LEFT_SINGLE_MOVES = [(j, i) for (i, j) in DOWN_RIGHT_SINGLE_MOVES]
UP_SINGLE_MOVES = UP_LEFT_SINGLE_MOVES + UP_RIGHT_SINGLE_MOVES
DOWN_SINGLE_MOVES = DOWN_LEFT_SINGLE_MOVES + DOWN_RIGHT_SINGLE_MOVES
OFFICER_SINGLE_MOVES = UP_SINGLE_MOVES + DOWN_SINGLE_MOVES


# Generating the possible capture moves. Paring single moves for this purpose.
def calc_capture_moves(single_moves):
    return [(i, j, k)
            for (i, j) in single_moves
            for (j2, k) in single_moves
            if j == j2]

DOWN_RIGHT_CAPTURE_MOVES = calc_capture_moves(DOWN_RIGHT_SINGLE_MOVES)
DOWN_LEFT_CAPTURE_MOVES = calc_capture_moves(DOWN_LEFT_SINGLE_MOVES)
UP_RIGHT_CAPTURE_MOVES = calc_capture_moves(UP_RIGHT_SINGLE_MOVES)
UP_LEFT_CAPTURE_MOVES = calc_capture_moves(UP_LEFT_SINGLE_MOVES)
UP_CAPTURE_MOVES = UP_LEFT_CAPTURE_MOVES + UP_RIGHT_CAPTURE_MOVES
DOWN_CAPTURE_MOVES = DOWN_LEFT_CAPTURE_MOVES + DOWN_RIGHT_CAPTURE_MOVES
OFFICER_CAPTURE_MOVES = UP_CAPTURE_MOVES + DOWN_CAPTURE_MOVES


# Assigning moves to specific players
SOLDIER_SINGLE_MOVES = {
    WHITE_PLAYER: UP_SINGLE_MOVES,
    BLACK_PLAYER: DOWN_SINGLE_MOVES,
}
SOLDIER_CAPTURE_MOVES = {
    WHITE_PLAYER: UP_CAPTURE_MOVES,
    BLACK_PLAYER: DOWN_CAPTURE_MOVES,
}

# Assigning colors
SOLDIER_COLOR = {
    WHITE_PLAYER: WS,
    BLACK_PLAYER: BS,
}
OFFICER_COLOR = {
    WHITE_PLAYER: WO,
    BLACK_PLAYER: BO,
}
OPPONENT_COLORS = {
    WHITE_PLAYER: (BS, BO),
    BLACK_PLAYER: (WS, WO),
}


class GameState:
    def __init__(self):
        """ Initializing the board and current player.
        """
        self.board = [
            BS, BS, BS, BS,
              BS, BS, BS,
            BS, BS, BS, BS,
              EM, EM, EM,
            WS, WS, WS, WS,
              WS, WS, WS,
            WS, WS, WS, WS
        ]
        self.curr_player = WHITE_PLAYER

    def calc_single_moves(self):
        """Calculation all the possible single moves.
        :return: All the legitimate single moves for this game state.
        """
        single_soldier_moves = [(i, j) for (i, j) in SOLDIER_SINGLE_MOVES[self.curr_player]
                                if self.board[i][:1] == SOLDIER_COLOR[self.curr_player]
                                and self.board[j] == EM]
        single_officer_moves = [(i, j) for (i, j) in OFFICER_SINGLE_MOVES
                                if self.board[i][:1] == OFFICER_COLOR[self.curr_player]
                                and self.board[j] == EM]
        return single_soldier_moves + single_officer_moves

    def calc_capture_moves(self):
        capture_soldier_moves = [(i, j, k) for (i, j, k) in SOLDIER_CAPTURE_MOVES[self.curr_player]
                                 if self.board[i][:1] == SOLDIER_COLOR[self.curr_player]
                                 and self.board[j][:1] in OPPONENT_COLORS[self.curr_player]
                                 and self.board[k][:1] == EM]
        capture_officer_moves = [(i, j, k) for (i, j, k) in OFFICER_CAPTURE_MOVES
                                 if self.board[i][:1] == OFFICER_COLOR[self.curr_player]
                                 and self.board[j][:1] in OPPONENT_COLORS[self.curr_player]
                                 and self.board[k][:1] == EM]
        return capture_soldier_moves + capture_officer_moves

    def get_possible_moves(self):
        possible_capture_moves = self.calc_capture_moves()
        if possible_capture_moves:
            return possible_capture_moves
        return self.calc_single_moves()

    def perform_move(self, move):
        # Performing the actual move.
        piece = self.board[move[0]]
        self.board[move[0]] = EM

        if len(move) == 2:
            # Single move
            self.board[move[1]] = piece

        else:
            captured = self.board[move[1]]
            self.board[move[1]] = captured[1:]
            self.board[move[2]] = piece + captured[:1]

        # Updating the current player.
        self.curr_player = WHITE_PLAYER if self.curr_player == BLACK_PLAYER else BLACK_PLAYER


def draw(game_state, verbose):
    if verbose == 'n':
        return

    if verbose == 'g':
        import gui
        gui.draw_state(game_state, 'gui/game.png', 'gui/Helvetica.ttf')
        return

    max_len = max((len(piece) for piece in game_state.board))
    # This weird string will be used to format the board cells.
    format_str = '{{:2}}:{{:^{}}}'.format(max_len)

    # Drawing the board row by row.
    i = 0
    for row in xrange(7):
        out_str = ''
        for col in xrange(7):
            if (row + col) % 2 == 0:
                # It's a piece place.
                out_str += format_str.format(i, game_state.board[i])
                i += 1
            else:
                # It's an always empty place.
                out_str += ' ' * (max_len + 3)
        print(out_str)
    print('*' * (7 * (max_len + 3)))


if __name__ == '__main__':
    # Testing stuff.
    s = GameState()
    print(len(s.board))
    # print(DOWN_RIGHT_MOVES)
    print([i for i in UP_SINGLE_MOVES])
    pass
