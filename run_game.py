"""A generic turn-based game runner.
"""
from __future__ import print_function
from sys import argv
import gameutils
import real_pkg
import exmaple
import utils

GAME_MODE_EXAMPLE = 'e'
GAME_MODE_REAL = 'r'


def setup_player(players, remaining_run_times, time_limit, player_class, type_):
    exmaple_player, setup_time = utils.run_with_limited_time(player_class, (type_, ), {}, time_limit)
    players.append(exmaple_player)
    remaining_run_times.append(time_limit - setup_time)


def main(time_limit, verbose, players_def):
    """Main entry point.

    :param time: The float amount of total seconds given to each player. Give 'inf' for unbounded time.
    :param verbose: A boolean (T/F) stating whether to display verbose game progress or not.
    :param players_def: A list of strings defining which player to include in the game. The order in which the list is
                given, is the order of the players. The first letter can be 'e' or 'r' for example or real
                player respectively. The optional rest of the string will be sent to the constructor of the
                player, and can be anything (or nothing) that is parsed by the player.
    """
    verbose = verbose.lower() == 't'
    time_limit = float(time_limit)

    players = []
    remaining_run_times = []

    for player in players_def:
        mode = player[0]
        type_ = player[1:]
        if mode == GAME_MODE_EXAMPLE:
            setup_player(players, remaining_run_times, time_limit, exmaple.Player, type_)
        elif mode == GAME_MODE_REAL:
            setup_player(players, remaining_run_times, time_limit, real_pkg.Player, type_)
        else:
            print('bad mode: {}'.format(mode))
            exit()

    game_state = gameutils.make_initial_state()
    curr_player_idx = 0
    winner = None

    while winner is None:
        player = players[curr_player_idx]
        remaining_run_time = remaining_run_times[curr_player_idx]
        try:
            move, run_time = utils.run_with_limited_time(player.get_action, (game_state, ), {}, remaining_run_time)
            remaining_run_times[curr_player_idx] -= run_time
            if remaining_run_times[curr_player_idx] < 0:
                raise utils.PlayerExceededTimeError
        except utils.PlayerExceededTimeError:
            print('Player {} exceeded time.'.format(player))
            break

        possible_actions = gameutils.get_possible_actions(game_state, player)
        if (move, player) not in possible_actions:
            raise Exception('Illegal move by ' + repr(player))

        game_state.perform_move(move, player)
        if verbose:
            game_state.draw()
            print('*' * len(game_state.board))
        winner = gameutils.is_final_state(game_state)
        curr_player_idx = (curr_player_idx + 1) % len(players)

    print('The winner is ' + repr(winner))
    if verbose:
        print('remaining runtimes: {}'.format([(players[i], remaining_run_times[i]) for i in xrange(len(players))]))


if __name__ == '__main__':

    main(argv[1], argv[2], argv[3:])