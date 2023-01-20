"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if terminal(board):
        return

    countX = 0
    countO = 0
    for row in board:
        for entry in row:
            if entry == X:
                countX += 1
            elif entry == O:
                countO += 1

    if countO < countX:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for i, row in enumerate(board):
        for j, entry in enumerate(row):
            if entry is None:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    player_move = player(board)

    new_board = copy.deepcopy(board)
    i, j = action

    if board[i][j] != None:
        raise Exception("unvalid move")
    else:
        new_board[i][j] = player_move

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    wins = [[(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)], [
        (0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]]

    for player in [X, O]:
        for win in wins:
            won = True
            for coords in win:
                i, j = coords
                if board[i][j] != player:
                    won = False
            if won:
                return player
    return


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if actions(board) == set():
        return True

    if winner(board) is not None:
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    if winner(board) is None:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    if player(board) == X:
        return maxValue(board)[1]
    elif player(board) == O:
        return minValue(board)[1]


def maxValue(board):
    optimal_move = ()

    if terminal(board):
        return utility(board), optimal_move

    v = - math.inf
    for action in actions(board):
        minV = minValue(result(board, action))[0]
        if minV > v:
            v = minV
            optimal_move = action
    return v, optimal_move


def minValue(board):
    optimal_move = ()

    if terminal(board):
        return utility(board), optimal_move

    v = math.inf
    for action in actions(board):
        maxV = maxValue(result(board, action))[0]
        if maxV < v:
            v = maxV
            optimal_move = action
    return v, optimal_move
