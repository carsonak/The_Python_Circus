#!/usr/bin/python3
"""Module for blacklist_whitelist."""


from collections.abc import Hashable, Iterable, Iterator


class BlackWhitelist:
    """A blacklist/whitelist manager."""

    def __init__(self, items: Iterable):
        """Initialise a Black/Whitelist of items.

        Args:
            items: an iterable with hashable items to initilise List.
        """
        self.itemslist = items  # type: ignore
        self.__cache_items: frozenset = frozenset(self.__mut_items)

    @property
    def itemslist(self) -> frozenset:
        """An iterable of all the items in the List."""
        if self.__cache_items != self.__mut_items:
            self.__cache_items = frozenset(self.__mut_items)

        return self.__cache_items

    @itemslist.setter
    def itemslist(self, items: Iterable) -> None:
        """Hash and store items in a List.

        Args:
            items: an iterable with hashable items to initilise List.
        """
        if not isinstance(items, Iterable):
            raise TypeError("itemslist must be an iterable")

        self.__mut_items: set = {i for i in items}

    def __repr__(self) -> str:
        """Return an official string representation of this instance."""
        return f"{self.__class__.__name__}({self.__mut_items})"

    def __add__(self, other: "BlackWhitelist") -> "BlackWhitelist":
        """Return a union of self and other."""
        if isinstance(other, BlackWhitelist):
            t = BlackWhitelist(self.__mut_items.union(other.itemslist))
            return t
        else:
            return NotImplemented

    def __iadd__(self, other: "BlackWhitelist") -> None:
        """Update self with a union of self and other."""
        if isinstance(other, BlackWhitelist):
            self.__mut_items.update(other.itemslist)
        else:
            return NotImplemented

    def __sub__(self, other: "BlackWhitelist") -> "BlackWhitelist":
        """Return a difference of self and other."""
        if isinstance(other, BlackWhitelist):
            return BlackWhitelist(self.__mut_items.difference(other.itemslist))
        else:
            return NotImplemented

    def __isub__(self, other: "BlackWhitelist") -> None:
        """Update self with the difference of self and other."""
        if isinstance(other, BlackWhitelist):
            self.__mut_items.difference_update(other.itemslist)
        else:
            return NotImplemented

    def __and__(self, other: "BlackWhitelist") -> "BlackWhitelist":
        """Return an intersection of self and other."""
        if isinstance(other, BlackWhitelist):
            return BlackWhitelist(
                self.__mut_items.intersection(other.itemslist))
        else:
            return NotImplemented

    def __iand__(self, other: "BlackWhitelist") -> None:
        """Update self with an intersection of self and other."""
        if isinstance(other, BlackWhitelist):
            self.__mut_items.intersection_update(other.itemslist)
        else:
            return NotImplemented

    def __or__(self, other: "BlackWhitelist") -> "BlackWhitelist":
        """Return a union of self and other."""
        if isinstance(other, BlackWhitelist):
            return BlackWhitelist(self.__mut_items.union(other.itemslist))
        else:
            return NotImplemented

    def __ior__(self, other: "BlackWhitelist") -> None:
        """Update self with a union of self and other."""
        if isinstance(other, BlackWhitelist):
            self.__mut_items.update(other.itemslist)
        else:
            return NotImplemented

    def __eq__(self, other: object) -> bool:
        """Return self == other."""
        if isinstance(other, BlackWhitelist):
            return self.__mut_items == other.itemslist
        else:
            return NotImplemented

    def __lt__(self, other: object) -> bool:
        """Return self < other."""
        if isinstance(other, BlackWhitelist):
            return self.__mut_items < other.itemslist
        else:
            return NotImplemented

    def __len__(self) -> int:
        """Return number of items in the List."""
        return len(self.__mut_items)

    def __contains__(self, item: Hashable) -> bool:
        """Check if item exists in the List.

        Args:
            item: a hashable object.

        Returns:
            A bool depending on whether the item in found.

        Raises:
            TypeError: item is not Hashable.
        """
        return item in self.__mut_items

    def __iter__(self) -> Iterator:
        """Return an iterator for the List."""
        return iter(self.__mut_items)

    def add(self, items: Iterable[Hashable] | Hashable) -> None:
        """Add an items to the List.

        Args:
            items: an iterable of hashable objects or a single hashable object.
                Strings are not considered as iterables.
        """
        if isinstance(items, Iterable) and not isinstance(items, str):
            self.__mut_items.update(items)
        elif isinstance(items, Hashable):
            self.__mut_items.add(items)
        else:
            raise TypeError("items must be an iterable of hashable objects or"
                            " a hashable object")

    def discard(self, items: Iterable[Hashable] | Hashable) -> None:
        """Remove an items from the List.

        If items is not in the list nothing happens.

        Args:
            items: an iterable of hashable objects or a single hashable object.
                Strings are not considered as iterables.
        """
        if isinstance(items, Iterable) and not isinstance(items, str):
            for i in items:
                self.__mut_items.discard(i)
        elif isinstance(items, Hashable):
            self.__mut_items.discard(items)
        else:
            raise TypeError("items must be an iterable of hashable objects or"
                            " a hashable object")

    def clear(self) -> None:
        """Clear all items from the List."""
        self.__mut_items.clear()
