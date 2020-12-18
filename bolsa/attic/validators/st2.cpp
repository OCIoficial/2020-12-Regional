#include "testlib.h"

int main() {
  registerValidation();
  int n = inf.readInt(1, 1000);
  inf.readSpace();
  int x = inf.readInt(0, 1000);
  inf.readEoln();

  for (int i = 0; i < n; ++i) {
    if (i > 0) {
      inf.readSpace();
    }
    inf.readInt(1, 1000);
  }
  inf.readEoln();
  inf.readEof();
}
