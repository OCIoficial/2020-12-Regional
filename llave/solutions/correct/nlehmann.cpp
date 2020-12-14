#include <cstdio>
#include <vector>

using namespace std;

int main() {
  int n, m;
  scanf("%d%d", &n, &m);

  vector<int> key(n);
  for (int i = 0; i < n; ++i) {
    scanf("%d", &key[i]);
  }
  int tot = 0;
  for (int i = 0; i < n; ++i) {
    int t = 0;
    scanf("%d", &t);
    if (t > key[i]) {
      printf("no\n");
      return 0;
    }
    tot += t < key[i];
  }
  printf(tot <= m ? "si\n" : "no\n");
}