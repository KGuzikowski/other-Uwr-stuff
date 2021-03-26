#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define size (int)10e6

uint32_t N, D[size] = {0}, D2[size] = {0};

int compare (const void * a, const void * b) {
    uint32_t _a = *(int*)a;
    uint32_t _b = *(int*)b;
    if (_a < _b) return -1;
    else if (_a == _b) return 0;
    else return 1;
}

uint32_t max (uint32_t a, uint32_t b) {
    if (a > b) return a;
    else if (b > a) return b;
    else return a;
}

void max_equal_sum_or_smallest_diff(uint32_t arr[]) {
    for (uint32_t i = 0; i < N; i++) {
        for (uint32_t j = 0; j < size; j++) {
            uint32_t s = D[j] + arr[i];

            uint32_t abs_val = abs(j - arr[i]);
            D2[abs_val] = max(D2[abs_val], s);

            abs_val = j + arr[i];
            D2[abs_val] = max(D2[abs_val], s);
        }
        memcpy(D, D2, size * sizeof(uint32_t));
    }
}

int main() {
    scanf("%d", &N);

    uint32_t arr[N];
    for (uint32_t i = 0; i < N; i++)
        scanf("%d", &arr[i]);

    qsort(arr, N, sizeof(uint32_t), compare);
    max_equal_sum_or_smallest_diff(arr);

    uint32_t a = D[0];
    if (D[0] != 0) {
        printf("TAK\n");
        printf("%d", D[0] / 2);
    } else {
        printf("NIE\n");
        for (uint32_t i = 1; i < size; i++)
            if (D[i] != 0) {
                printf("%d", i);
                break;
            }
    }

    return 0;
}
