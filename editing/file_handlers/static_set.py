#!/usr/bin/python3
"""Module for blackset_whiteset."""

from collections.abc import Hashable, Iterable, Iterator
from contextlib import suppress
from typing import Union


class StaticSet:
    """A set of only one type items."""

    def __init__(self, item: None | Hashable = None):
        """Initialise a StaticSet.

        Args:
            item: a Hashable to initialise the StaticSet or None.
        """
        self.items = item  # type: ignore

    @property
    def items(self) -> Iterator:
        """An iterator of all the items in the StaticSet."""
        return iter(self)

    @items.setter
    def items(self, item: None | Hashable) -> None:
        """Initialise a Static set.

        Args:
            item: an Hashable or None.

        Raises:
            TypeError: item is not Hashable or None.
        """
        self.__mut_items: set = set()
        self.__oftype: type | None = None
        if item is not None:
            self.__oftype = type(item)
            self.__mut_items.add(item)

    @property
    def oftype(self) -> type | None:
        """Type of all items in the set."""
        return self.__oftype

    def __repr__(self) -> str:
        """Return an official string representation of this instance."""
        return f"{self.__class__.__name__}({self.__mut_items})"

    def __add__(
            self, other: Union[set, frozenset, "StaticSet"]) -> "StaticSet":
        """Return a union of self and other."""
        ss: StaticSet = StaticSet()
        if isinstance(other, StaticSet):
            if (
                self.__oftype and other.__oftype and
                self.__oftype != other.__oftype
            ):
                raise ValueError("Sets contain items of different types")

            ss.update(self.__mut_items.union(other.__mut_items))
            return ss
        elif isinstance(other, (set, frozenset)):
            ss.update(self.__mut_items.union(other))
            return ss
        else:
            return NotImplemented

    def __iadd__(self, other: Union[set, frozenset, "StaticSet"]) -> None:
        """Update self with a union of self and other."""
        if isinstance(other, StaticSet):
            if (
                self.__oftype and other.__oftype and
                self.__oftype != other.__oftype
            ):
                raise ValueError("Sets contain items of different types")

            self.__mut_items.update(other.__mut_items)
        elif isinstance(other, (set, frozenset)):
            ss: StaticSet = StaticSet()
            ss.update(self.__mut_items.union(other))
            self.__mut_items = ss.__mut_items
        else:
            return NotImplemented

    def __sub__(
            self, other: Union[set, frozenset, "StaticSet"]) -> "StaticSet":
        """Return a difference of self and other."""
        ss: StaticSet = StaticSet()
        if isinstance(other, StaticSet):
            if (
                self.__oftype and other.__oftype and
                self.__oftype != other.__oftype
            ):
                raise ValueError("Sets contain items of different types")

            ss.update(self.__mut_items.difference(other.__mut_items))
            return ss
        elif isinstance(other, (set, frozenset)):
            ss.update(self.__mut_items.difference(other))
            return ss
        else:
            return NotImplemented

    def __isub__(self, other: Union[set, frozenset, "StaticSet"]) -> None:
        """Update self with the difference of self and other."""
        if isinstance(other, StaticSet):
            if (
                self.__oftype and other.__oftype and
                self.__oftype != other.__oftype
            ):
                raise ValueError("Sets contain items of different types")

            self.__mut_items.difference_update(other.__mut_items)
        elif isinstance(other, (set, frozenset)):
            ss: StaticSet = StaticSet()
            ss.update(self.__mut_items.difference(other))
            self.__mut_items = ss.__mut_items
        else:
            return NotImplemented

    def __and__(
            self, other: Union[set, frozenset, "StaticSet"]) -> "StaticSet":
        """Return an intersection of self and other."""
        ss: StaticSet = StaticSet()
        if isinstance(other, StaticSet):
            if (
                self.__oftype and other.__oftype and
                self.__oftype != other.__oftype
            ):
                raise ValueError("Sets contain items of different types")

            ss.update(self.__mut_items.intersection(other.__mut_items))
            return ss
        elif isinstance(other, (set, frozenset)):
            ss.update(self.__mut_items.intersection(other))
            return ss
        else:
            return NotImplemented

    def __iand__(self, other: Union[set, frozenset, "StaticSet"]) -> None:
        """Update self with an intersection of self and other."""
        if isinstance(other, StaticSet):
            if (
                self.__oftype and other.__oftype and
                self.__oftype != other.__oftype
            ):
                raise ValueError("Sets contain items of different types")

            self.__mut_items.intersection_update(other.__mut_items)
        elif isinstance(other, (set, frozenset)):
            ss: StaticSet = StaticSet()
            ss.update(self.__mut_items.intersection(other))
            self.__mut_items = ss.__mut_items
        else:
            return NotImplemented

    def __or__(self, other: Union[set, frozenset, "StaticSet"]) -> "StaticSet":
        """Return a union of self and other."""
        ss: StaticSet = StaticSet()
        if isinstance(other, StaticSet):
            if (
                self.__oftype and other.__oftype and
                self.__oftype != other.__oftype
            ):
                raise ValueError("Sets contain items of different types")

            ss.update(self.__mut_items.union(other.__mut_items))
            return ss
        elif isinstance(other, (set, frozenset)):
            ss.update(self.__mut_items.union(other))
            return ss
        else:
            return NotImplemented

    def __ior__(self, other: Union[set, frozenset, "StaticSet"]) -> None:
        """Update self with a union of self and other."""
        if isinstance(other, StaticSet):
            if (
                self.__oftype and other.__oftype and
                self.__oftype != other.__oftype
            ):
                raise ValueError("Sets contain items of different types")

            self.__mut_items.update(other.__mut_items)
        elif isinstance(other, (set, frozenset)):
            self.__mut_items.update(other)
        else:
            return NotImplemented

    def __eq__(self, other: object) -> bool:
        """Return self == other."""
        if isinstance(other, StaticSet):
            return self.__mut_items == other.__mut_items
        else:
            return self == other

    def __lt__(self, other: object) -> bool:
        """Return self < other."""
        if isinstance(other, StaticSet):
            return self.__mut_items < other.__mut_items
        else:
            return self < other

    def __le__(self, other: object) -> bool:
        """Return self <= other."""
        if isinstance(other, StaticSet):
            return self.__mut_items <= other.__mut_items
        else:
            return self <= other

    def __len__(self) -> int:
        """Return number of items in the set."""
        return len(self.__mut_items)

    def __contains__(self, item: Hashable) -> bool:
        """Check if item exists in the set.

        Args:
            item: a hashable object.

        Returns:
            A bool depending on whether the item in found.

        Raises:
            TypeError: item is not Hashable.
        """
        return item in self.__mut_items

    def __iter__(self) -> Iterator:
        """Return an iterator for the set."""
        return iter(self.__mut_items)

    def add(self, item: Hashable) -> None:
        """Add an item to the set.

        Args:
            item: a hashable object.

        Raises:
            TypeError: item is not an instance of same type as items in set.
                item is not hashable.
        """
        if self.__oftype is None:
            self.__oftype = type(item)

        if not isinstance(item, self.__oftype):
            raise TypeError(
                f"Item <{item}> is not an instance of {self.__oftype}")

        self.__mut_items.add(item)

    def clear(self) -> None:
        """Clear all items from the set."""
        self.__mut_items.clear()

    def discard(self, item: Hashable) -> None:
        """Remove an item from the set.

        If item is not in the set nothing happens.

        Args:
            item: a hashable object.

        Raises:
            TypeError: item is not Hashable
        """
        self.__mut_items.discard(item)

    def difference(self, other: "StaticSet") -> "StaticSet":
        """Return a difference of self and other."""
        if not isinstance(other, StaticSet):
            raise TypeError("Other is not an instance of StaticSet")

        if (
            self.__oftype and other.__oftype and
            self.__oftype != other.__oftype
        ):
            raise ValueError("Sets contain items of different types")

        ss: StaticSet = StaticSet()
        ss.update(self.__mut_items.difference(other.__mut_items))
        return ss

    def difference_update(self, other: "StaticSet") -> None:
        """Update self with a difference of self and other."""
        if not isinstance(other, StaticSet):
            raise TypeError("Other is not an instance of StaticSet")

        if (
            self.__oftype and other.__oftype and
            self.__oftype != other.__oftype
        ):
            raise ValueError("Sets contain items of different types")

        ss: StaticSet = StaticSet()
        ss.update(self.__mut_items.difference(other.__mut_items))
        self.__mut_items = ss.__mut_items

    def intersection(self, other: "StaticSet") -> "StaticSet":
        """Return an intersection of self and other."""
        if not isinstance(other, StaticSet):
            raise TypeError("Other is not an instance of StaticSet")

        if (
            self.__oftype and other.__oftype and
            self.__oftype != other.__oftype
        ):
            raise ValueError("Sets contain items of different types")

        ss: StaticSet = StaticSet()
        ss.update(self.__mut_items.intersection(other.__mut_items))
        return ss

    def intersection_update(self, other: "StaticSet") -> None:
        """Return an intersection of self and other."""
        if not isinstance(other, StaticSet):
            raise TypeError("Other is not an instance of StaticSet")

        if (
            self.__oftype and other.__oftype and
            self.__oftype != other.__oftype
        ):
            raise ValueError("Sets contain items of different types")

        ss: StaticSet = StaticSet()
        ss.update(self.__mut_items.intersection(other.__mut_items))
        self.__mut_items = ss.__mut_items

    def update(self, items: Iterable[Hashable]) -> None:
        """Update set with items in the set.

        Args:
            items: an Iterable of hashable objects.

        Raises:
            TypeError: items is not an iterable
                items in iterable are not all instances of same type.
                items in iterable are not all hashable.
        """
        iter_items: Iterator = iter(items)
        if self.__oftype is None:
            with suppress(StopIteration):
                i: Hashable = next(iter_items)
                self.__oftype = type(i)
                self.__mut_items.add(i)

        with suppress(StopIteration):
            while items is not None and True:
                i = next(iter_items)
                if self.__oftype and not isinstance(i, self.__oftype):
                    raise TypeError(
                        f"Item <{i}> is not an instance of {self.__oftype}")

                self.__mut_items.add(i)
