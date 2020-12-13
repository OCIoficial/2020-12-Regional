#include<bits/stdc++.h>

using namespace std;

// Estructura
template<class T>
struct SegmentTree{
    vector<T>ST;
    int n;
    T (*merge)(int i, int l, int r, T a, T b);
    void build(int i, int l, int r, vector<T>&a){
        if (l==r){
            ST[i]=a[l];return;
        }

        build(i << 1, l, (l + r) >> 1, a);
        build(i << 1 | 1, (l + r) / 2 + 1, r, a);
        ST[i] = merge(i, l, r, ST[i << 1], ST[i << 1 | 1]);
    }
    SegmentTree(vector<T>&a, T (*merge)(int i, int l, int r, T a, T b)) : merge(merge){
        n=a.size();
        ST.resize(4 * n + 5);
        build(1, 0, n - 1, a);
    }
    void setMerge(T (*_merge)(int i, int l, int r, T a, T b)){
        merge = _merge;
    }
    SegmentTree(){

    }
    void buildSegmentTree(vector<T> &a){
        n = a.size();
        ST.resize(4 * n + 5);
        build(1, 0, n - 1, a);
    }
    void update(int i, int l, int r, int pos, T val){
        if (r < pos or l > pos)
            return;
        if (l == r){
            ST[i] = val;
            return;
        }
        update(i << 1, l, (l + r) >> 1, pos, val);
        update(i << 1 | 1, (l + r) / 2 + 1, r, pos, val);
        ST[i]=merge(i, l, r, ST[i << 1], ST[i << 1 | 1]);
    }
    T query(int i, int l, int r, int a, int b){
        if (l >= a and r <= b)
            return ST[i];
        int mid = (l + r) >> 1;
        if (b <= mid)
            return query(i << 1, l, (l + r) >> 1, a, b);
        if (a > mid)
            return query(i << 1 | 1, (l + r) / 2 + 1, r, a, b);
        return merge(i, l, r, query(2*i, l, (l+r)/2, a, b), query(2*i+1, (l+r)/2+1, r, a, b));
    }

    T query(int a, int b){
    	if(b < a)
    	{
    		return make_pair(-1, -1);
		}
        return query(1, 0, n - 1, a, b);
    }

    void update(int pos, T val){
        update(1, 0, n - 1, pos, val);
    }
};


// Esta es la función que mezcla 2 nodos
// En este caso el segment tree tendrá en sus nodos los pares
// (x, y) donde x es el valor en la posición y
// Esto lo hacemos para hacer un segment tree
// de mínimos que además de entregar el mínimo entrega la posición
// donde éste se encuentra.


// Recibe el i, l, r porque a veces es necesario
// tener esa información al mezclar nodos
pair<int, int> merge1(int i, int l, int r, pair<int, int> A, pair<int, int> B){
    return max(A, B);   // Es simplemente el mínimo lexicográfico
}

int main()
{
	int n, act; cin >> n;
	vector< pair<int, int> > arr(n);
	for(int i = 0; i < n; i++)
	{
		int a; cin >> a;
		if(i == 0)
		{
			act = a;
		}
		arr[a] = make_pair(n - 1 - i, a);
	}
	
	int izq = 0, der = n - 1;
	
	SegmentTree<pair<int, int> > minST(arr, merge1);
	
	while(izq != der)
	{
		//cout << izq << endl;
		if(minST.query(izq, act - 1).first > minST.query(act + 1, der).first)
		{
			der = act - 1;
			act = minST.query(izq, act - 1).second;
		}
		else
		{
			izq = act + 1;
			act = minST.query(act + 1, der).second;
		}
	}
	
	cout << izq << endl;
}
