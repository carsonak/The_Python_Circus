#!/usr/bin/env python3
"""Module for testing average running time of insertion sort algorithm"""
import numpy as np
import time
import random as ran


def insertion_sort(array):
    """Insertion sort code"""

    for i in range(1, len(array)):
        k = array[i]
        j = i
        while j > 0 and array[j - 1] > k:
            array[j] = array[j - 1]
            j -= 1

        array[j] = k


def main():
    """Main"""

    max = 10000
    n_range = (10, 100)
    exec_time = np.empty(max)
    for g in range(max):
        l = np.array([ran.randint(n_range[0], n_range[1]) for x in range(20)])
        start = time.perf_counter()
        insertion_sort(l)
        end = time.perf_counter()
        exec_time[g] = end - start
        # print(f"{exec_time[g]:.7f}s\n{l}")
    else:
        print(
            f"Insertion Sort\n--------------\nArray sizes: 20" + f"""
Iterations: {max}
Data: Random range {n_range[0]}-{n_range[1]}
Average sorting time: {np.mean(exec_time):.7f}s
""")

    for g in range(max):
        l = np.array([ran.randint(n_range[0], n_range[1]) for x in range(20)])
        l = np.sort(l)[::-1]
        start = time.perf_counter()
        insertion_sort(l)
        end = time.perf_counter()
        exec_time[g] = end - start
        # print(f"{exec_time[g]:.7f}s\n{l}")
    else:
        print(
            f"Insertion Sort\n--------------\nArray sizes: 20" + f"""
Iterations: {max}
Data: Reversed range {n_range[0]}-{n_range[1]}
Average sorting time: {np.mean(exec_time):.7f}s
""")

    for g in range(max):
        l = np.array([ran.randint(n_range[0], n_range[1])
                     for x in range(ran.randint(5, 50))])
        start = time.perf_counter()
        insertion_sort(l)
        end = time.perf_counter()
        exec_time[g] = end - start
    else:
        print(
            f"Insertion Sort\n--------------\nArray sizes: Random range 5-50" + f"""
Iterations: {max}
Data: Random range {n_range[0]}-{n_range[1]}
Average sorting time: {np.mean(exec_time):.7f}s
""")


if __name__ == "__main__":
    main()
