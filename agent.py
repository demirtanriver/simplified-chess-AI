import random
from extension.board_utils import list_legal_moves_for, copy_piece_move
from extension.board_rules import get_result
import time

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
                return -(WIN_SCORE + depth)  # depth is the remaining depth
            else:
                # The root_player won the game
                return (WIN_SCORE + depth)

        if "Stalemate" in game_result:
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

    legal_moves.sort(key=lambda x: get_mvvlva_score(x, board), reverse=True)
    # random.shuffle(legal_moves)

    for piece_to_move, move_opt in legal_moves:

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

    legal_moves.sort(key=lambda x: get_mvvlva_score(x, board), reverse=True)
    # random.shuffle(legal_moves)

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
    The agent uses Iterative Deepening, Alpha-Beta Pruning, MVV-LVA, and 
    Principal Variation (PV) Ordering.
    '''
    TIME_LIMIT = 30
    ROOT_PLAYER = player
    MAX_DEPTH = 1

    best_move = (None, None)
    best_score = -99999999

    legal_moves = list_legal_moves_for(board, player)

    if not legal_moves:
        return None, None

    start_time_total = time.time()

    legal_moves.sort(key=lambda x: get_mvvlva_score(x, board), reverse=True)

    pv_move = None

    while True:

        if time.time() - start_time_total > TIME_LIMIT * 0.98:
            break

        root_moves = list(legal_moves)

        if pv_move:
            try:
                root_moves.remove(pv_move)

                root_moves.insert(0, pv_move)
            except ValueError:
                # If the move isn't legal anymore
                pv_move = None

        # TEMPORARY: Print the order of the first 5 moves for the current depth
        print(f"Depth {MAX_DEPTH} Root Move Order:")
        for i, (piece, move_opt) in enumerate(root_moves[:5]):
            start_pos = f"{piece.position.x},{piece.position.y}"
            end_pos = f"{move_opt.position.x},{move_opt.position.y}"
            print(f"  {i+1}: {piece.name} from {start_pos} to {end_pos}")
        print("-" * 20)
        # END TEMPORARY CODE

        current_best_move = (None, None)
        current_best_score = -999999999

        for piece_to_move, move_opt in root_moves:

            if time.time() - start_time_total > TIME_LIMIT * 0.95:
                # return previous best move if time runs out
                return best_move

            # applies the move on a clone board
            temp_board = board.clone()
            temp_board, moved_piece, applied_move = copy_piece_move(
                temp_board, piece_to_move, move_opt)

            if not (moved_piece and applied_move):
                continue

            # move the piece if its a valid move
            moved_piece.move(applied_move)

            # The next state is the opponent's turn.
            current_score = min_value(
                board=temp_board,
                depth=MAX_DEPTH - 1,
                alpha=-999999999,  # Use MIN_VAL constant
                beta=999999999,  # Use MAX_VAL constant
                root_player=ROOT_PLAYER
            )

            if current_score > current_best_score:
                current_best_score = current_score
                current_best_move = (piece_to_move, move_opt)

                pv_move = current_best_move

        if current_best_move != (None, None):
            best_move = current_best_move
            best_score = current_best_score

            print(
                f"Completed search to Depth {MAX_DEPTH}. Best score: {best_score}. Took {time.time()-start_time_total:.2f} seconds")

            MAX_DEPTH += 1
        else:
            break

    return best_move


def human_player(board, player, var):
    """Allows a human user to input a move using (x,y)-(x,y) coordinates."""

    legal_moves = list_legal_moves_for(board, player)

    if not legal_moves:
        print(f"Human player ({player.name}) has no legal moves.")
        return None, None

    # Map legal moves to a simple "start_x,start_y-end_x,end_y" string for validation
    valid_inputs = {}
    for piece, move_opt in legal_moves:
        # Format: "0,4-2,2"
        input_key = f"{piece.position.x},{piece.position.y}-{move_opt.position.x},{move_opt.position.y}"
        valid_inputs[input_key] = (piece, move_opt)

    print("-" * 40)
    print(f"It is YOUR turn ({player.name}).")
    print(f"Enter move (e.g., 0,4-2,2) or 'LIST' to see all valid options:")

    while True:
        try:
            user_input = input("> ").strip()

            if user_input.upper() == 'LIST':
                print("\nValid Moves:")
                # Prints up to 5 valid moves per line for readability
                print(*(list(valid_inputs.keys())
                      [i:i + 5] for i in range(0, len(valid_inputs), 5)), sep='\n')
                continue

            if user_input in valid_inputs:
                return valid_inputs[user_input]
            else:
                print("Invalid move format or illegal move. Try again, or type 'LIST'.")

        except Exception as e:
            print(f"An error occurred: {e}")

    return None, None


def get_mvvlva_score(piece_move_pair, board):
    """
    Calculates the MVV-LVA score for a single move using PIECE_VALUES. 
    A multiplier is used to ensure all captures are scored > 0.
    """
    piece, move_opt = piece_move_pair

    captured_pieces = getattr(move_opt, "captures", [])

    if not captured_pieces:
        return 0

    victim_value = 0

    for victim_pos in captured_pieces:

        cell = board[victim_pos]
        victim_piece = cell.piece

        if victim_piece:
            value = PIECE_VALUES.get(victim_piece.name, 100)

            victim_value = max(victim_value, value * 10)

    attacker_value = PIECE_VALUES.get(piece.name, 100)

    return victim_value - attacker_value
