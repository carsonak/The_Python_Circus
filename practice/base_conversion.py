#!/usr/bin/python3
"""Convert an int to any base between 2 and 62."""

from random import randint
import sys
from timeit import timeit


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def to_anybase(num: int, base: int) -> str:
    """Return the string representation of a number in a given base.

    Args:
        num: the number to convert.
        base: radix between 2 and 62 to convert the number to.

    Return:
        a string representing the given number in the given base.
    """
    if type(num) is not int:
        raise TypeError("num must be an int")

    if type(base) is not int:
        raise TypeError("base must be an int")

    if not 2 <= base <= 62:
        raise ValueError("base is out of range, must be between 2-62")

    if num == 0:
        return "0"

    match base:
        case 2:
            return bin(num)
        case 8:
            return oct(num)
        case 16:
            return hex(num)
        case _:
            out: str = ""
            is_negative: bool = num < 0
            num = abs(num)
            while num:
                c: int = num % base
                if c < 10:
                    out = chr(ord("0") + c) + out
                elif c < 36:
                    out = chr(ord("a") + c - 10) + out
                else:
                    out = chr(ord("A") + c - 36) + out

                num //= base

    if is_negative:
        out = "-" + out

    return out


if __name__ == "__main__":
    print(to_anybase(int(sys.argv[1]), int(sys.argv[2])))
    # num = 1000
    # print("num = {}, base = 36: {}s".format(
    #     num, timeit(stmt="to_anybase(num, 36)", number=10, globals=globals()))
    # )
    # num = 1000 ** 10
    # print("num = 1000 ** 10, base = 36: {}s".format(
    #     timeit(stmt="to_anybase(num, 36)", number=10, globals=globals()))
    # )
    # num = 1000 ** 100
    # print("num = 1000 ** 100, base = 36: {}s".format(
    #     timeit(stmt="to_anybase(num, 36)", number=10, globals=globals()))
    # )
    # num = 1000 ** 1_000
    # print("num = 1000 ** 1_000, base = 36: {}s".format(
    #     timeit(stmt="to_anybase(num, 36)", number=10, globals=globals()))
    # )
    # num = 1000 ** 10_000
    # print("num = 1000 ** 10_000, base = 36: {}s".format(
    #     timeit(stmt="to_anybase(num, 36)", number=10, globals=globals()))
    # )
