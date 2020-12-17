import java.util.*;
import java.io.*;

class lokomon {
  public static void main(String[] args) throws Exception {
    BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
    int n = Integer.parseInt(in.readLine());
    StringTokenizer st = new StringTokenizer(in.readLine());
    int heights[] = new int[n + 2];
    heights[0] = heights[n + 1] = n + 1;
    for (int h = n; h > 0; h--) {
      heights[Integer.parseInt(st.nextToken()) + 1] = h;
    }

    int next_left[] = new int[n + 2];
    int next_right[] = new int[n + 2];

    Stack<Integer> stack = new Stack<>();
    stack.push(0);
    for (int i = 1; i <= n; ++i) {
      while (heights[i] > heights[stack.peek()]) {
        next_left[i] = stack.pop();
      }
      stack.push(i);
    }
    stack.clear();

    stack.push(n + 1);
    for (int i = n; i >= 1; i--) {
      while (heights[i] > heights[stack.peek()]) {
        next_right[i] = stack.pop();
      }
      stack.push(i);
    }
    stack.clear();

    int top = 1;
    for (int i = 2; i <= n; i++) {
      if (heights[i] > heights[top]) {
        top = i;
      }
    }
    int pos = top;
    heights[0] = 0;
    while (next_left[pos] > 0 || next_right[pos] > 0) {
      pos = heights[next_left[pos]] > heights[next_right[pos]] ? next_left[pos] : next_right[pos];
    }
    System.out.println(pos - 1);
  }
}