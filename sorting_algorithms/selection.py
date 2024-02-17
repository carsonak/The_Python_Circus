#!/usr/bin/env python3
"""Module for selection_sort"""
from sort_speed import Sort_Speed
from random import randint


def selection_sort(array):
    print(array)
    for g in range(0, (len(array) - 1)):
        min = g
        for h in range(g + 1, len(array)):
            if array[h] < array[min]:
                min = h

        if min != g:
            b = array[g]
            array[g] = array[min]
            array[min] = b

    print(array)


if __name__ == "__main__":
    o = Sort_Speed(selection_sort)
    print(o.speed_test(), end="\n\n")

    print(o.speed_test(1), end="\n\n")

    o.arr_len = (5, 50)
    print(o.speed_test())
