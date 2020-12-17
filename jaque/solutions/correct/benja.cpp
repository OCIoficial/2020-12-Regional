#include <iostream>
#include <vector>
#include <algorithm>
#include <map>
#include <utility>

using namespace std;

enum Color {Blanco = 0, Negro = 1, Nada = 2};
enum Tipo {Torre = 0, Alfil = 1, Reina = 2, Rey = 3, Caballo = 4, Peon = 5, Vacia = 6};
struct Pos {
    int y;
    int x;

    bool operator==(const Pos a) const {
        return a.x == x && a.y == y;
    }

    bool operator<(const Pos a) const {
        return make_pair(y, x) < make_pair(a.y, a.x);
    }
};
struct Pieza {
    Color color;
    Tipo tipo;
};



vector<vector<Pieza>> board(8, vector<Pieza>(8));

bool isValid(Pos pos) {
    return pos.y >= 0 && pos.y < 8 && pos.x >= 0 && pos.x < 8;
}

vector<Pos> torreMoves(Pos start, Color color) {
    vector<Pos> options;
    Color otro = color == Negro ? Blanco : Negro;
    // top
    for (int i = start.y - 1; i >= 0; i--) {
        if (board[i][start.x].tipo != Vacia) {
            if (board[i][start.x].color == otro) {
                options.push_back(Pos{i, start.x});
            }
            break;
        }
        options.push_back(Pos{i, start.x});
    }
    // down
    for (int i = start.y + 1; i < 8; i++) {
        if (board[i][start.x].tipo != Vacia) {
            if (board[i][start.x].color == otro) {
                options.push_back(Pos{i, start.x});
            }
            break;
        }
        options.push_back(Pos{i, start.x});
    }
    // right
    for (int i = start.x + 1; i < 8; i++) {
        if (board[start.y][i].tipo != Vacia) {
            if (board[start.y][i].color == otro) {
                options.push_back(Pos{start.y, i});
            }
            break;
        }
        options.push_back(Pos{start.y, i});
    }
    // left
    for (int i = start.x - 1; i >= 0; i--) {
        if (board[start.y][i].tipo != Vacia) {
            if (board[start.y][i].color == otro) {
                options.push_back(Pos{start.y, i});
            }
            break;
        }
        options.push_back(Pos{start.y, i});
    }
    return options;
}

void alfilCheckAndAdd(vector<Pos>& options, vector<bool>& valid, Pos next, int idx, Color otro) {
    if (!isValid(next)) {
        valid[idx] = false;
    }
    else if (board[next.y][next.x].tipo != Vacia) {
        if (board[next.y][next.x].color == otro) {
            options.push_back(next);
        }
        valid[idx] = false;
    }
    else {
        options.push_back(next);
    }
}

vector<Pos> alfilMoves(Pos start, Color color) {
    Color otro = color == Negro ? Blanco : Negro;
    vector<Pos> options;
    vector<bool> valid = {true, true, true, true};
    for (int i = 1; i < 8; i++) {
        // Diagonal 1 -- arriba a la derecha
        if (valid[0]) {
            Pos next = Pos{start.y - i, start.x + i};            
            alfilCheckAndAdd(options, valid, next, 0, otro);
        }
        // Diagonal 2 -- arriba a la izquierda
        if (valid[1]) {
            Pos next = Pos{start.y - i, start.x - i};            
            alfilCheckAndAdd(options, valid, next, 1, otro);
        }

        // Diagonal 3 -- abajo a la izquierda
        if (valid[2]) {
            Pos next = Pos{start.y + i, start.x - i};            
            alfilCheckAndAdd(options, valid, next, 2, otro);
        }

        // Diagonal 4 -- abajo a la derecha
        if (valid[3]) {
            Pos next = Pos{start.y + i, start.x + i};            
            alfilCheckAndAdd(options, valid, next, 3, otro);
        }
    }
    return options;
}

vector<Pos> reinaMoves(Pos start, Color color) {
    auto torreOptions = torreMoves(start, color);
    auto alfilOptions = alfilMoves(start, color);
    torreOptions.insert(torreOptions.end(), alfilOptions.begin(), alfilOptions.end());
    return torreOptions;
}

vector<Pos> caballoMoves(Pos start, Color color) {
    vector<Pos> options;
    vector<Pos> maybe = {
               Pos{start.y - 2, start.x - 1},
               Pos{start.y - 2, start.x + 1},
               Pos{start.y + 2, start.x - 1},
               Pos{start.y + 2, start.x + 1},
               Pos{start.y - 1, start.x - 2},
               Pos{start.y + 1, start.x - 2},
               Pos{start.y - 1, start.x + 2},
               Pos{start.y + 1, start.x + 2}};
    for (auto option : maybe) {
        if (isValid(option)) {
            if (board[option.y][option.x].color != color) {
                options.push_back(option);
            }
        }
    }
    return options;
}

