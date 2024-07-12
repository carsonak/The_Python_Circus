#!/usr/bin/env python
"""Random str generator."""

from collections.abc import Iterable
import json
from random import SystemRandom
from string import printable


def randstr(char_set: Iterable, length: int) -> str:
    """Return a shuffled string of characters in char_set.

    Shuffles as many repetitions of char_set that fulfill length.

    Args:
        char_set: the set of characters to be used.
        length: the length of the output string.

    Return:
        A str of printable characters in char_set of length length.
    """
    p_set: set[str] = set(printable)
    candidates: list[str] = [a for a in char_set if a in p_set]
    u_len: int = len(candidates)

    if not u_len:
        return ""

    random_characters: list[str] = (
        (candidates * (length // u_len))
        # Any remainders are randomly selected from the candidates
        + SystemRandom().sample(candidates, length % u_len)
    )
    SystemRandom().shuffle(random_characters)
    return "".join(random_characters)


def randstr_list(characters: str, array_size: int, start: int,
                 stop: int | None = None, step: int = 1) -> list[str]:
    """Return a list of random strings."""
    strings_list: list[str] = []
    for _ in range((array_size // 4) * 3):
        strings_list.append(
            randstr(characters, SystemRandom().randrange(start, stop, step))
        )

    strings_list += SystemRandom().sample(strings_list, array_size // 4)
    SystemRandom().shuffle(strings_list)
    return (strings_list)


if __name__ == "__main__":
    with open("randout.json", "w", encoding="utf8") as f:
        json.dump(
            randstr_list(
                printable, array_size=512 * 4, start=0, stop=10_000, step=100),
            f, indent=4
        )
