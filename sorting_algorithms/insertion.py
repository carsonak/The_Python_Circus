#!/usr/bin/env python3
"""
Module for insertion_sort

Performance
-----------
Worst-case : O(n^2) comparisons and swaps
Best-case : O(n) comparisons, O(1) swaps
Average : O(n^2) comparisons and swaps

Space
-----
Worst-case : O(n) total, O(1) auxiliary
"""
from sort_speed import Sort_Speed
from numpy import ndarray


def insertion_sort(array: ndarray):
    for i in range(1, len(array)):
        k = array[i]
        j = i
        while j > 0 and array[j - 1] > k:
            array[j] = array[j - 1]
            j -= 1

        array[j] = k


if __name__ == "__main__":
    o = Sort_Speed(insertion_sort)
    print(o.speed_test(), end="\n\n")

    print(o.speed_test(1), end="\n\n")

    o.arr_len = (5, 50)
    print(o.speed_test())
