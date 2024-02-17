#!/usr/bin/env python3
"""Module for insertion_sort"""
from sort_speed import Sort_Speed


def insertion_sort(array):
    """Insertion sort code"""

    for i in range(1, len(array)):
        k = array[i]
        j = i
        while j > 0 and array[j - 1] > k:
            array[j] = array[j - 1]
            j -= 1

        array[j] = k


if __name__ == "__main__":
    o = Sort_Speed(insertion_sort)
    print(o.speed_test())

    print(o.speed_test(1))

    o.arr_len = (5, 50)
    print(o.speed_test())
