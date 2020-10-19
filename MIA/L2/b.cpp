#include <iostream>
#include <algorithm>

using namespace std;

int main()
{
    short n, a;
    cin >> n;
    short exist[5001] = { 0 };

    for (int i = 0; i < n; i++)
    {
        cin >> a;
        if (a <= n)
        {
            exist[a] = 1;
        }
    }
    cout << count(exist + 1, exist + n + 1, 0) << endl;
    return 0;
}
