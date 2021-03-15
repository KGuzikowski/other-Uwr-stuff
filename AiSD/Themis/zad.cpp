// Karol Guzikowski
// nr indeksu: 308864
// SDU

#include <iostream>

using namespace std;

int main() {
    unsigned int a, b, first;
    cin >> a >> b;

    unsigned int i = a;
    while (true) {
        if (i%2021 == 0) {
            first = i;
            break;
        }
        i++;
    }

    for (i; i <= b; i += 2021)
        cout << i << " ";

    return 0;
}
