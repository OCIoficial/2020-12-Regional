#include "testlib.h"

int main() {
  registerValidation();
  int n = inf.readInt(1, 100000);
  inf.readSpace();
  int x = inf.readInt(0, 1000000000);
  inf.readEoln();

  for (int i = 0; i < n; ++i) {
    if (i > 0) {
      inf.readSpace();
    }
    inf.readInt(1, 10000);
  }
  inf.readEoln();
  inf.readEof();
}
