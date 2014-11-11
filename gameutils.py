"""A game-specific implementations of utility functions.
"""
from __future__ import print_function, division
from gameconsts import *


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
            if piece[:1] == SOLDIER_COLOR[self.curr_player] and move[1] in LAST_LINE[self.curr_player]:
                self.board[move[1]] = OFFICER_COLOR[self.curr_player] + piece[1:]

        else:
            # Capture move
            captured = self.board[move[1]]
            self.board[move[1]] = captured[1:]
            self.board[move[2]] = piece + captured[:1]
            if piece[:1] == SOLDIER_COLOR[self.curr_player] and move[2] in LAST_LINE[self.curr_player]:
                self.board[move[2]] = OFFICER_COLOR[self.curr_player] + self.board[move[2]][1:]

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
