"""Rough work."""

from __future__ import annotations
from collections.abc import Iterable, Iterator, Hashable, Set
from contextlib import suppress
from typing import TypeVar


T = TypeVar("T")


class StaticSet(Set):
    """A Mutable Set of same type objects."""

    def __init__(self, items: Iterable[Hashable] = ()) -> None:
        """Initialise a static set from iterable.

        Args:
            items: an iterable of hashable items.

        Raises:
            TypeError: when items is not an iterable.
                when objects in items are not hashable.
                when objects in items are not all of the same type.
        """
        if not isinstance(items, Iterable):
            raise TypeError("items should be an Iterable.")

        self.__oftype: type | None = None
        self._check_types(items)
        self.__items = set(items)

    @property
    def oftype(self) -> type | None:
        """Return type of all objects in self."""
        return self.__oftype

    def __contains__(self, x: object) -> bool:
        """Return if x exists in self."""
        return x in self.__items

    def __iter__(self) -> Iterator:
        """Return an iterator of self."""
        return iter(self.__items)

    def __ior__(self, other: Iterable[T]) -> StaticSet:
        """Return self | other."""
        if not isinstance(other, Iterable):
            return NotImplemented

        for value in other:
            self.add(value)

        return self

    def __iand__(self, other: Set[T]) -> StaticSet:
        """Return self & other."""
        for value in (self - other):
            self.discard(value)

        return self

    def __ixor__(self, other: Set[T]) -> StaticSet:
        """Return self | other."""
        if other is self:
            self.clear()
        else:
            if not isinstance(other, Set):
                other = self._from_iterable(other)

            for value in other:
                if value in self:
                    self.discard(value)
                else:
                    self.add(value)

        return self

    def __isub__(self, other: Set) -> StaticSet:
        """S."""
        if other is self:
            self.clear()
        else:
            for value in other:
                self.discard(value)

        return self

    def __len__(self) -> int:
        """Length."""
        return len(self.__items)

    def __repr__(self) -> str:
        """Repr."""
        return f"{self.__class__.__name__}({self.__items})"

    def _check_types(self, items: Iterable) -> None:
        """Check all objects in items are instances of self.oftype.

        Otherwise raise a TypeError.
        """
        if self.__oftype is None:
            with suppress(StopIteration):
                self.__oftype = type(next(iter(items)))

        if (
            self.__oftype is not None and
            not all(isinstance(i, self.__oftype) for i in items)
        ):
            raise TypeError("all objects in items must be of the same type")

    def add(self, value: Hashable) -> None:
        """Add."""
        self._check_types([value])
        return self.__items.add(value)

    def discard(self, value: Hashable) -> None:
        """Discard."""
        return self.__items.discard(value)

    def remove(self, value: Hashable) -> None:
        """Remove an element. If not a member, raise a KeyError."""
        self.__items.remove(value)

    def pop(self) -> Hashable:
        """Return the popped value.  Raise KeyError if empty."""
        other = iter(self)
        try:
            value = next(other)
        except StopIteration:
            raise KeyError from None

        self.discard(value)
        return value

    def clear(self) -> None:
        """Remove all items from Set."""
        self.__items = set()


if __name__ == "__main__":
    ss = StaticSet(["Zero", "One"])
    print(ss)
    print("isinstance(StaticSet, Hashable) = "
          f"{isinstance(ss, Hashable)}")
    ss.add("Two")
    ss.add("Three")
    print(ss)
    ss.discard("Zero")
    print(ss)
    ss ^= ["Zero", "One"]
    print(ss)
    print(ss ^ ["Three", "F"])
