import java.util.*;
public class bolsa {

	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		int n = sc.nextInt();
		long x = sc.nextLong();
		long tot = 0;
		long xhalf = x / 2 + x % 2;
		boolean done = false;
		for(int i = 0; i < n; i++){
			long a = sc.nextLong();
			if(a > x) continue;
			if(a >= xhalf) done = true;
			tot += a;
		}
		if(done) System.out.println(1);
		else {
			if(tot >= xhalf) System.out.println(1);
			else System.out.println(0);
		}
	}

}
