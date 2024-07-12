#!/usr/bin/env python3
"""Playing around with base conversion."""


from collections.abc import Iterator


class MyNum:
    """A custom number representation."""

    def __init__(self, num: int, base: int) -> None:
        """Initialise MyNum."""
        if type(num) is not int:
            raise TypeError("num must be an int")

        if type(base) is not int:
            raise TypeError("base must be an int")

        if 2 <= base <= 36:
            self.__base = base
        else:
            raise ValueError("base is put of range. Supported bases are 2-36")

        self.__is_negative: bool = num < 0
        self.__arr: bytearray = bytearray()
        num = abs(num)
        match base:
            case 2:
                self.__arr = bytearray(bin(num).lstrip("0b"), "utf-8")
            case 8:
                self.__arr = bytearray(oct(num).lstrip("0o"), "utf-8")
            case 10:
                self.__arr = bytearray(str(num), "utf-8")
            case 16:
                self.__arr = bytearray(hex(num).lstrip("0x"), "utf-8")
            case _:
                while num:
                    v: int = num % base
                    if 0 <= v <= 10:
                        v += ord("0")
                    else:
                        v = ord("A") + (v - 10)

                    self.__arr.insert(0, v)
                    num //= base

    @property
    def base(self) -> int:
        """The base of the number."""
        return self.__base

    def __iter__(self) -> Iterator:
        """Return an iterator of self."""
        return iter(self.__arr)

    def __repr__(self) -> str:
        """Return string representation of self."""
        s: str = ""
        if self.__is_negative:
            s = "-"

        return s + "".join([chr(v) for v in self])
