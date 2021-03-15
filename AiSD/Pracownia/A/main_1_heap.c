#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct {
    uint64_t d;
    uint64_t nd;
} pair;

uint32_t first_size;
uint32_t strings_no = 0;
pair *first_minheap;

static inline void swap(uint32_t i, uint32_t j) {
    pair temp = first_minheap[i]; 
    first_minheap[i] = first_minheap[j]; 
    first_minheap[j] = temp; 
} 

static inline void move_down(uint32_t i) {
    uint32_t left_son_idx, right_son_idx, j;

    do {
        j = i;
        left_son_idx = 2*i + 1;
        right_son_idx = 2*i + 2;

        if (left_son_idx < first_size && first_minheap[left_son_idx].d < first_minheap[j].d) 
            i = left_son_idx;

        if (right_son_idx < first_size && first_minheap[right_son_idx].d < first_minheap[j].d && first_minheap[right_son_idx].d < first_minheap[left_son_idx].d)
            i = right_son_idx;

        swap(i, j);
    } while (j != i);
}

static inline void move_up(uint32_t i) {
    uint32_t j;

    do {
        j = i;
        if (i > 0 && first_minheap[(i - 1) / 2].d > first_minheap[i].d)
            i = (i - 1) / 2;

        swap(i, j);
    } while (j != i);
}

static inline void make_heap() {
    for (int i = (first_size - 1) / 2; i >= 0; i--)
        move_down(i);
}

static inline void insert(pair elem) {
    first_minheap[first_size] = elem;
    move_up(first_size);
    first_size++;
}

static inline uint32_t move_hole_down() {
    uint32_t left_son_idx, right_son_idx, j, i = 0;
    
    do {
        j = i;
        left_son_idx = 2*i + 1;
        right_son_idx = 2*i + 2;

        if (right_son_idx < first_size && first_minheap[right_son_idx].d < first_minheap[left_son_idx].d)
            i = right_son_idx;
        else if (left_son_idx < first_size)
            i = left_son_idx;

        first_minheap[j] = first_minheap[i];
    } while (j != i);

    return i;
}

static inline pair pop_min() {
    pair min = first_minheap[0];

    uint32_t hole_idx = move_hole_down();
    
    first_size--;
    if (hole_idx != first_size) {
        first_minheap[hole_idx] = first_minheap[first_size];
        move_up(hole_idx);
    }

    return min;
}

int main() {
    scanf("%d", &first_size);

    first_minheap = malloc(sizeof(pair)*first_size);
    
    for(uint32_t i = 0; i < first_size; i++)
        scanf("%ld %ld", &first_minheap[i].d, &first_minheap[i].nd);

    make_heap(first_minheap, first_size - 1);

    uint64_t smaller_strings_no = 0;
    pair first_min, joined_strings;

    while (first_size > 0) {
        first_min = pop_min();

        smaller_strings_no = first_min.nd;

        if (first_size > 0 && first_minheap[0].d == first_min.d) {
            first_min = pop_min();
            smaller_strings_no += first_min.nd;
        }

        if (smaller_strings_no == 1) {
            strings_no++;
        } else {
            joined_strings.d = first_min.d * 2;
            joined_strings.nd = smaller_strings_no / 2;

            if (smaller_strings_no % 2 == 1) {
                insert(joined_strings);
                strings_no++;
            } else {
                insert(joined_strings);
            }
        }
    }

    printf("%d\n", strings_no);

    return 0;
}
