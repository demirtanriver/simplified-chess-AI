import random
from extension.board_utils import list_legal_moves_for, copy_piece_move
from extension.board_rules import get_result

WIN_SCORE = 10000000
LOSS_SCORE = -9000000
DRAW_SCORE = 0

PIECE_VALUES = {
    "King": 0,
    "Queen": 900,
    "Right": 750,
    "Bishop": 300,
    "Knight": 300,
    "Pawn": 100
}


# Custom Helper Function in agent.py (used in the template I provided)

def get_terminal_score(board, depth, root_player):
    """Checks for terminal state and returns score relative to 'root_player'.
    taking away the depth from the score ensures that if there is a guaranteed mate, the algorithm will prefer the quickest mate

    """

    game_result = get_result(board)
    if game_result:

        if "Checkmate" in game_result or "no kings" in game_result:
            # If the current player (who is now to move) is the one who lost the King,
            # or was mated, the score for the root_player is negative (a loss).
            if board.current_player == root_player:
                return -(WIN_SCORE - depth)
            else:
                # The root_player won the game
                return (WIN_SCORE - depth)

        if "Stalemate" in game_result:
            # The player whose turn it is (board.current_player) is the one who is stalemated
            # and loses the game.
            if board.current_player == root_player:
                # Root player loses by stalemate
                return LOSS_SCORE
            else:
                # Root player wins by opponent's stalemate
                return - LOSS_SCORE  # A positive score!

        if "Draw" in game_result or "only 2 kings" in game_result:
            return DRAW_SCORE

    return None


def min_value(board, depth, alpha, beta, root_player):
    """
    Finds the minimum score for the minimizing player (Opponent).
    The score is returned from the 'root_player's' perspective.

    Args:
        board (Board): The current board state.
        depth (int): Remaining search depth.
        alpha (float): The best score found so far for the MAX player (Agent).
        beta (float): The best score found so far for the MIN player (Opponent).
        root_player (Player): The player whose perspective the final score must be calculated from.
    """

    # returns ends score if it has ended
    terminal_score = get_terminal_score(board, depth, root_player)
    if terminal_score is not None:
        return terminal_score

    if depth == 0:
        return evaluate(board, root_player)

    # the thing we're trying to minimise so it has to start as a high value
    v = 99999999999

    # Get legal moves for the current player (who is MIN)
    legal_moves = list_legal_moves_for(board, board.current_player)

    # Note: Phase II (Move Ordering) would go here

    for piece_to_move, move_opt in legal_moves:

        # 4. Try the move on a clone
        temp_board = board.clone()
        temp_board, moved_piece, applied_move = copy_piece_move(
            temp_board, piece_to_move, move_opt)

        if moved_piece and applied_move:
            moved_piece.move(applied_move)

            score = max_value(temp_board, depth - 1, alpha, beta, root_player)

            v = min(v, score)
            beta = min(beta, v)

            # ignores the branch if alpha >= beta
            if alpha >= beta:
                break

    return v


def max_value(board, depth, alpha, beta, root_player):
    """
    Finds the maximum score for the maximizing player (Agent).
    The score is returned from the 'root_player's' perspective.

    Args:
        board (Board): The current board state.
        depth (int): Remaining search depth.
        alpha (float): The best score found so far for the MAX player (Agent).
        beta (float): The best score found so far for the MIN player (Opponent).
        root_player (Player): The player whose perspective the final score must be calculated from.
    """

    # returns ends score if it has ended
    terminal_score = get_terminal_score(board, depth, root_player)
    if terminal_score is not None:
        return terminal_score

    if depth == 0:
        return evaluate(board, root_player)

    # the thing we're trying to maximise has to start negative
    v = -99999999999

    # get all legal moves for the current player (who is MAX)
    legal_moves = list_legal_moves_for(board, board.current_player)

    for piece_to_move, move_opt in legal_moves:

        # Try the move on a clone board
        temp_board = board.clone()
        # copy_piece_move ensures we get the piece/move objects linked to the clone
        temp_board, moved_piece, applied_move = copy_piece_move(
            temp_board, piece_to_move, move_opt)

        if moved_piece and applied_move:
            moved_piece.move(applied_move)

            score = min_value(temp_board, depth - 1, alpha, beta, root_player)

            v = max(v, score)

            alpha = max(alpha, v)
            if alpha >= beta:
                break

    return v


def evaluate(board, player):
    '''
    Basic material-only evaluation. Currently based only on material values.
    '''
    score = 0
    for piece in board.get_pieces():
        value = PIECE_VALUES.get(piece.name, 0)
        if piece.player == player:
            score += value
        else:
            score -= value
    return score


def agent(board, player, var):
    '''
    the agent looks at all possible moves at a ply depth of one and runs the 
    minimax algorithm on each move the estimate which one leads to the better state

    args:
        board               : the board being played on 
        ROOT_PLAYER (player): the player whose turn it is to make a move.
                            we maximise for the root_player.

    '''
    # Hints:
    # List of players on the current board game: list(board.players) - default list: [Player (white), Player (black)]
    # board.players[0].name = "white" and board.players[1].name = "black"
    # Name of the player assigned to the agent (either "white" or "black"): player.name
    # list of pieces of the current player: list(board.get_player_pieces(player))
    # List of pieces and corresponding moves for each pieces of the player: piece, move_opt = list_legal_moves_for(board, player)
    # List of legal move for a corresponding pieces: piece.get_move_options()

    ROOT_PLAYER = player
    MAX_DEPTH = 4

    best_move = (None, None)
    best_score = -99999999999

    legal_moves = list_legal_moves_for(board, player)

    if not legal_moves:
        return None, None  # No legal moves, likely game over

    random.shuffle(legal_moves)

    for piece_to_move, move_opt in legal_moves:

        # applies the move on a clone board
        temp_board = board.clone()
        temp_board, moved_piece, applied_move = copy_piece_move(
            temp_board, piece_to_move, move_opt)

        if not (moved_piece and applied_move):
            continue

        # move the piece if its a valid move
        moved_piece.move(applied_move)

        # The next state is the opponent's turn.
        # start the recursive search one level shallower (MAX_DEPTH - 1).
        current_score = min_value(
            board=temp_board,
            depth=MAX_DEPTH - 1,
            alpha=-99999999999,
            beta=99999999999,
            root_player=ROOT_PLAYER
        )

        # We want the move that maximizes the score for the ROOT_PLAYER
        if current_score > best_score:
            best_score = current_score
            best_move = (piece_to_move, move_opt)

    return best_move
