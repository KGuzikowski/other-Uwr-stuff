#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main(){

    short n;
    cin >> n;
    int N = n * (2 * n - 1);
    vector<pair<int, pair<short, short>>> strength;

    for(int i = 0; i < 2 * n; i++){
        for(int j = 0; j < i; j++){
            int value;
            cin >> value;
            pair<short, short> team;
            team.first = j;
            team.second = i;
            strength.push_back(pair<int, pair<short, short>>(value, team));
        }
    }

    sort(strength.begin(), strength.end());
    vector<int> ans(2 * n, -1);

    for(int i = strength.size() - 1; i >= 0; i--){
        pair<short, short> team = strength[i].second;
        if(ans[team.first] >= 0 || ans[team.second] >= 0)
            continue;

        ans[team.first] = team.second;
        ans[team.second] = team.first;
    }

    for(int i = 0; i < 2 * n; i++)
        cout << 1 + ans[i] << " ";
    
    cout << endl;

    return 0;
}
