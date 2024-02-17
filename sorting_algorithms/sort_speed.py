#!/usr/bin/env python3
"""Module for Sort_Speed"""
import numpy as np
from time import perf_counter
from random import randint


class Sort_Speed():
    """
    Sort_Speed class: methods and attributes for timing sorting algorithms

    Attributes:
        funct (function): a function to be tested
        reps (int): number of repetitions
        data_range: range of values for the data set
        arr_len: array length of data set

    Methods:
        __init__: initialises a Sort_Speed instance
        speed_test: runs a function over a random set of data and
            times execution time
    """

    def __init__(self, funct, reps=10000, data_range=(10, 100), arr_len=20):
        self.funct = funct
        self.reps = reps
        self.data_range = data_range
        self.arr_len = arr_len

    @property
    def funct(self):
        return self.__funct

    @funct.setter
    def funct(self, funct):
        """Set the function to test"""

        if type(funct) is not type(lambda x: x):
            raise TypeError("funct must be a function")

        self.__funct = funct

    @property
    def reps(self):
        return self.__iters

    @reps.setter
    def reps(self, reps):
        """Set number of reps"""

        if type(reps) is not int:
            raise TypeError("reps must be an int")

        if reps < 0:
            raise ValueError("reps must be a positive integer")

        self.__iters = reps

    @property
    def data_range(self):
        return self.__range

    @data_range.setter
    def data_range(self, data_range):
        """Set the data_range"""

        if type(data_range) is not tuple:
            raise TypeError("data_range must be a tuple of 2 integers")

        if type(data_range[0]) is not int or type(data_range[1]) is not int:
            raise TypeError("data_range must be a tuple of 2 integers")

        self.__range = data_range

    @property
    def arr_len(self):
        return self.__alen

    @arr_len.setter
    def arr_len(self, arr_len):
        """Set length of the arrays"""

        a_typ = type(arr_len)
        if a_typ is not int and a_typ is not tuple and a_typ is not list and a_typ is not set:
            raise TypeError("arr_len should be an int or a sequence type")

        if a_typ is tuple or a_typ is list:
            if len(arr_len) != 2:
                raise ValueError("arr_len should be a sequence of 2 ints")

            if type(arr_len[0]) is not int and type(arr_len[1]) is not int:
                raise TypeError("arr_len should be a sequence of 2 ints")

        self.__alen = arr_len

    def speed_test(self, reversed=False):
        """
        Return average execution time of a function on random data sets

        Args:
            reversed (bool): flag for using data sorted in reverse

        Return:
            a string with information about the test results
        """

        a_typ = type(self.arr_len)
        exec_time = np.empty(self.reps)
        for g in range(self.reps):
            if a_typ is int:
                l = np.array([randint(self.data_range[0], self.data_range[1])
                              for x in range(self.arr_len)])
            else:
                l = np.array([randint(self.data_range[0], self.data_range[1])
                              for x in range(randint(self.arr_len[0], self.arr_len[1]))])

            if reversed:
                l = np.sort(l)[::-1]

            start = perf_counter()
            self.funct(l)
            end = perf_counter()
            exec_time[g] = end - start
            # print(f"{exec_time[g]:.7f}s\n{l}")

        return f"{self.funct.__qualname__:s}\n" + ("-" * len(self.funct.__qualname__)) + "\n" + \
            f"Array sizes: {self.arr_len}\n" + \
            f"Iterations: {self.reps}\n" + \
            "Data: {} range {}-{}\n".format(("Reversed" if reversed else "Random"), self.data_range[0], self.data_range[1]) + \
            f"Average sorting time: {np.mean(exec_time):.7f}s\n"
