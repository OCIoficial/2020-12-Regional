#include <cstdio>

int main() {
    int n, x, i, sum = 0;
    bool possible = false;

    scanf("%d%d", &n, &x);

    while (n-- > 0) {
        scanf("%d", &i);
        if (i > x) {
            continue;
        }
        if (2 * i >= x) {
            possible = true;
            break;
        }
        sum += i;
    }
    if (2 * sum >= x) possible = true;

    printf("%d\n", possible ? 1 : 0);

    return 0;
}
