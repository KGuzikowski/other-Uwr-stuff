#include<iostream>

using namespace std;

int main() {
    int n, t;

    cin >> n >> t;
    int a[n-1];

    for (int i = 0; i < n - 1; i++)
        cin >> a[i];

    int i = 0;
    while (i < n-1) {
        i = i + a[i];
        if (i == t- 1) {
            cout << "YES" <<endl;
            return 0;
        }
    }

    cout<< "NO" << endl;

    return 0;
}