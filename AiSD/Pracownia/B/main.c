#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define size ((int)1e6 + 1)

int N, *D, *D2;

static inline int max (int a, int b) {
    if (a > b) return a;
    else if (b > a) return b;
    else return a;
}

static inline void max_equal_sum_or_smallest_diff(int arr[]) {
    memset(D, -1, size * sizeof(int));
    memset(D2, -1, size * sizeof(int));
    D[0] = 0;
    D2[0] = 0;
    int max_diff = 0, new_diff = 0;

    for (int i = 0; i < N; i++) {
        for (int j = 0; j <= max_diff; j++) {
            if (D[j] == -1) continue;
            int s = D[j] + arr[i];

            int new_idx = abs((int)(j - arr[i]));
            D2[new_idx] = max(D2[new_idx], s);

            new_idx = j + arr[i];
            
            if (new_idx > max_diff)
                new_diff = new_idx;

            D2[new_idx] = max(D2[new_idx], s);
        }
        max_diff = new_diff;
        memcpy(D, D2, size * sizeof(int));
    }
}

int main() {
    D = malloc(size * sizeof(int));
    D2 = malloc(size * sizeof(int));

    scanf("%d", &N);

    int arr[N];
    for (int i = 0; i < N; i++)
        scanf("%d", &arr[i]);

    max_equal_sum_or_smallest_diff(arr);

    if (D[0] > 0) {
        printf("TAK\n%d", D[0] / 2);
    } else {
        printf("NIE\n");
        for (int i = 1; i < size; i++)
            if (D[i] != -1 && i != D[i]) {
                printf("%d", i);
                break;
            }
    }

    return 0;
}