vector<Pos> reyMoves(Pos start, Color color) {
    vector<Pos> options;
    vector<int> moves = {-1, 0, 1};
    for (int i : moves) {
        for (int j : moves) {
            if (i == 0 && j == 0) {
                continue;
            }
            Pos option = Pos{start.y + i, start.x + j};
            if (isValid(option)) {
                if (board[option.y][option.x].color != color) {
                    options.push_back(option);
                }
            }
        }
    }
    return options;
}

vector<Pos> peonMoves(Pos start, Color color) {
    vector<Pos> options;
    int yOff = 0;
    Color otro;
    if (color == Negro) {
        yOff = 1;
        otro = Blanco;
    }
    else {
        yOff = -1;
        otro = Negro;
    }
    // Ataque
    Pos op1 = Pos{start.y + yOff, start.x + 1};
    Pos op2 = Pos{start.y + yOff, start.x - 1};
    if (isValid(op1)) {
        if (board[op1.y][op1.x].color == otro) {
            options.push_back(op1); 
        }
    }
    if (isValid(op2)) {
        if (board[op2.y][op2.x].color == otro) {
            options.push_back(op2); 
        }
    }
    // Frente
    Pos op3 = Pos{start.y + yOff, start.x};
    if (isValid(op3)) {
        if (board[op3.y][op3.x].tipo == Vacia) {
            options.push_back(op3); 
        }
    }
    return options;
}

Pos findWhiteKing() {
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            if (board[i][j].tipo == Rey && board[i][j].color == Blanco) {
                return Pos{i, j};
            }
        }
    }
    // Shouldn't get here
    return Pos{0, 0};
}

bool isCheck() {
    Pos whiteKing = findWhiteKing();
    vector<Pos> blackOptions;
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            Pos start = Pos{i, j};
            if (board[i][j].color == Negro) {
                vector<Pos> moves;
                if (board[i][j].tipo == Torre) {
                    moves = torreMoves(start, Negro);
                }
                else if (board[i][j].tipo == Alfil) {
                    moves = alfilMoves(start, Negro);
                }
                else if (board[i][j].tipo == Reina) {
                    moves = reinaMoves(start, Negro);
                }
                else if (board[i][j].tipo == Caballo) {
                    moves = caballoMoves(start, Negro);
                }
                else if (board[i][j].tipo == Rey) {
                    moves = reyMoves(start, Negro);
                }
                else if (board[i][j].tipo == Peon) {
                    moves = peonMoves(start, Negro);
                }
                blackOptions.insert(blackOptions.end(), moves.begin(), moves.end());
            }
        }
    }

    return find(blackOptions.begin(), blackOptions.end(), whiteKing) != blackOptions.end();
}

bool tryAll() {
    map<Pos, vector<Pos>> whiteOptions;

    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            Pos start = Pos{i, j};
            if (board[i][j].color == Blanco) {
                vector<Pos> moves;
                if (board[i][j].tipo == Torre) {
                    moves = torreMoves(start, Blanco);
                }
                else if (board[i][j].tipo == Alfil) {
                    moves = alfilMoves(start, Blanco);
                }
                else if (board[i][j].tipo == Reina) {
                    moves = reinaMoves(start, Blanco);
                }
                else if (board[i][j].tipo == Rey) {
                    moves = reyMoves(start, Blanco);
                }
                else if (board[i][j].tipo == Caballo) {
                    moves = caballoMoves(start, Blanco);
                }
                else if (board[i][j].tipo == Peon) {
                    moves = peonMoves(start, Blanco);
                }
                whiteOptions[start] = moves;
            }
        }
    }

    for (const auto& elem : whiteOptions) {
        auto start = elem.first;
        const auto& options = elem.second; 
        
        auto pieza = board[start.y][start.x];
        Pieza empty = Pieza{Nada, Vacia};
        for (const auto& move : options) {
            auto old = board[move.y][move.x];
            board[move.y][move.x] = pieza;
            board[start.y][start.x] = Pieza{Nada, Vacia};
            if (!isCheck()) {
                // cout << "y: " << move.y << " x: " << move.x << endl;
                // cout << "old y: " << start.y << " x: " << start.x << endl;
                // cout << "pieza: " << pieza.tipo << endl; 
                return true;
            }
            board[move.y][move.x] = old;
            board[start.y][start.x] = pieza;
        }
    }

    return false;
}

void initBoard() {
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            board[i][j] = Pieza{Nada, Vacia};
        }
    }
}

int main() {
    initBoard();
    int n;
    cin >> n;
    for (int i = 0; i < n; i++) {
        int c, p, y, x;
        cin >> c >> p >> y >> x;
        board[y][x] = Pieza{(Color)c, (Tipo)p};
    }
    if (tryAll()) {
        cout << "0\n";
    }
    else {
        cout << "1\n";
    }
    return 0;
}
