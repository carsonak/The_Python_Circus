#!/usr/bin/env python3
"""
Module for cocktailshaker_sort a variation of bubble sort

Performance
-----------
Worst-case : O(n^2)
Best-case : O(n)
Average : O(n^2)

Space
-----
Worst-case : O(1) auxiliary
"""
from sort_speed import Sort_Speed
from numpy import ndarray


def cocktailshaker_sort(array: ndarray):
    """
    A variation of bubble sort that operates bi-directionally
    """

    top, bot = len(array), 1
    new_top, new_bot = top, bot
    swapped = True
    while swapped and top > bot:
        swapped = False
        for g in range(bot, top):
            if array[g - 1] > array[g]:
                b = array[g-1]
                array[g-1] = array[g]
                array[g] = b
                swapped = True
                new_top = g
        else:
            top = new_top

        if not swapped:
            break

        swapped = False
        for h in range(top, bot - 1, -1):
            if array[h] < array[h - 1]:
                b = array[h-1]
                array[h-1] = array[h]
                array[h] = b
                swapped = True
                new_bot = h
        else:
            bot = new_bot


if __name__ == "__main__":
    o = Sort_Speed(cocktailshaker_sort)
    print(o.speed_test(), end="\n\n")

    print(o.speed_test(1), end="\n\n")

    o.arr_len = (5, 50)
    print(o.speed_test())
