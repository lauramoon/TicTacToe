from common import *
from playbook import Playbook


def get_AI_move(game):
    """
    Determine AI move and return it, taking into account the rotation
    of the board being used in looking up moves
    :param game: the game being played
    :return: the move selected
    """
    # first three turns have set moves
    if game.turn == 1:
        t_move = 5

    elif game.turn == 2:
        # If human played in middle, play in top left, else play in middle
        if game.t_record[1] == 5:
            t_move = 1
        else:
            t_move = 5

    elif game.turn == 3:
        # always play in upper right on transformed board
        t_move = 3

    else:
        # for moves 4-9, look up next move
        next_move = Playbook(game.key).getresult()
        t_move = next_move[0]
        game.result = next_move[1]

    # Update record of transformed game
    game.t_record[game.turn] = t_move
    # Find move on regular board
    move = game.rev_transform(t_move)

    return move


def transform_human_move(game, move):
    """
    Take the human move, determine if board transformation is necessary,
    place move on transformed board
    :param game: the game being played
    :param move: the move selected by the human player
    """
    # in first two turns, rotate board to put human move in
    # upper left or upper center
    if game.turn in [1, 2]:
        # need to rotate board to get t_board
        # before updating move (including creating key)
        if move == 3 or move == 6:
            game.rotate = 3
        if move == 9 or move == 8:
            game.rotate = 2
        if move == 7 or move == 4:
            game.rotate = 1

    # most complicated transformation happens on turn three
    if game.turn == 3:
        # if AI played in corner turn 2, see if need to flip board along x = -y axis
        # (same as rotate cw by 90, then flip along vertical, first two moves on t_board
        # stay in the same place)
        if game.key == 51:
            if move in [2, 3, 6]:
                game.rotate = 1
                game.flip = True

        # if AI played in center turn 2
        # if turn 1 is at 1 on t_board, transformation same as just above,
        # but have to add to any rotation that already might be there
        if game.key == 15:
            if game.transform(move) in [2, 3, 6]:
                game.rotate = (game.rotate + 1) % 4
                game.flip = True

        # if turn 1 is at position 2 on t_board; flip if turn 3 on right side
        if game.key == 25:
            if game.transform(move) in [3, 6, 9]:
                game.flip = True

    # after any necessary board transformations, can finally update t_record
    # with transformed mov
    game.t_record[game.turn] = game.transform(move)


def play_smart(game):
    """
    Play game using the moves in the Playbook for the computer
    updates game.result with game result
    :param game: game being played
    """
    # keep playing a move until there's a result
    while game.result == -1:
        # if human turn
        if (game.first + game.turn) % 2 == 1:
            move = get_human_move(game)
            # Update game board transformations and game.t_result
            transform_human_move(game, move)
            game.update_board(move)

        # else computer's turn
        else:
            move = get_AI_move(game)
            computer_move_text(game)
            game.update_board(move)

        print_board(game.clean_board)

        # Check if board full and no result
        if game.turn == 10 and game.result == -1:
            game.result = 2
            break
