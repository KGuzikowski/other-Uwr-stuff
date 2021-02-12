#include <bits/stdc++.h>

using namespace std;

int main()
{
    const int primes[25] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97};
    int arr[101][25] = {0};

    for (int i = 1; i <= 100; i++) {
        int p = i;
        for (int j = 0; p != 1 && j < 25; j++) {
            while (p % primes[j] == 0) {
                arr[i][j] += 1;
                p /= primes[j];
            }
        }
    }

    int a, b, c, final = 0;
    cin >> a >> b >> c;

    for (int i = 1; i <= a; i++) {
        for (int j = 1; j <= b; j++) {
            for (int k = 1; k <= c; k++) {
                int divisors = 1;
                for (int m = 0; m < 25; m++) {
                    divisors *= (1 + arr[i][m] + arr[j][m] + arr[k][m]);
                }
                final += divisors;
            }
        }
    }

    cout << final % 1073741824 << endl;

    return 0;
}