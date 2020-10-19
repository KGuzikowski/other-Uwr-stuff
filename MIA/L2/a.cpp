#include <iostream>

using namespace std;

int main(int argc, char const *argv[])
{
    int days;
    cin >> days;
    short min_price;
    int total = 0;

    for (int i = 0; i < days; i++) {
        short kgs, price;
        cin >> kgs >> price;
        if (i == 0) min_price = price;
        
        if (price < min_price) {
            min_price = price;
        } 
        total += kgs * min_price;
    }

    cout << total << endl;
    return 0;
}
