#include <bits/stdc++.h>
#define limit 1000

using namespace std;

int main() {
    char board[limit][limit];
    int row[limit] , col[limit];
    int total = 0;
    int n, m;
    cin>>n>>m;

    for(int i=0; i<n; i++)
        cin>>board[i];


    for(int i=0; i<n; i++) {
        for(int j=0; j<m; j++) {
            if(board[i][j] == '*') {
                row[i]++;
                col[j]++;
                total++;
            }
        }
    }



    for(int i=0; i<n; i++) {
        for(int j=0; j<m; j++) {
            if(board[i][j] == '*' && (row[i]+col[j] -1) == total) {
                cout<<"YES"<<endl<<i+1<<' '<<j+1;
                return 0;
            } else if(board[i][j] == '.' && (row[i]+col[j]) == total) {
                cout<<"YES"<<endl<<i+1<<' '<<j+1;
                return 0;
            }

        }
    }

    if(!total) cout<<"YES\n1 1\n";
    else cout<<"NO\n";

    return 0;
}