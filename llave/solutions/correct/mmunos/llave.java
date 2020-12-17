import java.util.*;
public class llave {

	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		int n = sc.nextInt();
		int m = sc.nextInt();
		int[] inicial = new int[n];
		int[] objetivo = new int[n];
		for(int i = 0; i < n; i++){
			inicial[i] = sc.nextInt();
		}
		for(int i = 0; i < n; i++){
			objetivo[i] = sc.nextInt();
		}
		if(check(inicial, objetivo, m)) System.out.println("si");
		else System.out.println("no");
	}
	static boolean check(int[] inicial, int[] objetivo, int m) {
		int n = inicial.length;
		int limar = 0;
		for(int i = 0; i < n; i++){
			if(inicial[i] < objetivo[i]) return false;
			else if(inicial[i] > objetivo[i]) limar++;
		}
		return limar <= m;
	}

}
