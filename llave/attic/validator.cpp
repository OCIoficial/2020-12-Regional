#include <array>
#include <utility>

#include "testlib.h"

int main() {
  registerValidation();

  int N = inf.readInt(1, 100, "N");
  inf.readSpace();
  int M = inf.readInt(0, N, "M");
  inf.readEoln();

  for (auto _ : {1, 2}) {
    for (int i = 0; i < N; ++i) {
      if (i > 0) {
        inf.readSpace();
      }
      inf.readInt(1, 10, "vec[i]");
    }
    inf.readEoln();
  }

  inf.readEof();
}