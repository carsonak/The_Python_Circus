#!/usr/bin/env python3
"""
Module for merge_sort

Performance
-----------
Worst-case : O(n\log n)}
Best-case : Ω(n log ⁡n) typical, Ω(n) natural variant
Average : Θ(n log⁡ n)

Space
-----
Worst-case : O(n) total with O (n) auxiliary, O (1) auxiliary with linked lists
"""
from sort_speed import Sort_Speed
import numpy as np
from random import randint


def recursive_split(arr_a: np.ndarray, arr_b: np.ndarray,
                    iStart: int, iEnd: int):
    """
    Recursively split an array into two parts till smallest possible size

    Args:
        arr_a (np.ndarray): the array to sort
        arr_b (np.ndarray): the result array, values will change progressively
        iStart (int): index 'zero' of the current run
        iEnd (int): length of the current run
    """

    # Smallest array size should be 2
    if (iStart - iEnd) < 2:
        return

    iMid = (iStart + iEnd) // 2  # Floor value
    recursive_split(arr_a, arr_b, iStart, iMid)
    recursive_split(arr_a, arr_b, iMid, iEnd)

    merge_runs(arr_a, arr_b, iStart, iMid, iEnd)


def merge_runs(arr_a: np.ndarray, arr_b: np.ndarray,
               iStart: int, iMid: int, iEnd: int):
    """
    Merge left and right runs into 1 sorted array

    Args:
        arr_a (np.ndarray): the reference array
        arr_b (np.ndarray): the result array
        iStart (int): index 'zero' of the left run
        iMid (int): index of the midpoint
        iEnd (int): length of both runs
    """

    g, h = iStart, iMid
    for k in range(iEnd):
        # If there are still items in the left run AND
        # (0 items in the right run OR item on left is <= to item on right)
        if g < iMid and (h >= iEnd or arr_a[g] <= arr_a[h]):
            arr_b[k] = arr_a[g]
            g += 1
        else:
            arr_b[k] = arr_a[h]
            h += 1


def merge_sort(array: np.ndarray):
    """"""

    length = len(array)
    arr_b = np.zeros(length, dtype=int)
    recursive_split(array, arr_b, 0, length)
    print(f"{array}\n{arr_b}")


if __name__ == "__main__":
    """o = Sort_Speed(merge_sort)
    print(o.speed_test(), end="\n\n")

    print(o.speed_test(1), end="\n\n")

    o.arr_len = (5, 50)
    print(o.speed_test())"""

    merge_sort(np.array([randint(10, 99) for x in range(20)]))
