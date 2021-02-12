#include <bits/stdc++.h>

using namespace std;

int main(int argc, char const *argv[])
{
    // To be continued
    int n, solution = 0;
    cin >> n;
    long lowest_price = 1e10;

    for (int i = 0; i < n; i++) {
        long price;
        string pack;
        cin >> price >> pack;

        if (lowest_price >= 0 && price > lowest_price)
            continue;

        // 2021
        int nums[4] = {0};
        for (char const &c: pack) {
            if (c == '2') {
                if (nums[0]) nums[2] = 1;
                else nums[0] = 1;
            } else if (c == '0') {
                nums[1] = 1;
            } else if (c == '1') {
                nums[3] = 1;
            }
        }

        bool all_preset = true;
        for (int j = 0; j < 4; j++)
            if (!nums[j]) {
                all_preset = false;
                break;
            }

        if (all_preset && price < lowest_price) {
            lowest_price = price;
            solution = i + 1;
        }
    }

    cout << solution;

    return 0;
}
