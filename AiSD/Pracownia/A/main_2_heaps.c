#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct {
    uint64_t d;
    uint64_t nd;
} pair;

uint32_t first_size, second_size = 0, strings_no = 0;
pair *first_minheap, *second_minheap;

static inline void swap(pair *i, pair *j) {
    pair temp = *i; 
    *i = *j; 
    *j = temp; 
} 

static inline void move_down(pair heap[], uint32_t size, uint32_t i) {
    uint32_t left_son_idx, right_son_idx, j;

    do {
        j = i;
        left_son_idx = 2*i + 1;
        right_son_idx = left_son_idx + 1;

        if (left_son_idx < size && heap[left_son_idx].d < heap[j].d) 
            i = left_son_idx;

        if (right_son_idx < size && heap[right_son_idx].d < heap[j].d && heap[right_son_idx].d < heap[left_son_idx].d)
            i = right_son_idx;

        swap(&heap[i], &heap[j]);
    } while (j != i);
}

static inline void move_up(pair heap[], uint32_t i) {
    uint32_t j;
    do {
        j = i;
        if (i > 0 && heap[(i - 1) / 2].d > heap[i].d)
            i = (i - 1) / 2;

        swap(&heap[i], &heap[j]);
    } while (j != i);
}


static inline void make_heap(pair heap[], uint32_t size) {
    for (int i = (size - 1) / 2; i >= 0; i--)
        move_down(heap, size, i);
}

static inline void insert(pair elem) {
    second_minheap[second_size] = elem;
    move_up(second_minheap, second_size);
    second_size += 1;
}

static inline uint32_t move_hole_down(pair heap[], uint32_t size) {
    uint32_t left_son_idx, right_son_idx, j, i = 0;
    
    do {
        j = i;
        left_son_idx = 2*i + 1;
        right_son_idx = left_son_idx + 1;

        if (right_son_idx < size && heap[right_son_idx].d < heap[left_son_idx].d)
            i = right_son_idx;
        else if (left_son_idx < size)
            i = left_son_idx;

        heap[j] = heap[i];
    } while (j != i);

    return i;
}

static inline pair pop_min(pair heap[], uint32_t* size) {
    pair min = heap[0];

    uint32_t hole_idx = move_hole_down(heap, *size);
    
    *size -= 1;
    if (hole_idx != *size) {
        heap[hole_idx] = heap[*size];
        move_up(heap, hole_idx);
    }

    return min;
}

int main() {
    scanf("%d", &first_size);

    first_minheap = malloc(sizeof(pair)*first_size);
    second_minheap = malloc(sizeof(pair)*first_size);
    
    for(uint32_t i = 0; i < first_size; i++)
        scanf("%ld %ld", &first_minheap[i].d, &first_minheap[i].nd);

    make_heap(first_minheap, first_size);

    // printf("First heap before:\n");
    // for(uint32_t i = 0; i < first_size; i++)
    //     printf("(%ld %ld)", first_minheap[i].nd, first_minheap[i].d);
    // printf("\n===================\n");

    uint64_t smaller_strings_no = 0;
    pair joined_strings, first_min, second_min;

    while (first_size > 0) {
        if (second_size > 0) {
            if (first_minheap[0].d == second_minheap[0].d) {
                // remove min from both heaps
                first_min = pop_min(first_minheap, &first_size);
                second_min = pop_min(second_minheap, &second_size);
                smaller_strings_no = first_min.nd + second_min.nd;
                
                if (second_size > 0 && second_minheap[0].d == second_min.d) {
                    second_min = pop_min(second_minheap, &second_size);
                    smaller_strings_no += second_min.nd;
                }

                joined_strings.d = second_min.d * 2;
                joined_strings.nd = smaller_strings_no / 2;
            } else if (first_minheap[0].d > second_minheap[0].d) {
                second_min = pop_min(second_minheap, &second_size);
                smaller_strings_no = second_min.nd;

                if (second_size > 0 && second_minheap[0].d == second_min.d) {
                    second_min = pop_min(second_minheap, &second_size);
                    smaller_strings_no += second_min.nd;
                }

                joined_strings.d = second_min.d * 2;
                joined_strings.nd = smaller_strings_no / 2;
            } else {
                first_min = pop_min(first_minheap, &first_size);
                smaller_strings_no = first_min.nd;
                joined_strings.d = first_min.d * 2;
                joined_strings.nd = smaller_strings_no / 2;
            }
        } else {
            first_min = pop_min(first_minheap, &first_size);
            smaller_strings_no = first_min.nd;
            joined_strings.d = first_min.d * 2;
            joined_strings.nd = smaller_strings_no / 2;
        }

        if (smaller_strings_no == 1) {
            strings_no++;
        } else {
            if (smaller_strings_no % 2 == 1) {
                insert(joined_strings);
                strings_no++;
            } else {
                insert(joined_strings);
            }
        }
    }

    while (second_size > 0) {
        second_min = pop_min(second_minheap, &second_size);
        smaller_strings_no = second_min.nd;

        if (second_size > 0 && second_minheap[0].d == second_min.d) {
            second_min = pop_min(second_minheap, &second_size);
            smaller_strings_no += second_min.nd;
        }

        if (smaller_strings_no == 1) {
            strings_no++;
        } else {
            joined_strings.d = second_min.d * 2;
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
