from enum import Enum
from typing import Generator, Iterable, List, Optional, Tuple
import sys

Color = Enum('Color', 'WHITE BLACK', start=0)
Piece = Enum('Piece', 'ROOK BISHOP QUEEN KING KNIGHT PAWN', start=0)
Square = Optional[Tuple[Color, Piece]]
Board = List[List[Square]]

ROOK_DIRECTIONS = (
    (+1, +0), (+0, +1),
    (+0, -1), (-1, +0),
)

BISHOP_DIRECTIONS = (
    (+1, -1), (+1, +1),
    (-1, -1), (-1, +1),
)

KNIGHT_MOVES = (
    (+2, +1),
    (+1, +2),
    (-1, +2),
    (-2, +1),
    (-2, -1),
    (-1, -2),
    (+1, -2),
    (+2, -1),
)

KING_MOVES = (
    (+1, -1), (+1, +0), (-1, +1),
    (+0, -1),           (+0, +1),
    (-1, -1), (-1, +0), (-1, +1),
)

PAWN_CAPTURES = (
    (-1, -1), (-1, 1)
)


def debug_board(board: Board) -> None:
    """Displays a board on stderr."""
    for i in range(8):
        for j in range(8):
            if board[i][j]:
                if board[i][j] == (Color.WHITE, Piece.KING):
                    print("♔", end="", file=sys.stderr)
                if board[i][j] == (Color.WHITE, Piece.QUEEN):
                    print("♕", end="", file=sys.stderr)
                if board[i][j] == (Color.WHITE, Piece.ROOK):
                    print("♖", end="", file=sys.stderr)
                if board[i][j] == (Color.WHITE, Piece.BISHOP):
                    print("♗", end="", file=sys.stderr)
                if board[i][j] == (Color.WHITE, Piece.KNIGHT):
                    print("♘", end="", file=sys.stderr)
                if board[i][j] == (Color.WHITE, Piece.PAWN):
                    print("♙", end="", file=sys.stderr)
                if board[i][j] == (Color.BLACK, Piece.KING):
                    print("♚", end="", file=sys.stderr)
                if board[i][j] == (Color.BLACK, Piece.QUEEN):
                    print("♛", end="", file=sys.stderr)
                if board[i][j] == (Color.BLACK, Piece.ROOK):
                    print("♜", end="", file=sys.stderr)
                if board[i][j] == (Color.BLACK, Piece.BISHOP):
                    print("♝", end="", file=sys.stderr)
                if board[i][j] == (Color.BLACK, Piece.KNIGHT):
                    print("♞", end="", file=sys.stderr)
                if board[i][j] == (Color.BLACK, Piece.PAWN):
                    print("♟", file=sys.stderr)
            else:
                print("+", end="", file=sys.stderr)
        print(file=sys.stderr)


def valid_coordinates(y: int, x: int) -> bool:
    """Returns whether a coordinate pair is a valid chess square."""
    return x in range(8) and y in range(8)


def is_white_king_in_check(board: Board) -> bool:
    """Returns whether the white king is in check in the given board."""
    x, y = -1, -1
    for i in range(8):
        for j in range(8):
            if board[i][j] == (Color.WHITE, Piece.KING):
                x = j
                break
        if board[i][x] == (Color.WHITE, Piece.KING):
            y = i

    for dy, dx in ROOK_DIRECTIONS:
        for i in range(1, 8):
            ty, tx = y + i * dy, x + i * dx
            if not valid_coordinates(ty, tx):
                break
            if board[ty][tx]:
                if (
                    board[ty][tx][0] == Color.BLACK
                    and board[ty][tx][1] in (Piece.ROOK, Piece.QUEEN)
                ):
                    return True
                else:
                    break
    for dy, dx in BISHOP_DIRECTIONS:
        for i in range(1, 8):
            ty, tx = y + i * dy, x + i * dx
            if not valid_coordinates(ty, tx):
                break
            if board[ty][tx]:
                if (
                    board[ty][tx][0] == Color.BLACK
                    and board[ty][tx][1] in (Piece.BISHOP, Piece.QUEEN)
                ):
                    return True
                else:
                    break

    for dy, dx in KNIGHT_MOVES:
        if (
            valid_coordinates(y + dy, x + dx)
            and board[y + dy][x + dx] == (Color.BLACK, Piece.KNIGHT)
        ):
            return True

    for dy, dx in KING_MOVES:
        if (
            valid_coordinates(y + dy, x + dx)
            and board[y + dy][x + dx] == (Color.BLACK, Piece.KING)
        ):
            return True

    for dy, dx in PAWN_CAPTURES:
        if (
            valid_coordinates(y - dy, x + dx)
            and board[y - dy][x + dx] == (Color.BLACK, Piece.PAWN)
        ):
            return True

    return False


