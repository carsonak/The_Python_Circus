#!/usr/bin/python3
"""Module for blacklist_whitelist."""


from collections.abc import Iterable, Iterator, Hashable


class BlackWhitelist:
    """A blacklist/whitelist manager."""

    def __init__(self, items: Iterable[Hashable]) -> None:
        """Initialise a Black/Whitelist of items.

        Args:
            items: an iterable with hashable items to initilise List.
        """
        self.itemslist = items

    @property
    def itemslist(self) -> Iterable:
        """An iterable of all the items in the List."""
        return iter(self)

    @itemslist.setter
    def itemslist(self, items: Iterable[Hashable]) -> None:
        """Hash and store items in a List.

        Args:
            items: an iterable with hashable items to initilise List.
        """
        if isinstance(items, Iterable):
            self.__itemList: set = set([i for i in items])
        else:
            raise TypeError("itemslist must be an iterable")

    def __str__(self) -> str:
        """Return a string of items in the List."""
        return str(self.__itemList)

    def __repr__(self) -> str:
        """Return an official string representation of this instance."""
        return f"{self.__class__.__name__}({self.__itemList})"

    def __add__(self, other: "BlackWhitelist") -> "BlackWhitelist":
        """Return a union of self and other."""
        if isinstance(other, BlackWhitelist):
            t = BlackWhitelist(self.__itemList.union(other.__itemList))
            return t
        else:
            return NotImplemented

    def __iadd__(self, other: "BlackWhitelist") -> None:
        """Update self with a union of self and other."""
        if isinstance(other, BlackWhitelist):
            self.__itemList.update(other.__itemList)
        else:
            return NotImplemented

    def __sub__(self, other: "BlackWhitelist") -> "BlackWhitelist":
        """Return a difference of self and other."""
        if isinstance(other, BlackWhitelist):
            t = BlackWhitelist(self.__itemList.difference(other.__itemList))
            return t
        else:
            return NotImplemented

    def __isub__(self, other: "BlackWhitelist") -> None:
        """Update self with the difference of self and other."""
        if isinstance(other, BlackWhitelist):
            self.__itemList.difference_update(other.__itemList)
        else:
            return NotImplemented

    def __and__(self, other: "BlackWhitelist") -> "BlackWhitelist":
        """Return an intersection of self and other."""
        if isinstance(other, BlackWhitelist):
            t = BlackWhitelist(self.__itemList & other.__itemList)
            return t
        else:
            return NotImplemented

    def __iand__(self, other: "BlackWhitelist") -> None:
        """Update self with an intersection of self and other."""
        if isinstance(other, BlackWhitelist):
            self.__itemList.intersection(other.__itemList)
        else:
            return NotImplemented

    def __or__(self, other: "BlackWhitelist") -> "BlackWhitelist":
        """Return a union of self and other."""
        if isinstance(other, BlackWhitelist):
            t = BlackWhitelist(self.__itemList.union(other.__itemList))
            return t
        else:
            return NotImplemented

    def __ior__(self, other: "BlackWhitelist") -> None:
        """Update self with a union of self and other."""
        if isinstance(other, BlackWhitelist):
            self.__itemList.update(other.__itemList)
        else:
            return NotImplemented

    def __eq__(self, other: object) -> bool:
        """Return self == other."""
        if isinstance(other, BlackWhitelist):
            return self.__itemList == other.__itemList
        else:
            return NotImplemented

    def __lt__(self, other: object) -> bool:
        """Return self < other."""
        if isinstance(other, BlackWhitelist):
            return self.__itemList < other.__itemList
        else:
            return NotImplemented

    def __len__(self) -> int:
        """Return number of items in the List."""
        return len(self.__itemList)

    def __contains__(self, item: Hashable) -> bool:
        """Check if item exists in the List."""
        return item in self.__itemList

    def __iter__(self) -> Iterator:
        """Return an iterator for the List."""
        return iter(self.__itemList)

    def add(self, item: Hashable | Iterable[Hashable]) -> None:
        """Add an items to the List.

        Args:
            item: a hashable object or an iterable of hashable objects.
        """
        if isinstance(item, Hashable) and not isinstance(item, Iterable):
            self.__itemList.add(item)
        elif isinstance(item, Iterable):
            self.__itemList.update(item)
        else:
            raise TypeError("item must be a hashable object or"
                            "an iterable of hashable objects")

    def discard(self, item: Hashable | Iterable[Hashable]) -> None:
        """Remove an items from the List.

        If item is not in the list nothing happens.

        Args:
            item: a hashable object or an iterable of Hashable objects.
        """
        if isinstance(item, Hashable) and not isinstance(item, Iterable):
            self.__itemList.discard(item)
        elif isinstance(item, Iterable):
            for i in item:
                self.__itemList.discard(i)
        else:
            raise TypeError("item must be a hashable object or"
                            "an iterable of hashable objects")

    def clear(self) -> None:
        """Clear all items from the List."""
        self.__itemList.clear()
