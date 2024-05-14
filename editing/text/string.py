#!/usr/bin/python3
"""Module for string."""

import os
import typing


def strip_path(path: str) -> str:
    """Remove trailing slashes and ./ from pathnames.

    Args:
        path: a string represeting a pathname.

    Returns:
        The modified string.

    Raises:
        TypeError: path is not a str object.
    """
    if not isinstance(path, str):
        raise TypeError("path must be a string")

    path = path.strip(os.sep)
    if path.startswith(f".{os.sep}"):
        path = path[2:]

    return path


@typing.overload
def trimstr(string: str, start: int, /, *, mark: str = "*") -> str:
    """Variant."""
    pass


@typing.overload
def trimstr(
    string: str, start: int, stop: int | None, /, *, mark: str = "*"
) -> str:
    """Variant."""
    pass


def trimstr(
        string: str, start: int, stop: int | None = None,
        fill: str = "", mark: str = "*"
) -> str:
    """Trim a string with a slice(start, stop), add fill where necessary.

    Args:
        string: a str instance
        start: start position of the slice.
        stop: stop position of the slice
        fill: string that will be used to replace the truncated text
        mark: a string used to mark the endpoints of the slice

    Returns:
        The modified string.

    Raises:
        TypeError: if one of stringm fill or mark is not a str
        Exceptions raised by improper slice() arguments
    """
    if not isinstance(string, str):
        raise TypeError("string must be a str")

    if not isinstance(fill, str):
        raise TypeError("fill must be a str")

    if not isinstance(mark, str):
        raise TypeError("mark must be a str")

    new_str: str = string[start:stop]
    fill_len: int = len(string) - len(new_str)
    if fill_len > 0:
        fill_len -= len(mark)
    else:
        mark = ""

    filler: str = fill
    while 0 < len(filler) < fill_len:
        filler = filler.join([filler, filler])

    if stop is None:
        if start > 0:
            filler = "".join([mark, filler[fill_len + 1: None]])
            new_str = "".join([new_str, filler])
        else:
            filler = "".join([filler[0 - fill_len: None], mark])
            new_str = "".join([filler, new_str])
    elif stop > start:
        new_str = new_str.join(
            [f"{filler[:len(string[:start]) + 1]}{mark}",
             f"{mark}{filler[:len(string[-1:stop:-1])]}"]
        )
    elif stop < start:
        new_str = new_str.join(
            [f"{filler[:len(string[:stop])]}{mark}",
             f"{mark}{filler[:len(string[-1:start:-1])]}"]
        )

    return new_str
