#!/usr/bin/python3
"""Module for blackset_whiteset."""

from __future__ import annotations
from collections.abc import Iterable, Iterator, Hashable, MutableSet, Set
from contextlib import suppress
from typing import TypeVar

_SSHashable = TypeVar("_SSHashable", bound=Hashable)
_GenHashable = TypeVar("_GenHashable", bound=Hashable)


class StaticSet(MutableSet[_SSHashable]):
    """A Mutable Set of objects of the same type."""

    def __init__(self, items: Iterable[_SSHashable] = ()) -> None:
        """Initialise a static set from iterable.

        Args:
            items: an iterable of hashable items.

        Raises:
            TypeError: when items is not an iterable.
                when objects in items are not hashable.
                when objects in items are not all of the same type.
        """
        self.__oftype: type | None = None
        if isinstance(items, Iterator):
            items = frozenset(items)

        self.__oftype = self._check_types(items, self.__oftype)
        self.__items = set(items)

    @property
    def _items(self) -> set[_SSHashable]:
        """Return the internal set being used."""
        return self.__items

    @property
    def oftype(self) -> type | None:
        """Return type of all objects in self."""
        return self.__oftype

    def __contains__(self, x: Hashable) -> bool:
        """Return if x exists in self."""
        return x in self.__items

    def __isub__(
            self, other: Iterable[Hashable]) -> StaticSet[_SSHashable]:
        """Return self - other."""
        if other is self:
            self.clear()
        else:
            self.difference_update(other)

        return self

    def __iter__(self) -> Iterator[_SSHashable]:
        """Return an iterator of self."""
        return iter(self.__items)

    def __ior__(self, other: Iterable[Hashable]) -> StaticSet[_SSHashable]:
        """Return self | other."""
        self.update(other)
        return self

    def __ixor__(self, other: Iterable[Hashable]) -> StaticSet[_SSHashable]:
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

    def __len__(self) -> int:
        """Return length of self."""
        return len(self.__items)

    def __or__(self, other: Iterable[Hashable]) -> StaticSet[_SSHashable]:
        """Return self | other."""
        if not isinstance(other, Iterable):
            return NotImplemented

        return self.union(other)

    def __repr__(self) -> str:
        """Return official string representation of self."""
        if not self:
            return f"{self.__class__.__name__}()"

        return f"{self.__class__.__name__}({self.__items})"

    def __sub__(self, other: Iterable[Hashable]) -> StaticSet[_SSHashable]:
        """Return self - other."""
        if not isinstance(other, Iterable):
            return NotImplemented

        return self.difference(other)

    def __xor__(self, other: Iterable[Hashable]) -> StaticSet[_SSHashable]:
        """Return self ^ other."""
        if not isinstance(other, Set):
            if not isinstance(other, Iterable):
                return NotImplemented

            other = self._from_iterable(other)

        return (self - other) | (other - self)

    @staticmethod
    def _check_types(items: Iterable, oftype: type | None) -> type | None:
        """Check that objects in Iterable are all of same type.

        Args:
            items: an iterable of objects.
            oftype: a type used to check all objects in iterable against.
                if None, the type of the first object in the iterable will be
                used.

        Raises:
            TypeError: when items is not an iterable.
                when objects in the iterable to not match the type.
        """
        if not isinstance(items, Iterable):
            raise TypeError(f"{type(items)} is not iterable.")

        if isinstance(items, Iterator):
            items = (*items,)

        if oftype is None:
            with suppress(StopIteration):
                oftype = type(next(iter(items)))

        if isinstance(items, StaticSet) and oftype != items.oftype:
            raise TypeError("items in both sets are not of the same types")

        if (
            oftype is not None and
            not isinstance(items, StaticSet) and
            not all(type(i) is oftype for i in items)
        ):
            raise TypeError("all objects in iterable must be of the same type")

        return oftype

    @classmethod
    def _from_iterable(
            cls, items: Iterable[_GenHashable]) -> StaticSet[_GenHashable]:
        """Construct an instance of the class from any iterable input."""
        return cls(items)

    def add(self, value: _SSHashable) -> None:
        """Add an item to self.

        Raises:
            TypeError: when value is not of the same type as items in self.
                when value is not hashable.
        """
        self.__oftype = self._check_types([value], self.oftype)
        return self.__items.add(value)

    def clear(self) -> None:
        """Remove all items from self."""
        self.__items.clear()
        self.__oftype = None

    def copy(self) -> StaticSet[_SSHashable]:
        """Return a shallow copy of self."""
        return self._from_iterable(self.__items)

    def difference(
            self, *others: Iterable[Hashable]) -> StaticSet[_SSHashable]:
        """Return the difference of self and other sets.

        Raises:
            TypeError: when an object in others is not an iterable.
                when an item is not hashable.
                when an item is of a different type.
        """
        return self._from_iterable(self.__items.difference(*others))

    def difference_update(self, *others: Iterable[Hashable]) -> None:
        """Update self with the difference of self and other sets.

        Raises:
            TypeError: when an object in others is not an iterable.
                when an item is not hashable.
                when an item is of a different type.
        """
        combined: StaticSet = self.difference(*others)
        self.__items = combined.__items
        self.__oftype = combined.oftype

    def discard(self, value: _SSHashable) -> None:
        """Remove value from a self if it is a member, else do nothing."""
        self.__items.discard(value)
        if not self.__items:
            self.__oftype = None

    def intersection(
            self, *others: Iterable[_SSHashable]) -> StaticSet[_SSHashable]:
        """Return the intersection of self and other sets.

        Raises:
            TypeError: when an object in others is not an iterable.
                when an item is not hashable.
                when an item is of a different type.
        """
        return self._from_iterable(self.__items.intersection(*others))

    def intersection_update(self, *others: Iterable[_SSHashable]) -> None:
        """Update self with the intersection of self and other sets.

        Raises:
            TypeError: when an object in others is not an iterable.
                when an item is not hashable.
                when an item is of a different type.
        """
        combined: StaticSet = self.intersection(*others)
        self.__items = combined.__items
        self.__oftype = combined.oftype

    def isdisjoint(self, other: Iterable[_SSHashable]) -> bool:
        """Return True if two sets have a null intersection."""
        return not self.intersection(other)

    def issubset(self, other: Iterable[Hashable]) -> bool:
        """Report whether another set contains this set."""
        return bool(self.difference(other))

    def issuperset(self, other: Iterable[Hashable]) -> bool:
        """Report whether this set contains another set."""
        if not isinstance(other, Iterable):
            return NotImplemented

        if not isinstance(other, Set):
            other = self._from_iterable(other)

        return not (other - self)

    def pop(self) -> _SSHashable:
        """Return the popped value. Raise KeyError if empty."""
        popped: _SSHashable = self.__items.pop()
        if not self.__items:
            self.__oftype = None

        return popped

    def remove(self, value: _SSHashable) -> None:
        """Remove value. If not a member, raise a KeyError."""
        self.__items.remove(value)
        if not self.__items:
            self.__oftype = None

    def symmetric_difference(
            self, *others: Iterable[_SSHashable]) -> StaticSet[_SSHashable]:
        """Return the symmetric_difference of self and others.

        Raises:
            TypeError: when an object in others is not an iterable.
                when an item is not hashable.
                when an item is of a different type.
        """
        return self._from_iterable(self.__items.symmetric_difference(*others))

    def symmetric_difference_update(
            self, *others: Iterable[_SSHashable]) -> None:
        """Update self with the symmetric_difference of self and others.

        Raises:
            TypeError: when an object in others is not an iterable.
                when an item is not hashable.
                when an item is of a different type.
        """
        combined: StaticSet = self.symmetric_difference(*others)
        self.__items = combined.__items
        self.__oftype = combined.oftype

    def union(self, *others: Iterable[_SSHashable]) -> StaticSet[_SSHashable]:
        """Return the union of self and others as a new StaticSet.

        Raises:
            TypeError: when an object in others is not an iterable.
                when an item is not hashable.
                when an item is of a different type.
        """
        return self._from_iterable(self.__items.union(*others))

    def update(self, *others: Iterable[_SSHashable]) -> None:
        """Update self with the union of itself and others.

        Raises:
            TypeError: when an object in others is not an iterable.
                when an item is not hashable.
                when an item is of a different type.
        """
        combined: StaticSet[_SSHashable] = self.union(*others)
        self.__items = combined.__items
        self.__oftype = combined.oftype


