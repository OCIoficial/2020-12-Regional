#include <cstdio>
#include <array>
#include <vector>

using namespace std;

#define DEBUG

#define BLACK_SQUARE "\033[37;40m"
#define WHITE_SQUARE "\033[30;47m"
#define RESET "\033[0m"

#define GET_COLOR(item) (item & 0x18)
#define GET_PIECE(item) (item & 0x07)

typedef array<int, 8> Rank;
typedef array<Rank, 8> Board;

enum Color { white = 16, black = 24 };
enum Piece { rook, bishop, queen, king, knight, pawn };

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
    {+1, -1},           {+1, +1},
    {+0, -1},           {+0, +1},
    {-1, -1}, {-1, +0}, {-1, +1},
};

const int PAWN_CAPTURES[][2] = {
    {-1, -1}, {-1, 1},
};

const int PAWN_MOVES[][2] = {
    {-1, 0},
};


/**
    Displays a board on stderr.
*/
void debug_board(Board board) {
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            bool is_white_square = i % 2 == j % 2;
            fprintf(stderr, is_white_square ? WHITE_SQUARE : BLACK_SQUARE);
            switch (board[i][j]) {
                case 0: fprintf(stderr, " "); break;
                case white | rook: fprintf(stderr, is_white_square ? "♖" : "♜"); break;
                case black | rook: fprintf(stderr, is_white_square ? "♜" : "♖"); break;
                case white | bishop: fprintf(stderr, is_white_square ? "♗" : "♝"); break;
                case black | bishop: fprintf(stderr, is_white_square ? "♝" : "♗"); break;
                case white | queen: fprintf(stderr, is_white_square ? "♕" : "♛"); break;
                case black | queen: fprintf(stderr, is_white_square ? "♛" : "♕"); break;
                case white | king: fprintf(stderr, is_white_square ? "♔" : "♚"); break;
                case black | king: fprintf(stderr, is_white_square ? "♚" : "♔"); break;
                case white | knight: fprintf(stderr, is_white_square ? "♘" : "♞"); break;
                case black | knight: fprintf(stderr, is_white_square ? "♞" : "♘"); break;
                case white | pawn: fprintf(stderr, is_white_square ? "♙" : "♟"); break;
                case black | pawn: fprintf(stderr, is_white_square ? "♟" : "♙"); break;
                default: fprintf(stderr, "?"); break;
            }
        }
        fprintf(stderr, "%s\n", RESET);
    }
    fprintf(stderr, "\n");
}


/**
    Returns whether a coordinate pair is a valid chess square.
*/
bool valid_coordinates(int y, int x) {
    return 0 <= y && y <= 7 && 0 <= x && x <= 7;
}


/**
    Returns whether the white king is in check in the given board.
*/
bool is_white_king_in_check(Board board) {
    // Find white king
    int ky, kx;
    bool found = false;
    for (ky = 0; ky < 8; ky++) {
        for (kx = 0; kx < 8; kx++) {
            if (board[ky][kx] == (white | king)) {
                found = true;
                break;
            }
        }
        if (found) break;
    }

//     #ifdef DEBUG
//     fprintf(stderr, "Checking if K%c%d is in mate...\n", 'h' - ky, kx + 1);
//     debug_board(board);
//     #endif

    for (auto direction: ROOK_DIRECTIONS) {
        int dy = direction[0], dx = direction[1];
        for (int ty = ky + dy, tx = kx + dx; ; ty += dy, tx += dx) {
            if (!valid_coordinates(ty, tx)) break;
            if (!board[ty][tx]) continue;
            if (
                board[ty][tx] == (black | rook) || 
                board[ty][tx] == (black | queen)
            ) return true;
            else break;
        }
    }

    for (auto direction: BISHOP_DIRECTIONS) {
        int dy = direction[0], dx = direction[1];
        for (int ty = ky + dy, tx = kx + dx; ; ty += dy, tx += dx) {
            if (!valid_coordinates(ty, tx)) break;
            if (!board[ty][tx]) continue;
            if (
                board[ty][tx] == (black | bishop) || 
                board[ty][tx] == (black | queen)
            ) return true;
            else break;
        }
    }

    for (auto move: KNIGHT_MOVES) {
        int ty = ky + move[0], tx = kx + move[1];
        if (valid_coordinates(ty, tx) && board[ty][tx] == (black | knight)) return true;
    }

    for (auto move: KING_MOVES) {
        int ty = ky + move[0], tx = kx + move[1];
        if (valid_coordinates(ty, tx) && board[ty][tx] == (black | king)) return true;
    }

    for (auto move: PAWN_CAPTURES) {
        int ty = ky + move[0], tx = kx + move[1];
        if (valid_coordinates(ty, tx) && board[ty][tx] == (black | pawn)) return true;
    }

    return false;
}


