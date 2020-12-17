#include <cstdio>

int main() {
    int n, x;
    scanf("%d%d", &n, &x);
    float xhalf = x / 2.0;
    int tot = 0;
    for (int i = 0; i < n; ++i) {
        int a;
        scanf("%d", &a);
        if (a > x) continue;
        if (a >= xhalf) {
            printf("1\n");
            return 0;
        }
        tot += a;
    }
    printf(tot >= xhalf ? "1\n" : "0\n");
    return 0;
}
