#!/usr/bin/env python3
"""Module for cocktailshaker_sort a variation of bubble sort"""
from sort_speed import Sort_Speed
from random import randint


"""
procedure cocktailShakerSort(A : list of sortable items) is
    do
        swapped := false
        for each i in 0 to length(A) − 1 do:
            if A[i] > A[i + 1] then // test whether the two elements are in the wrong order
                swap(A[i], A[i + 1]) // let the two elements change places
                swapped := true
            end if
        end for
        if not swapped then
            // we can exit the outer loop here if no swaps occurred.
            break do-while loop
        end if
        swapped := false
        for each i in length(A) − 1 to 0 do:
            if A[i] > A[i + 1] then
                swap(A[i], A[i + 1])
                swapped := true
            end if
        end for
    while swapped // if no elements have been swapped, then the list is sorted
end procedure
"""


def cocktailshaker_sort(array):
    swapped = True
    while swapped:
        swapped = False
        print(array)
        for g in range(1, len(array)):
            if array[g - 1] > array[g]:
                array[g] += array[g-1]
                array[g-1] = array[g] - array[g-1]
                array[g] = array[g] - array[g-1]
                swapped = True

        if not swapped:
            break
        else:
            swapped = False

        print(array)
        for h in range(len(array) - 1, 0):
            if array[h] > array[h + 1]:
                array[h] += array[h+1]
                array[h+1] = array[h] - array[h+1]
                array[h] = array[h] - array[h+1]
                swapped = True


if __name__ == "__main__":
    """o = Sort_Speed(cocktailshaker_sort)
    print(o.speed_test(), end="\n\n")

    print(o.speed_test(1), end="\n\n")

    o.arr_len = (5, 50)
    print(o.speed_test())"""

    cocktailshaker_sort([randint(10, 100) for x in range(15)])
