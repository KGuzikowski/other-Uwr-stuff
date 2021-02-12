#include <bits/stdc++.h>
 
using namespace std;
 
int main()
{
    int n, t;
    double p;
    cin >> n >> p >> t;
 
    vector<vector<double>> dp(t + 1, vector<double>(n + 5));
 
    dp[0][0] = 1;
 
    for (int i = 0; i < t; i++)
    {
        for (int j = 0; j < n; j++)
            if (dp[i][j] > 0)
            {
                dp[i + 1][j + 1] += dp[i][j] * p;
                dp[i + 1][j] += dp[i][j] * (1 - p);
            }
        dp[i + 1][n] += dp[i][n];
    }
 
    double res = 0;
    for (int i = 1; i <= n; i++)
    {
        res += dp[t][i] * i;
    }
 
    cout << setprecision(11) << fixed << res << endl;
    return 0;
}