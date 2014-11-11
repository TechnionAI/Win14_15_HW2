"""A generic turn-based game runner.
"""
from __future__ import print_function
import sys
import gameutils
import utils
import copy
from gameconsts import WHITE_PLAYER, BLACK_PLAYER


def setup_player(players, remaining_run_times, time_limit, player_class, player_color):
    """ An auxiliary function to populate the players list, and measure setup times on the go.

    :param players: The current list of players.
    :param remaining_run_times: The current list of remaining runtimes.
    :param time_limit: The time limit for this players.
    :param player_class: The player class that should be initialized, measured and put into the list.
    """
    player, setup_time = utils.run_with_limited_time(player_class, (player_color,), {}, time_limit)
    players.append(player)
    remaining_run_times.append(time_limit - setup_time)


def main(time_limit, verbose, white_player, black_player):
    """Main entry point.

    :param time_limit: The float amount of total seconds given to each player. Give 'inf' for unbounded time.
    :param verbose: Indication the level of verbosity of describing the progress of the game.
        One of the following: (n, t, g) for (no draw, terminal, and gui).
    :param white_player: The name of the module containing the white player. E.g. "myplayer" will invoke an equivalent
        to "import myplayer" in the code.
    :param black_player: Same as 'white_player' parameter, but for the black one.
    """
    verbose = verbose.lower()
    time_limit = float(time_limit)

    players = []
    remaining_run_times = []

    # Dynamically importing the players. This allows maximum flexibility and modularity.
    white_player = 'players.{}'.format(white_player)
    black_player = 'players.{}'.format(black_player)
    __import__(white_player)
    __import__(black_player)

    setup_player(players, remaining_run_times, time_limit, sys.modules[white_player].Player, WHITE_PLAYER)
    setup_player(players, remaining_run_times, time_limit, sys.modules[black_player].Player, BLACK_PLAYER)

    game_state = gameutils.GameState()
    curr_player_idx = 0
    winner = None

    # Running the actual game loop. Assuming the game ends when someone is left out of moves.
    while True:
        gameutils.draw(game_state, verbose)

        player = players[curr_player_idx]
        remaining_run_time = remaining_run_times[curr_player_idx]
        try:
            possible_moves = game_state.get_possible_moves()
            if not possible_moves:
                winner = players[0 if curr_player_idx == 1 else 1]
                break
            move_idx, run_time = utils.run_with_limited_time(
                player.get_move, (copy.deepcopy(game_state), possible_moves), {}, remaining_run_time)
            remaining_run_times[curr_player_idx] -= run_time
            if remaining_run_times[curr_player_idx] < 0:
                raise utils.ExceededTimeError
        except utils.ExceededTimeError:
            print('Player {} exceeded time.'.format(player))
            winner = players[0 if curr_player_idx == 1 else 1]
            break

        game_state.perform_move(possible_moves[move_idx])
        if verbose in ('t', 'g'):
            print('Player ' + repr(player) + ' performed the move: ' + repr(possible_moves[move_idx]))
        curr_player_idx = (curr_player_idx + 1) % len(players)

    print('The winner is ' + repr(winner))
    if verbose in ('t', 'g'):
        print('remaining runtimes: {}'.format([(players[i], remaining_run_times[i]) for i in xrange(len(players))]))


if __name__ == '__main__':

    main(*sys.argv[1:])