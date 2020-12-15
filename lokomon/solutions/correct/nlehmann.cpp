#include <algorithm>
#include <cstdio>
#include <vector>
using namespace std;

int main() {
  int n;
  scanf("%d", &n);

  int v, i;
  int l = 0, r = n - 1;
  scanf("%d", &i);
  for (int j = 1; j < n; ++j) {
    scanf("%d", &v);
    if (v > r || v < l) continue;
    if (v < i) {
      r = i;
    } else {
      l = i;
    }
    i = v;
  }

  printf("%d\n", i);
}