/**
    Returns whether the white king is in check if the move (y, x) -> (ty, tx) is made.
*/
bool is_next_move_white_king_in_check(Board board, int y, int x, int ty, int tx) {
    int captured = board[ty][tx];
    board[ty][tx] = board[y][x];
    board[y][x] = 0;

    bool result = is_white_king_in_check(board);

    board[y][x] = board[ty][tx];
    board[ty][tx] = captured;

    return result;
}


/**
    Returns whether the piece at (y, x) can stop the white king from being in check by moving in the direction given by (my, mx).
*/
bool is_move_in_check(Board board, int y, int x, int my, int mx) {
    int ty = y + my;
    int tx = x + mx;
    if (!valid_coordinates(ty, tx)) return true;
    int captured = board[ty][tx];
    if (GET_COLOR(captured) == white) return true;
    return is_next_move_white_king_in_check(board, y, x, ty, tx);
}


/**
    Returns whether the piece at (y, x) can stop the white king from being in check by moving in the direction given by (dy, dx).
*/
bool is_direction_in_check(Board board, int y, int x, int dy, int dx) {
    for (int ty = y + dy, tx = x + dx; ; ty += dy, tx += dx) {
        if (!valid_coordinates(ty, tx)) return true;
        int captured = board[ty][tx];
        if (GET_COLOR(captured) == white) return true;
        if (!is_next_move_white_king_in_check(board, y, x, ty, tx)) return false;
        if (captured) return true;
    }
}


/**
    Returns whether the piece at (y, x) can stop the white king from being in check.
*/
bool can_avoid_check(Board board, int y, int x) {
    switch (GET_PIECE(board[y][x])) {
        case rook:
        case queen:
            for (auto direction: ROOK_DIRECTIONS) {
                if (!is_direction_in_check(board, y, x, direction[0], direction[1])) return true;
            }
            if (GET_PIECE(board[y][x]) == rook) break;
        case bishop:
            for (auto direction: BISHOP_DIRECTIONS) {
                if (!is_direction_in_check(board, y, x, direction[0], direction[1])) return true;
            }
            break;
        case knight:
            for (auto move: KNIGHT_MOVES) {
                if (!is_move_in_check(board, y, x, move[0], move[1])) return true;
            }
            break;
        case king:
            for (auto move: KING_MOVES) {
                if (!is_move_in_check(board, y, x, move[0], move[1])) return true;
            }
            break;
        case pawn:
            for (auto move: PAWN_CAPTURES) {
                int ty = y + move[0];
                int tx = x + move[1];
                if (valid_coordinates(ty, tx) && !board[ty][tx]) continue;
                if (!is_move_in_check(board, y, x, move[0], move[1])) return true;
            }
            for (auto move: PAWN_MOVES) {
                int ty = y + move[0];
                int tx = x + move[1];
                if (valid_coordinates(ty, tx) && board[ty][tx]) continue;
                if (!is_move_in_check(board, y, x, move[0], move[1])) return true;
            }
            break;
    }

    return false;
}


/**
    Resolves whether the given piece tuples represent black checkmating white or not.
*/
bool is_checkmate_over_white(vector< vector< int > > pieces) {
    Board board = {};

    for (auto props: pieces) {
        board[props[2]][props[3]] = 0x10 | (props[0] << 3) | props[1];
    }

    #ifdef DEBUG
    fprintf(stderr, "Checking if the following is checkmate:\n");
    debug_board(board);
    #endif

    for (auto props: pieces) {
        if (GET_COLOR(board[props[2]][props[3]]) == black) continue;

        if (can_avoid_check(board, props[2], props[3])) return false;
    }

    return true;
}


/**
    Solves the problem by parsing the input and calling bool is_checkmate_over_white(pieces).
*/
int main() {
    int n, c, p, y, x;
    scanf("%d", &n);

    vector< vector< int > > pieces(n, vector< int >(4));
    for (int i = 0; i < n; ++i) {
        scanf("%d%d%d%d", &(pieces[i][0]), &(pieces[i][1]), &(pieces[i][2]), &(pieces[i][3]));
    }

    printf("%d\n", is_checkmate_over_white(pieces) ? 1 : 0);

    return 0;
}
