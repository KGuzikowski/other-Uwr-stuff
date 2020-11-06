#include<iostream>
#include<map>

using namespace std;

int main(int argc, char const *argv[])
{
    short cases;
    cin >> cases;

    for (short i = 0; i < cases; i++) {
        short v;
        cin >> v;
        map<short, short> votes;

        for (short j = 0; j < v; j++) {
            short num;
            cin >> num;
            auto curr = votes.find(num);
            if (curr == votes.end()) {
                votes.insert({num, 1});
            } else {
                curr->second++;
            }
        }

        pair<short, short> winner = {-1, 0};
        for(auto& x : votes) {
            if ((x.second > winner.second) || (x.second >= winner.second && x.first < winner.first)) {
                winner = x;
            }
        }
        cout << winner.first << endl;
    }

    return 0;
}