if __name__ == "__main__":
    l0 = ["Zero", "One", "Two", "Three"]
    print(f"l0 = {l0}")
    ss0 = StaticSet(l0)
    print(f"ss0 = {ss0}")
    l3 = ["Three", "Four", "Five", "Six", "Seven"]
    print(f"l3 = {l3}")
    ss3 = StaticSet(l3)
    print(f"{len(ss3)} items in ss3:", end="")
    for i in ss3:
        print(" '{}'".format(i), end="")
    else:
        print()

    print()

    print("ss0 & ss0: ", ss0 & ss0)
    print("ss0 & ss3: ", ss0 & ss3)
    print("ss0 & l3: ", ss0 & l3)

    print()

    print("ss0 | ss0: ", ss0 | ss0)
    print("ss0 | ss3: ", ss0 | ss3)
    print("ss0 | l3: ", ss0 | l3)

    print()

    print("ss0 ^ ss0: ", ss0 ^ ss0)
    print("ss0 ^ ss3: ", ss0 ^ ss3)
    print("ss0 ^ l3: ", ss0 ^ l3)

    print()

    print("ss0 == ss0: ", ss0 == ss0)
    print("ss0 == ss3: ", ss0 == ss3)
    # print("ss0 == l0: ", ss0 == l0)

    print()

    print("ss0 != ss0: ", ss0 != ss0)
    print("ss0 != ss3: ", ss0 != ss3)
    # print("ss0 != l0: ", ss0 != l0)

    print()

    print("ss0 >= ss0: ", ss0 >= ss0)
    print("ss0 >= ss3: ", ss0 >= ss3)
    # print("ss0 >= l3: ", ss0 >= l3)

    print()

    print("ss0 > ss0: ", ss0 > ss0)
    print("ss0 > ss3: ", ss0 > ss3)
    # print("ss0 > l3: ", ss0 > l3)

    print()

    print("ss0 <= ss0: ", ss0 <= ss0)
    print("ss0 <= ss3: ", ss0 <= ss3)
    # print("ss0 <= l3: ", ss0 <= l3)

    print()

    print("ss0 < ss0: ", ss0 < ss0)
    print("ss0 < ss3: ", ss0 < ss3)
    # print("ss0 < l3: ", ss0 < l3)

    print()

    ss_calc = ss0 - ss0
    print("ss0 - ss0: ", ss_calc)
    ss_calc = ss0 - ss3
    print("ss0 - ss3: ", ss_calc)
    print("ss0 - l3: ", ss0 - l3)

    print()

    print("'Zero' in ss0: ", "Zero" in ss0)
    ss0.add("Four")
    print("ss0.add('Four'): ", ss0)
    print("_ := ss0.copy(): ", _ := ss0.copy())
    ss0.discard("Zero")
    print("ss0.discard('Zero'): ", ss0)
    print("ss0.pop(): ", ss0.pop())
    ss3.remove("Three")
    print("ss3.remove('Three')", ss3)
    print("ss0.union(ss3): ", ss0.union(ss3))
    ss0.clear()
    print("ss0.clear(): ", ss0)
    ss0.update(l0)
    print("ss0.update(l0): ", ss0)
    print("ss3.issuperset(l0): ", ss3.issuperset(l0))
    print("ss0.issuperset(l0): ", ss0.issuperset(l0))