def move(board: Board, sy: int, sx: int, ty: int, tx: int) -> None:
    """Mutates the board by moving the piece in sy, sx to ty, tx. Assumes the piece in (ty, tx), if any,
    has been already stored, and that the move is valid. """
    board[ty][tx] = board[sy][sx]
    board[sy][sx] = None


def undo(board: Board, sy: int, sx: int, ty: int, tx: int, captured: Square) -> None:
    """Undoes a move by moving the piece in ty, tx to sy, sx and returning the captured piece, if any, back to ty,
    tx. """
    board[sy][sx] = board[ty][tx]
    board[ty][tx] = captured


def get_moves_for_white_piece(board: Board, y: int, x: int, piece: Piece) -> Generator[Board, None, None]:
    """Returns a generator which yields boards representing all valid moves (but ignoring checks) for the piece in (
    y, x). """
    if piece in (Piece.ROOK, Piece.QUEEN):
        for dy, dx in ROOK_DIRECTIONS:
            for i in range(1, 8):
                ty, tx = y + i * dy, x + i * dx
                if not valid_coordinates(ty, tx):
                    break
                captured = board[ty][tx]
                if captured and captured[0] is Color.WHITE:
                    break
                move(board, y, x, ty, tx)
                yield board
                undo(board, y, x, ty, tx, captured)

                if captured:
                    break

    if piece in (Piece.BISHOP, Piece.QUEEN):
        for dy, dx in BISHOP_DIRECTIONS:
            for i in range(1, 8):
                ty, tx = y + i * dy, x + i * dx
                if not valid_coordinates(ty, tx):
                    break
                captured = board[ty][tx]
                if captured and captured[0] is Color.WHITE:
                    break
                move(board, y, x, ty, tx)
                yield board
                undo(board, y, x, ty, tx, captured)

                if captured:
                    break

    if piece is Piece.KNIGHT:
        for my, mx in KNIGHT_MOVES:
            ty, tx = y + my, x + mx
            if not valid_coordinates(ty, tx):
                continue

            captured = board[ty][tx]
            if captured and captured[0] is Color.WHITE:
                break
            move(board, y, x, ty, tx)
            yield board
            undo(board, y, x, ty, tx, captured)

    if piece is Piece.KING:
        for my, mx in KING_MOVES:
            ty, tx = y + my, x + mx
            if not valid_coordinates(ty, tx):
                continue

            captured = board[ty][tx]
            if captured and captured[0] is Color.WHITE:
                break
            move(board, y, x, ty, tx)
            yield board
            undo(board, y, x, ty, tx, captured)

    if piece is Piece.PAWN:
        for my, mx in PAWN_CAPTURES:
            ty, tx = y + my, x + mx
            if not valid_coordinates(ty, tx):
                continue

            captured = board[ty][tx]
            if captured and captured[0] is Color.WHITE:
                break
            move(board, y, x, ty, tx)
            yield board
            undo(board, y, x, ty, tx, captured)

        ty, tx = y + 1, x
        captured = board[ty][tx]
        if captured:
            return
        move(board, y, x, ty, tx)
        yield board
        undo(board, y, x, ty, tx, captured)


def solve(pieces: Iterable[Tuple[int, int, int, int]]) -> bool:
    """Resolves whether the given piece tuples represent black checkmating white or not."""
    board: Board = [[None for _ in range(8)] for _ in range(8)]

    for color, piece, y, x in pieces:
        board[y][x] = (Color(color), Piece(piece))

    debug_board(board)

    for color, piece, y, x in pieces:
        if Color(color) is Color.BLACK:
            continue

        boards = get_moves_for_white_piece(board, y, x, Piece(piece))

        if not all(map(is_white_king_in_check, boards)):
            return False

    return True


def main() -> None:
    """Solves the problem by parsing the input and calling solve(pieces)."""
    _ = int(input())
    pieces = (tuple(map(int, (line.split()))) for line in sys.stdin)

    # Here we assume the input matches the expected format.
    # noinspection PyTypeChecker
    print(1 if solve(pieces) else 0)


if __name__ == "__main__":
    main()
