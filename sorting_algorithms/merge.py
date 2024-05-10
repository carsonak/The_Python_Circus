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


# def recursive_split(arr_a: np.ndarray, arr_b: np.ndarray,
#                     iStart: int, iEnd: int):
#     """
#     Recursively split an array into two parts till smallest possible size

#     Args:
#         arr_a (np.ndarray): the array to sort
#         arr_b (np.ndarray): the result array, values will change progressively
#         iStart (int): index 'zero' of the current run
#         iEnd (int): length of the current run
#     """

#     # Smallest array size should be 2
#     if (iEnd - iStart) < 2:
#         return

#     iMid = (iStart + iEnd) // 2  # Floor value
#     recursive_split(arr_a, arr_b, iStart, iMid)
#     recursive_split(arr_a, arr_b, iMid, iEnd)

#     merge_runs(arr_a, arr_b, iStart, iMid, iEnd)


# def merge_runs(arr_a: np.ndarray, arr_b: np.ndarray,
#                iStart: int, iMid: int, iEnd: int):
#     """
#     Merge left and right runs into 1 sorted array

#     Args:
#         arr_a (np.ndarray): the reference array
#         arr_b (np.ndarray): the result array
#         iStart (int): index 'zero' of the left run
#         iMid (int): index of the midpoint
#         iEnd (int): length of both runs
#     """

#     g, h = iStart, iMid
#     for k in range(iStart, iEnd):
#         # If there are still items in the left run AND
#         # (0 items in the right run OR item on left is <= to item on right)
#         if g < iMid and (h >= iEnd or arr_a[g] <= arr_a[h]):
#             arr_b[k] = arr_a[g]
#             g += 1
#         else:
#             arr_b[k] = arr_a[h]
#             h += 1

#     # arr_a = np.copy(arr_b[iStart:iEnd+1])


# def merge_sort(array: np.ndarray):
#     """Accepts array input and calls the actual sorting function"""

#     print(array)
#     length = len(array)
#     arr_b = np.copy(array)
#     # arr_b = np.zeros(length, dtype=int)
#     recursive_split(array, arr_b, 0, length)
#     print(arr_b)

# Python program for implementation of MergeSort

# Merges two subarrays of arr[].
# First subarray is arr[l..m]
# Second subarray is arr[m+1..r]


def merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m

    # create temp arrays
    L = [0] * (n1)
    R = [0] * (n2)

    # Copy data to temp arrays L[] and R[]
    for i in range(0, n1):
        L[i] = arr[l + i]

    for j in range(0, n2):
        R[j] = arr[m + 1 + j]

    # Merge the temp arrays back into arr[l..r]
    i = 0	 # Initial index of first subarray
    j = 0	 # Initial index of second subarray
    k = l	 # Initial index of merged subarray

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    # Copy the remaining elements of L[], if there
    # are any
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

    # Copy the remaining elements of R[], if there
    # are any
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

# l is for left index and r is right index of the
# sub-array of arr to be sorted


def mergeSort(arr, l, r):
    if l < r:

        # Same as (l+r)//2, but avoids overflow for
        # large l and h
        m = l+(r-l)//2

        # Sort first and second halves
        mergeSort(arr, l, m)
        mergeSort(arr, m+1, r)
        merge(arr, l, m, r)


if __name__ == "__main__":
    """o = Sort_Speed(merge_sort)
    print(o.speed_test(), end="\n\n")

    print(o.speed_test(1), end="\n\n")

    o.arr_len = (5, 50)
    print(o.speed_test())"""

    # merge_sort(np.array([randint(10, 99) for x in range(10)]))
    # Driver code to test above
    arr = [12, 11, 13, 5, 6, 7]
    n = len(arr)
    print(arr)
    mergeSort(arr, 0, n-1)
    print(arr)
