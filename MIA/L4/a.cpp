#include<bits/stdc++.h>

using namespace std;

int main()
{
    long long n, m;
    long long i, j, k;

    cin >> n >> m;
    long long a[n], b[m];

    for(i = 0; i < n; i++)
        cin >> a[i];
        
    for(i = 0; i < m; i++)
        cin >> b[i];

    sort(a, a + n);

    for(i=0; i < m; i++)
    {
        cout << upper_bound(a, a + n, b[i]) - a << " ";
    }

    return 0;
}