
# ANSI Color Codes
WHITE_COLOR = "\033[97m"
BLACK_COLOR = "\033[35m"
RESET_COLOR = "\033[0m"


def print_board_ascii(board):
    # Mapping based on your files: "Right" is 'R'
    piece_map = {"pawn": "P", "right": "R", "knight": "N",
                 "bishop": "B", "queen": "Q", "king": "K"}
    grid = [["." for _ in range(5)] for _ in range(5)]

    for piece in board.get_pieces():
        pos = piece.position
        ch = piece_map.get(piece.name.lower(), "?")

        # Determine color based on player name
        if piece.player.name.lower() == "white":
            # White pieces are uppercase, wrapped in WHITE_COLOR code
            colored_ch = f"{WHITE_COLOR}{ch.upper()}{RESET_COLOR}"
        else:
            # Black pieces are lowercase, wrapped in BLACK_COLOR code
            colored_ch = f"{BLACK_COLOR}{ch.lower()}{RESET_COLOR}"

        grid[pos.y][pos.x] = colored_ch

    print("  0 1 2 3 4")
    # Join the grid rows, which now contain the color codes
    for row in (range(5)):
        print(f"{row} " + " ".join(grid[row]))


def list_legal_moves_for(board, player):
    pairs = []
    for pc in board.get_player_pieces(player):
        for opt in pc.get_move_options():
            pairs.append((pc, opt))
    return pairs


def copy_piece_move(board, piece, move):
    try:
        if piece and move:
            for tp in board.get_player_pieces(piece.player):
                if type(tp) is type(piece) and tp.position == piece.position:
                    temp_piece = tp
                    break
            if temp_piece is None:
                return board, None, None
            # find the equivalent move option on the cloned piece
            dest = getattr(move, "position", None)
            temp_move = None
            for m in temp_piece.get_move_options():
                m_dest = getattr(m, "position", None)
                if m_dest == dest:
                    temp_move = m
                    return board, temp_piece, temp_move
            return board, temp_piece, None
        else:
            return board, None, None
    except Exception:
        return board, None, None
