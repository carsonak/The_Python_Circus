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


def main():
    """Main"""

    max = 10000
    n_range = (10, 100)
    exec_time = np.empty(max)
    for g in range(max):
        l = np.array([ran.randint(n_range[0], n_range[1]) for x in range(20)])
        start = time.perf_counter()
        bubble_sort(l)
        end = time.perf_counter()
        exec_time[g] = end - start
        # print(f"{exec_time[g]:.7f}s\n{l}")
    else:
        print(
            f"Bubble Sort\n--------------\nArray sizes: 20" + f"""
Iterations: {max}
Data: Random range {n_range[0]}-{n_range[1]}
Average sorting time: {np.mean(exec_time):.7f}s
""")

    for g in range(max):
        l = np.array([ran.randint(n_range[0], n_range[1]) for x in range(20)])
        l = np.sort(l)[::-1]
        start = time.perf_counter()
        bubble_sort(l)
        end = time.perf_counter()
        exec_time[g] = end - start
        # print(f"{exec_time[g]:.7f}s\n{l}")
    else:
        print(
            f"Bubble Sort\n--------------\nArray sizes: 20" + f"""
Iterations: {max}
Data: Reversed range {n_range[0]}-{n_range[1]}
Average sorting time: {np.mean(exec_time):.7f}s
""")

    for g in range(max):
        l = np.array([ran.randint(n_range[0], n_range[1])
                     for x in range(ran.randint(5, 50))])
        start = time.perf_counter()
        bubble_sort(l)
        end = time.perf_counter()
        exec_time[g] = end - start
    else:
        print(
            f"Bubble Sort\n--------------\nArray sizes: Random range 5-50" + f"""
Iterations: {max}
Data: Random range {n_range[0]}-{n_range[1]}
Average sorting time: {np.mean(exec_time):.7f}s
""")


if __name__ == "__main__":
    main()
