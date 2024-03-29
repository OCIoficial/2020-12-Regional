#include "testlib.h"
#include <utility>
#include <array>

using namespace std;

typedef array<pair<int, int>, 8> Rank;
typedef array<Rank, 8> Board;

enum Color { white, black };
enum Piece { rook, bishop, queen, king, knight, pawn };

const pair<int, int> BLANK = make_pair(-1, -1);

const int ROOK_DIRECTIONS[][2] = {
    {+1, +0}, {+0, +1},
    {+0, -1}, {-1, +0},
};

const int BISHOP_DIRECTIONS[][2] = {
    {+1, -1}, {+1, +1},
    {-1, -1}, {-1, +1},
};

const int KNIGHT_MOVES[][2] = {
    {+2, +1},
    {+1, +2},
    {-1, +2},
    {-2, +1},
    {-2, -1},
    {-1, -2},
    {+1, -2},
    {+2, -1},
};

const int KING_MOVES[][2] = {
    {+1, -1}, {+1, +0}, {+1, +1},
    {+0, -1},           {+0, +1},
    {-1, -1}, {-1, +0}, {-1, +1},
};

const int PAWN_CAPTURES[][2] = {
    {-1, -1}, {-1, 1},
};

const int PAWN_MOVES[][2] = {
    {-1, 0},
};

int countPiece(Board board, int color, int piece) {
    int count = 0;
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            if (board[i][j].first == color && board[i][j].second == piece) count++;
        }
    }
    return count;
}

int countColor(Board board, int color) {
    int count = 0;
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            if (board[i][j].first == color) count++;
        }
    }
    printf("%d\n", count);
    return count;
}

bool valid_coordinates(int y, int x) {
    return 0 <= y && y <= 7 && 0 <= x && x <= 7;
}

int numChecks(Board board, int color) {
    int ky, kx;
    bool found = false;
    for (ky = 0; ky < 8; ky++) {
        for (kx = 0; kx < 8; kx++) {
            if (board[ky][kx].first == color && board[ky][kx].second == king) {
                found = true;
                break;
            }
        }
        if (found) break;
    }

    int count = 0;

    for (auto direction: ROOK_DIRECTIONS) {
        int dy = direction[0], dx = direction[1];
        for (int ty = ky + dy, tx = kx + dx; ; ty += dy, tx += dx) {
            if (!valid_coordinates(ty, tx)) break;
            if (board[ty][tx] == BLANK) continue;
            if (board[ty][tx].first == !color && (board[ty][tx].second == rook || board[ty][tx].second == queen))
                count++;
            break;
        }
    }

    for (auto direction: BISHOP_DIRECTIONS) {
        int dy = direction[0], dx = direction[1];
        for (int ty = ky + dy, tx = kx + dx; ; ty += dy, tx += dx) {
            if (!valid_coordinates(ty, tx)) break;
            if (board[ty][tx] == BLANK) continue;
            if (board[ty][tx].first == !color && (board[ty][tx].second == bishop || board[ty][tx].second == queen))
                count++;
            break;
        }
    }

    for (auto move: KNIGHT_MOVES) {
        int ty = ky + move[0], tx = kx + move[1];
        if (valid_coordinates(ty, tx) && board[ty][tx].first == 1 - color && board[ty][tx].second == knight)
            count++;
    }

    for (auto move: KING_MOVES) {
        int ty = ky + move[0], tx = kx + move[1];
        if (valid_coordinates(ty, tx) && board[ty][tx].first == 1 - color && board[ty][tx].second == king)
            count++;
    }

    for (auto move: PAWN_CAPTURES) {
        int ty = ky + (color ? -move[0] : move[0]), tx = kx + move[1];
        if (valid_coordinates(ty, tx) && board[ty][tx].first == 1 - color && board[ty][tx].second == pawn)
            count++;
    }

    return count;
}

int main() {
    registerValidation();
    Board board = {};
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            board[i][j] = make_pair(-1, -1);
        }
    }

    int N = inf.readInt(2, 32, "N");
    inf.readEoln();

    for (int i = 0; i < N; i++) {
        int C = inf.readInt(0, 1, "C");
        inf.readSpace();
        int P = inf.readInt(0, 5, "P");
        inf.readSpace();
        int Y = inf.readInt(0, 7, "Y");
        inf.readSpace();
        int X = inf.readInt(0, 7, "X");
        inf.readEoln();
        ensuref(board[Y][X] == BLANK, "No puede haber dos piezas en la misma posición (%d, %d).", Y, X);
        board[Y][X] = make_pair(C, P);
    }

    ensuref(countPiece(board, white, king) == 1, "Debe haber exactamente un rey blanco.");
    ensuref(numChecks(board, white) > 1, "El rey blanco debe estar en jaque múltiple.");

    ensuref(countPiece(board, black, king) == 1, "Debe haber exactamente un rey negro.");
    ensuref(numChecks(board, black) == 0, "El rey negro no debe estar en jaque.");

    ensuref(countPiece(board, white, queen) <= 1, "Debe haber a lo más una reina blanca.");
    ensuref(countPiece(board, white, rook) <= 2, "Debe haber a lo más dos torres blancas.");
    ensuref(countPiece(board, white, bishop) <= 2, "Debe haber a lo más dos alfiles blancos.");
    ensuref(countPiece(board, white, knight) <= 2, "Debe haber a lo más dos caballos blancos.");
    ensuref(countPiece(board, white, pawn) <= 8, "Debe haber a lo más ocho peones blancos.");

    ensuref(countPiece(board, black, queen) <= 1, "Debe haber a lo más una reina negra.");
    ensuref(countPiece(board, black, rook) <= 2, "Debe haber a lo más dos torres negras.");
    ensuref(countPiece(board, black, bishop) <= 2, "Debe haber a lo más dos alfiles negros.");
    ensuref(countPiece(board, black, knight) <= 2, "Debe haber a lo más dos caballos negros.");
    ensuref(countPiece(board, black, pawn) <= 8, "Debe haber a lo más ocho peones negros.");

    inf.readEof();
}
