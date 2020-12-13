#include <cstdio>
#include <vector>

using namespace std;

#define FINISH 0

int main() {
    int n;

    scanf("%d", &n);

    vector<int> heights(n + 2);
    heights[0] = heights[n + 1] = n + 1;
    for (int i, h = n; h > 0; h--) {
        scanf("%d", &i);
        heights[i + 1] = h;
    }

    // Next jump to each side
    vector<int> next_left(n + 2, FINISH);
    vector<int> next_right(n + 2, FINISH);

    vector<int> stack;

    stack.push_back(0);
    for (int i = 1; i <= n; i++) {
        while (heights[i] > heights[stack.back()]) {
            next_left[i] = stack.back();
            stack.pop_back();
        }
        stack.push_back(i);
    }
    stack.clear();

    stack.push_back(n + 1);
    for (int i = n; i >= 1; i--) {
        while (heights[i] > heights[stack.back()]) {
            next_right[i] = stack.back();
            stack.pop_back();
        }
        stack.push_back(i);
    }
    stack.clear();

    // Get starting mountain
    int top = 1;
    for (int i = 2; i <= n; i++) {
        if (heights[i] > heights[top]) {
            top = i;
        }
    }
    
    int pos;

    // Trick so we never jump to FINISH
    heights[FINISH] = 0;

    // Iterate until both sides are FINISH
    for (pos = top; next_left[pos] || next_right[pos]; ) {
        pos = heights[next_left[pos]] > heights[next_right[pos]] ? next_left[pos] : next_right[pos];
    }
    
    printf("%d\n", pos - 1);

    return 0;
}
