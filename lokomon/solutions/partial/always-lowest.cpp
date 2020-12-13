#include <cstdio>
#include <vector>

#define BLANK -1

using namespace std;

int main() {
    int n, i;

    scanf("%d", &n);

    vector<int> heights(n);
    for (int h = n; h > 0; h--) {
        scanf("%d", &i);
        heights[i] = h;
    }
    
    printf("%d\n", i);

    return 0;
}
