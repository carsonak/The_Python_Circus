#!/usr/bin/env python3
""""""
import numpy as np
import time
import random as ran

"""
procedure bubbleSort(A : list of sortable items)
    n := length(A)
    repeat
        newn := 0
        for i := 1 to n - 1 inclusive do
            if A[i - 1] > A[i] then
                swap(A[i - 1], A[i])
                newn := i
            end if
        end for
        n := newn
    until n ≤ 1
end procedure
"""


def bubble_sort(array):
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


def speed_test(funct, iters=10000, data_range=(10, 100), arr_len=20, rev=0):
    """"""

    if type(iters) is not int:
        raise TypeError("iters must be an int")

    if iters < 0:
        raise ValueError("iters must be a positive integer")

    a_typ = type(arr_len)
    if a_typ is not int and a_typ is not tuple and a_typ is not list and a_typ is not set:
        raise TypeError("arr_len should be an int or a sequence type")

    if a_typ is tuple or a_typ is list:
        if len(arr_len) != 2:
            raise ValueError("arr_len should be a sequence of 2 ints")

        if type(arr_len[0]) is not int and type(arr_len[1]) is not int:
            raise TypeError("arr_len should be a sequence of 2 ints")

    exec_time = np.empty(iters)
    for g in range(iters):
        if a_typ is int:
            l = np.array([ran.randint(data_range[0], data_range[1])
                         for x in range(arr_len)])
        else:
            l = np.array([ran.randint(data_range[0], data_range[1])
                         for x in range(ran.randint(arr_len[0], arr_len[1]))])

        if rev:
            l = np.sort(l)[::-1]

        start = time.perf_counter()
        funct(l)
        end = time.perf_counter()
        exec_time[g] = end - start
        # print(f"{exec_time[g]:.7f}s\n{l}")

    return f"{funct.__name__:s}\n" + ("-" * len(funct.__name__)) + "\n" + \
        f"Array sizes: {arr_len}\n" + \
        f"Iterations: {iters}\n" + \
        "Data: {} range {}-{}\n".format(("Reversed" if rev else "Random"), data_range[0], data_range[1]) + \
        f"Average sorting time: {np.mean(exec_time):.7f}s\n"


if __name__ == "__main__":
    print(speed_test(bubble_sort))
    print(speed_test(bubble_sort, rev=1))
    print(speed_test(bubble_sort, arr_len=(5, 50)))
