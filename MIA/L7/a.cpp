#include<iostream>

using namespace std;

int main(int argc, char const *argv[])
{
    int N;
    cin >> N;
    int flamingos[N];
    int qty[N-1];

    for (int i = N; i > 1; i--) {
        cout << "? 1 " << i << endl;
        cin >> qty[i-2];
    }
    cout << "? 2 3" << endl;
    int two_and_three;
    cin >> two_and_three;

    for (int i = N - 1; i >= 0; i--) {
        if (i > 1)
            flamingos[i] = qty[i-1] - qty[i-2];
        else
            flamingos[2] = qty[1] - qty[0];
    }

    flamingos[1] = two_and_three - flamingos[2];
    flamingos[0] = qty[0] - flamingos[1];

    cout << "!";
    for (int i = 0; i < N; i++) {
        cout << " " << flamingos[i];
    }
    cout << endl;

    return 0;
}
