import java.util.*;
import java.io.*;

class lokomon {
  public static void main(String[] args) throws Exception {
    BufferedReader in = new BufferedReader(new InputStreamReader(System.in));

    int n = Integer.parseInt(in.readLine());
    StringTokenizer st = new StringTokenizer(in.readLine());

    int l = 0, r = n - 1;
    int i = Integer.parseInt(st.nextToken());
    for (int j = 1; j < n; ++j) {
      int v = Integer.parseInt(st.nextToken());
      if (v < l || r < v)
        continue;
      if (v < i)
        r = i;
      else
        l = i;
      i = v;
    }
    System.out.println(i);
  }
}
