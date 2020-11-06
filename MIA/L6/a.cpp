#include<iostream>
#include <limits>

using namespace std;

int main(int argc, char const *argv[])
{
    int n, k;
    cin >> n >> k;
    short h[n] = {0};
    long total_min = numeric_limits<int>::max();
    int total_min_start = 0;

    for(int i = 0; i < n; i++) {
		cin >> h[i];
	}

    int cost = 0;
    for (int j = 0; j < k; j++) {
        cost += h[j];
    }
	total_min = cost;
	for(int i = 1; i < n-k+1; i++) {
        cost += h[i+k-1] - h[i-1];
        if(total_min > cost) {
            total_min = cost;
            total_min_start = i;
        }
	}

	cout << total_min_start + 1;
    return 0;
}
