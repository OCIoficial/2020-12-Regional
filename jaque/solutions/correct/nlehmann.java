import java.io.*;
import java.util.*;

class jaque {
  static Pieza board[][] = new Pieza[8][8];

  public static void main(String[] args) throws Exception {
    for (int y = 0; y < 8; ++y) {
      for (int x = 0; x < 8; ++x) {
        board[y][x] = new Pieza(Color.Blank, Type.Empty);
      }
    }

    BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
    int n = Integer.parseInt(in.readLine());
    StringTokenizer st;
    for (int i = 0; i < n; ++i) {
      st = new StringTokenizer(in.readLine());
      int c = Integer.parseInt(st.nextToken());
      int p = Integer.parseInt(st.nextToken());
      int y = Integer.parseInt(st.nextToken());
      int x = Integer.parseInt(st.nextToken());
      board[y][x] = new Pieza(Color.values()[c], Type.values()[p]);
    }

    System.out.println(isCheckMate() ? "1" : "0");
  }

  static boolean isValid(int x, int y) {
    return y >= 0 && y < 8 && x >= 0 && x < 8;
  }

  static ArrayList<Pos> longMoves(Pos start, Color color, int dx[], int dy[]) {
    ArrayList<Pos> options = new ArrayList<>();
    for (int i = 0; i < dx.length; ++i) {
      int x = start.x + dx[i];
      int y = start.y + dy[i];
      while (isValid(x, y) && board[y][x].type == Type.Empty) {
        options.add(new Pos(x, y));
        x += dx[i];
        y += dy[i];
      }
      if (isValid(x, y) && board[y][x].color != color) {
        options.add(new Pos(x, y));
      }
    }
    return options;
  }

  static ArrayList<Pos> shortMoves(Pos start, Color color, int dx[], int dy[]) {
    ArrayList<Pos> options = new ArrayList<>();
    for (int i = 0; i < dx.length; ++i) {
      int x = start.x + dx[i];
      int y = start.y + dy[i];
      if (isValid(x, y) && board[y][x].color != color) {
        options.add(new Pos(x, y));
      }
    }
    return options;
  }

  static ArrayList<Pos> rookMoves(Pos start, Color color) {
    int dx[] = { -1, +1, +0, +0 };
    int dy[] = { +0, +0, -1, +1 };
    return longMoves(start, color, dx, dy);
  }

  static ArrayList<Pos> bishopMoves(Pos start, Color color) {
    int dx[] = { -1, +1, -1, +1 };
    int dy[] = { -1, -1, +1, +1 };
    return longMoves(start, color, dx, dy);
  }

  static ArrayList<Pos> queenMoves(Pos start, Color color) {
    int dx[] = { -1, +1, -1, +1, -1, +1, +0, +0 };
    int dy[] = { -1, -1, +1, +1, +0, +0, -1, +1 };
    return longMoves(start, color, dx, dy);
  }

  static ArrayList<Pos> knightMoves(Pos start, Color color) {
    int dx[] = { +2, +2, -2, -2, +1, +1, -1, -1 };
    int dy[] = { +1, -1, +1, -1, +2, -2, +2, -2 };
    return shortMoves(start, color, dx, dy);
  }

  static ArrayList<Pos> kingMoves(Pos start, Color color) {
    int dx[] = { -1, +1, -1, +1, -1, +1, +0, +0 };
    int dy[] = { -1, -1, +1, +1, +0, +0, -1, +1 };
    return shortMoves(start, color, dx, dy);
  }

  static ArrayList<Pos> pawnMoves(Pos start, Color color) {
    ArrayList<Pos> options = new ArrayList<>();
    Color otro = color == Color.Black ? Color.White : Color.Black;
    int y = start.y + (color == Color.Black ? 1 : -1);

    int dx[] = { -1, 1 };
    for (int i = 0; i < dx.length; ++i) {
      int x = start.x + dx[i];
      if (isValid(x, y) && board[y][x].color == otro) {
        options.add(new Pos(x, y));
      }
    }
    if (isValid(start.x, y) && board[y][start.x].type == Type.Empty) {
      options.add(new Pos(start.x, y));
    }
    return options;
  }

  static Pos findWhiteKing() {
    for (int y = 0; y < 8; ++y) {
      for (int x = 0; x < 8; ++x) {
        if (board[y][x].type == Type.King && board[y][x].color == Color.White) {
          return new Pos(x, y);
        }
      }
    }
    // this should be unreacheable
    return new Pos(0, 0);
  }

  static ArrayList<Pos> moves(Pos pos) {
    Color c = board[pos.y][pos.x].color;
    switch (board[pos.y][pos.x].type) {
      case Bishop:
        return bishopMoves(pos, c);
      case Knight:
        return knightMoves(pos, c);
      case Pawn:
        return pawnMoves(pos, c);
      case Queen:
        return queenMoves(pos, c);
      case King:
        return kingMoves(pos, c);
      case Rook:
        return rookMoves(pos, c);
      default:
        return new ArrayList<>();
    }
  }

  static boolean isCheck() {
    Pos wk = findWhiteKing();
    for (int y = 0; y < 8; ++y) {
      for (int x = 0; x < 8; ++x) {
        if (board[y][x].color == Color.Black) {
          for (Pos p : moves(new Pos(x, y))) {
            if (p.compareTo(wk) == 0) {
              return true;
            }
          }
        }
      }
    }
    return false;
  }

  static boolean isCheckMate() {
    HashMap<Pos, ArrayList<Pos>> whiteOptions = new HashMap<>();
    for (int y = 0; y < 8; ++y) {
      for (int x = 0; x < 8; ++x) {
        if (board[y][x].color == Color.White) {
          Pos start = new Pos(x, y);
          whiteOptions.put(start, moves(start));
        }
      }
    }
    for (Pos start : whiteOptions.keySet()) {
      Pieza pieza = board[start.y][start.x];
      Pieza empty = new Pieza(Color.Blank, Type.Empty);
      for (Pos target : whiteOptions.get(start)) {
        Pieza t = board[target.y][target.x];
        board[target.y][target.x] = pieza;
        board[start.y][start.x] = empty;
        if (!isCheck()) {
          return false;
        }
        board[target.y][target.x] = t;
        board[start.y][start.x] = pieza;
      }
    }
    return true;
  }
}

enum Color {
  White, Black, Blank
};

enum Type {
  Rook, Bishop, Queen, King, Knight, Pawn, Empty;
};

class Pos implements Comparable<Pos> {
  int x;
  int y;

  @Override
  public int compareTo(Pos rhs) {
    if (x != rhs.x)
      return x - rhs.x;
    return y - rhs.y;
  }

  @Override
  public String toString() {
    return "(" + x + ", " + y + ")";
  }

  public Pos(int x, int y) {
    this.x = x;
    this.y = y;
  }
}

class Pieza {
  Color color;
  Type type;

  public Pieza(Color color, Type type) {
    this.color = color;
    this.type = type;
  }

  public String toString() {
    return type + "" + color;
  }
}
