#include "testlib.h"
#include <vector>

using namespace std;

int main() {
    registerValidation();
    
    int n = inf.readInt(2, 1_000_000, "n");
    vector<bool> positions(n, false);
    inf.readEoln();

    for (int h = n - 1; h >= 0; h--) {
        int position = inf.readInt(0, n - 1, "i");

        ensuref(!positions[position], "Montaña de altura %d en posición %d ya ocupada.", h, position);
        positions[position] = true;

        if (h) inf.readSpace();
        else inf.readEoln();
    }

    inf.readEof();
}
