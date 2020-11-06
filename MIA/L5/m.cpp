#include<iostream>

using namespace std;

int main(int argc, char const *argv[])
{
    short t;
    cin >> t;

    for (short i = 0; i < t; i++) {
        short v, e;
        cin >> v >> e;
        cout << e - v + 2 << endl;
    }

    return 0;
}
