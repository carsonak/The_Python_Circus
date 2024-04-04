#!/usr/bin/env python3
"""
Module for bubble_sort

Performance
-----------
Worst-case : O(n^2) comparisons, O(n^2) swaps
Best-case : O(n) comparisons, O(1) swaps
Average : O(n^2) comparisons, O(n^2) swaps

Space
-----
Worst-case : O(n) total, O(1) auxiliary
"""
from sort_speed import Sort_Speed
from numpy import ndarray


def bubble_sort(array: ndarray):
    g = len(array)
    while g > 1:
        new_g = 0
        for h in range(1, g):
            if array[h-1] > array[h]:
                b = array[h-1]
                array[h-1] = array[h]
                array[h] = b
                new_g = h

        else:
            g = new_g


if __name__ == "__main__":
    o = Sort_Speed(bubble_sort)
    print(o.speed_test(), end="\n\n")

    print(o.speed_test(1), end="\n\n")

    o.arr_len = (5, 50)
    print(o.speed_test())
