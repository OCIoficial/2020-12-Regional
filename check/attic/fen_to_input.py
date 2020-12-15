#!/bin/python3

from enum import Enum
from typing import List, Tuple

Color = Enum('Color', 'WHITE BLACK', start=0)
Piece = Enum('Piece', 'ROOK BISHOP QUEEN KING KNIGHT PAWN', start=0)


def solve(fen: str) -> List[Tuple[Color, Piece, int, int]]:
    piece_map = {
        "K": (Color.WHITE, Piece.KING),
        "Q": (Color.WHITE, Piece.QUEEN),
        "R": (Color.WHITE, Piece.ROOK),
        "B": (Color.WHITE, Piece.BISHOP),
        "N": (Color.WHITE, Piece.KNIGHT),
        "P": (Color.WHITE, Piece.PAWN),
        "k": (Color.BLACK, Piece.KING),
        "q": (Color.BLACK, Piece.QUEEN),
        "r": (Color.BLACK, Piece.ROOK),
        "b": (Color.BLACK, Piece.BISHOP),
        "n": (Color.BLACK, Piece.KNIGHT),
        "p": (Color.BLACK, Piece.PAWN),
    }
    y = 0
    x = 0
    pieces = []
    for c in fen:
        if c in piece_map:
            pieces.append((*piece_map[c], y, x))
            x += 1
        elif c == '/':
            assert x == 8
            y += 1
            x = 0
            continue
        else:
            x += int(c)

    assert y == 7
    assert x == 8

    return pieces


def main() -> None:
    fen = input().split()[0]
    
    pieces = solve(fen)
    
    print(len(pieces))
    
    for color, piece, y, x in pieces:
        print(f"{color.value} {piece.value} {y} {x}")


if __name__ == "__main__":
    main()
