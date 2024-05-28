#!/usr/bin/python3
"""Module for blackset_whiteset."""

from __future__ import annotations
from collections.abc import Iterable, Iterator, Hashable, MutableSet, Set
from contextlib import suppress
from typing import TypeVar


T = TypeVar("T")


class StaticSet(MutableSet):
    """A Mutable Set of objects of the same type."""

    def __init__(self, items: Iterable[Hashable] = ()) -> None:
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

        self._check_types(items)
        self.__items = set(items)

    @property
    def oftype(self) -> type | None:
        """Return type of all objects in self."""
        return self.__oftype

    def __contains__(self, x: object) -> bool:
        """Return if x exists in self."""
        return x in self.__items

    def __isub__(self, other: Iterable) -> StaticSet:
        """Return self - other."""
        if other is self:
            self.clear()
        else:
            for value in other:
                self.discard(value)

        return self

    def __iter__(self) -> Iterator:
        """Return an iterator of self."""
        return iter(self.__items)

    def __ior__(self, other: Iterable[T]) -> StaticSet:
        """Return self | other."""
        self.update(other)
        return self

    def __ixor__(self, other: Iterable[T]) -> StaticSet:
        """Return self | other."""
        if other is self:
            self.clear()
        else:
            if not isinstance(other, Set):
                other = StaticSet(other)

            for value in other:
                if value in self:
                    self.discard(value)
                else:
                    self.add(value)

        return self

    def __len__(self) -> int:
        """Return length of self."""
        return len(self.__items)

    def __repr__(self) -> str:
        """Return official string representation of self."""
        if not self:
            return f"{self.__class__.__name__}()"

        return f"{self.__class__.__name__}({self.__items})"

    def _check_types(self, items: Iterable) -> None:
        """Raise TypeError if items is unsuitable for StaticSet operations."""
        if not isinstance(items, Iterable):
            raise TypeError(f"{type(items)} is not iterable.")

        if self.__oftype is None:
            with suppress(StopIteration):
                self.__oftype = type(next(iter(items)))

        if isinstance(items, StaticSet) and self.oftype != items.oftype:
            raise TypeError("items in both sets are not of the same types")

        if (
            self.__oftype is not None and
            not isinstance(items, StaticSet) and
            not all(isinstance(i, self.__oftype) for i in items)
        ):
            raise TypeError("all objects in iterable must be of the same type")

    def add(self, value: Hashable) -> None:
        """Add an item to self.

        Raises:
            TypeError: when value is not hashable.
                when value is not of the same type as items in self.
        """
        self._check_types([value])
        return self.__items.add(value)

    def clear(self) -> None:
        """Remove all items from self."""
        self.__items.clear()
        self.__oftype = None

    def copy(self) -> StaticSet:
        """Return a shallow copy of self."""
        return StaticSet(self.__items)

    def difference(self, *others: Iterable[Hashable]) -> StaticSet:
        """Return the difference of self and others as a StaticSet."""
        combined: frozenset[Hashable] = frozenset(
            item for iterable in others for item in iterable)
        return StaticSet(self - combined)

    def difference_update(self, *others: Iterable[Hashable]) -> None:
        """Update self with the difference of self and others.

        Raises:
            TypeError: when others is not an iterable.
                when objects in others are not hashable.
                when objects in others are not all of the same type.
        """
        combined: frozenset[Hashable] = frozenset(
            item for iterable in others for item in iterable)
        self._check_types(combined)
        self.__items.difference_update(combined)

    def discard(self, value: Hashable) -> None:
        """Remove an element from a self if it is a member."""
        return self.__items.discard(value)

    def intersection(self, *others: Iterable[Hashable]) -> StaticSet:
        """Return the intrsection of self and others as a new StaticSet."""
        combined: frozenset[Hashable] = frozenset(
            item for iterable in others for item in iterable)
        return StaticSet(self & combined)

    def intersection_update(self, *others: Iterable[Hashable]) -> None:
        """Update self with the difference of self and others.

        Raises:
            TypeError: when others is not an iterable.
                when objects in others are not hashable.
                when objects in others are not all of the same type.
        """
        combined: frozenset[Hashable] = frozenset(
            item for iterable in others for item in iterable)
        self._check_types(combined)
        self.__items.intersection_update(combined)

    def isdisjoint(self, other: Iterable[Hashable]) -> bool:
        """Return True if two sets have a null intersection."""
        return not self.intersection(other)

    def issubset(self, other: Iterable[Hashable]) -> bool:
        """Report whether another set contains this set."""
        return bool(self.difference(other))

    def issuperset(self, other: Iterable[Hashable]) -> bool:
        """Report whether this set contains another set."""
        return not (other - self)

    def pop(self) -> Hashable:
        """Return the popped value.  Raise KeyError if empty."""
        return self.__items.pop()

    def remove(self, value: Hashable) -> None:
        """Remove an element. If not a member, raise a KeyError."""
        self.__items.remove(value)

    def union(self, *others: Iterable[Hashable]) -> StaticSet:
        """Return the union of self and others as a new StaticSet."""
        combined: frozenset[Hashable] = frozenset(
            item
            for iterable in (self.__items, *others)
            for item in iterable
        )
        return StaticSet(combined)

    def update(self, *others: Iterable[Hashable]) -> None:
        """Update self with the union of itself and others.

        Raises:
            TypeError: when others is not an iterable.
                when objects in others are not hashable.
                when objects in others are not all of the same type.
        """
        combined: frozenset[Hashable] = frozenset(
            item for iterable in others for item in iterable)
        self._check_types(combined)
        self.__items.update(combined)


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
        print(f" '{i:}'", end="")
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
    # print("ss0 - l3: ", ss0 - l3)

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
