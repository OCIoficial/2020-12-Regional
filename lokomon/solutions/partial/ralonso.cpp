#include <cstdio>
#include <vector>

#define BLANK -1

using namespace std;

int main() {
    int n;

    scanf("%d", &n);

    vector<int> heights(n);
    for (int i, h = n; h > 0; h--) {
        scanf("%d", &i);
        heights[i] = h;
    }

    int top = 0;
    int bottom = 0;
    for (int i = 1; i < n; i++) {
        if (heights[top] < heights[i]) {
            top = i;
        }
        if (heights[bottom] > heights[i]) {
            bottom = i;
        }
    }

    int pos = top;
    while (true) {
        int lmax = BLANK;
        for (int i = pos - 1; i >= 0; i--) {
            if (heights[i] > heights[pos]) break;
            if (lmax == BLANK || heights[i] > heights[lmax]) lmax = i;
        }
        int rmax = BLANK;
        for (int i = pos + 1; i < n; i++) {
            if (heights[i] > heights[pos]) break;
            if (rmax == BLANK || heights[i] > heights[rmax]) rmax = i;
        }
        if (lmax == BLANK && rmax == BLANK) {
            break;
        }
        pos = heights[lmax] > heights[rmax] ? lmax : rmax;
    }
    
    printf("%d\n", pos);

    return 0;
}
