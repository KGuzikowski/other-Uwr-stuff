#include <iostream>
#include <algorithm> 

using namespace std;

bool isBeautiful(short year) {
    string str = to_string(year);

    sort(begin(str), end(str));
    auto pos = adjacent_find(begin(str), end(str));
    if (pos != end(str))
        return false;
    return true;
}

int main(int argc, char const *argv[])
{
    short year;
    cin >> year;
    bool beautiful = false;

    short i = year + 1;
    while (true) {
        if (isBeautiful(i))
            break;

        i++;
    }

    cout << i << endl;
    
    return 0;
}
