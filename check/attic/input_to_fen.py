#!/bin/python3

from enum import Enum
from typing import Iterable, List, Optional, Tuple
import sys

Color = Enum('Color', 'WHITE BLACK', start=0)
Piece = Enum('Piece', 'ROOK BISHOP QUEEN KING KNIGHT PAWN', start=0)
Square = Optional[Tuple[Color, Piece]]
Board = List[List[Square]]


def get_fen(board: Board) -> str:
    ranks = []
    for i in range(8):
        rank = []
        count = 0
        for j in range(8):
            if board[i][j]:
                if count:
                    rank.append(str(count))
                    count = 0
                if board[i][j] == (Color.WHITE, Piece.KING):
                    rank.append("K")
                if board[i][j] == (Color.WHITE, Piece.QUEEN):
                    rank.append("Q")
                if board[i][j] == (Color.WHITE, Piece.ROOK):
                    rank.append("R")
                if board[i][j] == (Color.WHITE, Piece.BISHOP):
                    rank.append("B")
                if board[i][j] == (Color.WHITE, Piece.KNIGHT):
                    rank.append("N")
                if board[i][j] == (Color.WHITE, Piece.PAWN):
                    rank.append("P")
                if board[i][j] == (Color.BLACK, Piece.KING):
                    rank.append("k")
                if board[i][j] == (Color.BLACK, Piece.QUEEN):
                    rank.append("q")
                if board[i][j] == (Color.BLACK, Piece.ROOK):
                    rank.append("r")
                if board[i][j] == (Color.BLACK, Piece.BISHOP):
                    rank.append("b")
                if board[i][j] == (Color.BLACK, Piece.KNIGHT):
                    rank.append("n")
                if board[i][j] == (Color.BLACK, Piece.PAWN):
                    rank.append("p")
            else:
                count += 1
        if count:
            rank.append(str(count))
            count = 0
        ranks.append(''.join(rank))
    return '/'.join(ranks) + ' w - - 0 1'


def solve(pieces: Iterable[Tuple[int, int, int, int]]) -> str:
    board: Board = [[None for _ in range(8)] for _ in range(8)]

    for color, piece, y, x in pieces:
        board[y][x] = (Color(color), Piece(piece))

    return get_fen(board)


def main() -> None:
    _ = int(input())
    pieces = (tuple(map(int, (line.split()))) for line in sys.stdin)

    print(solve(pieces))


if __name__ == "__main__":
    main()
