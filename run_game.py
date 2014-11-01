"""A generic turn-based game runner.
"""
from __future__ import print_function
from sys import argv
import utils
import real_pkg
import exmaple

GAME_MODE_EXAMPLE = 'e'
GAME_MODE_REAL = 'r'


def main(verbose, players_def):
    """Main entry point.

    :param verbose: A boolean (T/F) stating whether to display verbose game progress or not.
    :param players_def: A list of strings defining which player to include in the game. The order in which the list is
                        given, is the order of the players. The first letter can be 'e' or 'r' for example or real
                        player respectively. The optional rest of the string will be sent to the constructor of the
                        player, and can be anything (or nothing) that is parsed by the player.
    """
    verbose = verbose.lower() == 't'
    players = []
    for player in players_def:
        mode = player[0]
        type_ = player[1:]
        if mode == GAME_MODE_EXAMPLE:
            players.append(exmaple.Player(type_))
        elif mode == GAME_MODE_REAL:
            players.append(real_pkg.Player(type_))
        else:
            print('bad mode: {}'.format(mode))
            exit()

    game_state = utils.make_initial_state()
    curr_player_idx = 0
    winner = None

    while winner is None:
        player = players[curr_player_idx]
        move = player.get_action(game_state)
        if move not in utils.get_possible_actions(game_state, player):
            raise Exception('Illegal move by ' + repr(player))

        game_state.perform_move(move)
        if verbose:
            game_state.draw()
            print('*' * len(game_state.board))
        winner = utils.is_final_state(game_state)
        curr_player_idx = (curr_player_idx + 1) % len(players)

    print('The winner is ' + repr(winner))


if __name__ == '__main__':

    main(argv[1], argv[2:])