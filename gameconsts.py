
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