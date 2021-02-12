#include <bits/stdc++.h>

using namespace std;

struct operation {
    int left, right, value;
};


int main(int argc, char const *argv[]) {
    int num_of_elements, num_of_operations, num_of_queries;
    cin >> num_of_elements >> num_of_operations >> num_of_queries;

    vector <long long> element(num_of_elements + 1, 0);
    for(int i = 1; i <= num_of_elements; i++) {
        cin >> element[i];
    }

    vector <operation> operations(num_of_operations + 1);
    for(int i = 1; i <= num_of_operations; i++) {
        cin >> operations[i].left >> operations[i].right >> operations[i].value;
    }

    vector <int> num_of_operations_starting(num_of_operations + 2, 0);
    while(num_of_queries--) {
        int left_operation, right_operation;
        cin >> left_operation >> right_operation;

        num_of_operations_starting[left_operation]++;
        num_of_operations_starting[right_operation + 1]--;
    }

    vector <int> no_of_uses(num_of_operations + 1, 0);
    for(int i = 1; i <= num_of_operations; i++) {
        no_of_uses[i] = no_of_uses[i - 1] + num_of_operations_starting[i];
    }

    vector <long long> no_of_updates_starting(num_of_elements + 2, 0);
    for(int i = 1; i <= num_of_operations; i++) {
        int start_point = operations[i].left, end_point = operations[i].right, d = operations[i].value;

        no_of_updates_starting[start_point] += no_of_uses[i]*1LL*d;
        no_of_updates_starting[end_point + 1]-= no_of_uses[i]*1LL*d;
    }

    vector <long long> amount_to_be_added(num_of_elements + 1, 0);
    for(int i = 1; i <= num_of_elements; i++) {
        amount_to_be_added[i] = amount_to_be_added[i - 1] + no_of_updates_starting[i];
    }

    for(int i = 1; i <= num_of_elements; i++) {
        element[i] += amount_to_be_added[i];
    }

    for(int i = 1; i <= num_of_elements; i++) {
        cout << element[i] << " ";
    }

    return 0;
}
