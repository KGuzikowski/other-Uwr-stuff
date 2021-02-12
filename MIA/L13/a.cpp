#include <iostream>

using namespace std;

int main(int argc, char const *argv[]) {
    long long n, k, res;

    cin >> n >> k;

    res = n / k;
    if (res % 2 != 0) cout << "YES\n";
    else cout << "NO\n";

    return 0;
}
