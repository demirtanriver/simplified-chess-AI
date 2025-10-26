from chessmaker.chess.base import Player
from chessmaker.chess.pieces import King, Bishop, Knight, Queen
from extension.piece_right import Right
from extension.piece_pawn import Pawn_Q
from chessmaker.chess.base import Square

white = Player("white")
black = Player("black")

sample0 = [
    [Square(Knight(black)), Square(Queen(black)), Square(
        King(black)), Square(Bishop(black)), Square(Right(black))],
    [Square(Pawn_Q(black)), Square(Pawn_Q(black)), Square(
        Pawn_Q(black)), Square(Pawn_Q(black)), Square(Pawn_Q(black))],
    [Square(), Square(), Square(), Square(), Square()],
    [Square(Pawn_Q(white)), Square(Pawn_Q(white)), Square(
        Pawn_Q(white)), Square(Pawn_Q(white)), Square(Pawn_Q(white))],
    [Square(Right(white)), Square(Bishop(white)),  Square(
        King(white)), Square(Queen(white)), Square(Knight(white))],
]

sample1 = [
    [Square(Right(black)), Square(Queen(black)), Square(King(black)),
     Square(Knight(black)), Square(Bishop(black))],
    [Square(Pawn_Q(black)), Square(Pawn_Q(black)), Square(
        Pawn_Q(black)), Square(Pawn_Q(black)), Square(Pawn_Q(black))],
    [Square(), Square(), Square(), Square(), Square()],
    [Square(Pawn_Q(white)), Square(Pawn_Q(white)), Square(
        Pawn_Q(white)), Square(Pawn_Q(white)), Square(Pawn_Q(white))],
    [Square(Bishop(white)), Square(Knight(white)),  Square(
        King(white)), Square(Queen(white)), Square(Right(white))],
]

sample_tactics = [
    # 0_x     1_x      2_x                 3_x      4_x
    [Square(), Square(), Square(King(black)), Square(), Square()],            # 0_y
    [Square(), Square(), Square(Queen(black)),
     Square(), Square()],            # 1_y
    [Square(), Square(Pawn_Q(black)), Square(),
     Square(), Square()],            # 2_y
    [Square(), Square(), Square(), Square(Knight(white)), Square()],           # 3_y
    [Square(), Square(), Square(King(white)), Square(), Square()],             # 4_y
]


sample_mvvlva_test = [
    # 0_y (Row 0) -- Black King added at (0,2)
    [Square(), Square(), Square(King(black)), Square(), Square()],

    # 1_y (Row 1)
    [Square(), Square(), Square(), Square(), Square()],

    # 2_y: Victims Row: Black Pawn (2,1) and Black Queen (2,2)
    [Square(), Square(Pawn_Q(black)), Square(Queen(black)), Square(), Square()],

    # 3_y: Attackers Row: White Pawn (3,1) and White Queen (3,2)
    # Note: King is placed at (4,3) for legality
    [Square(), Square(Pawn_Q(white)), Square(Queen(white)), Square(), Square()],

    # 4_y (Row 4)
    [Square(), Square(), Square(), Square(King(white)), Square()],
]
