#!/usr/bin/python3
"""Module for Doubly Linked Node class."""
from collections.abc import Hashable
from typing import Callable, Optional


class DoublyLinkedNode:
    """A doubly linked list node."""

    def __init__(self, val: Hashable | None = None, next: Optional["DoublyLinkedNode"] = None,
                 prev: Optional["DoublyLinkedNode"] = None) -> None:
        """Initialise instance variables.

        Args:
            val (any): data to be held in the list.
            next (DoublyLinkedNode | None): the next node in the list.
            prev (DoublyLinkedNode | None): the previous node in the list.
        """
        self.val = val
        self.next = next
        self.prev = prev

    @property
    def next(self) -> Optional["DoublyLinkedNode"]:
        return self.__next

    @next.setter
    def next(self, next_node: Optional["DoublyLinkedNode"]) -> None:
        """Set the value of next."""
        if not isinstance(next_node, (self.__class__, None.__class__)):
            raise TypeError(f"next node must be an instance of {type(self)}")
        else:
            self.__next = next_node

    @property
    def prev(self) -> Optional["DoublyLinkedNode"]:
        return self.__prev

    @prev.setter
    def prev(self, prev_node: Optional["DoublyLinkedNode"]) -> None:
        """Set the value of prev."""
        if not isinstance(prev_node, (self.__class__, None.__class__)):
            raise TypeError(
                f"previous node must be an instance of {type(self)}")
        else:
            self.__prev = prev_node

    def insert_before(self, node: "DoublyLinkedNode") -> None:
        """Insert instance node before 'node'."""
        if not isinstance(node, self.__class__):
            raise TypeError(f"node must be an instance of {type(self)}")

        self.next = node
        self.prev = node.prev
        if node.prev:
            node.prev.next = self

        node.prev = self

    def insert_after(self, node: "DoublyLinkedNode") -> None:
        """Insert instance node after 'node'."""
        if not isinstance(node, self.__class__):
            raise TypeError(f"node must be an instance of {type(self)}")

        self.next = node.next
        self.prev = node
        if node.next:
            node.next.prev = self

        node.next = self

    def sorted_insert(self, head: Optional["DoublyLinkedNode"],
                      key: Callable[["DoublyLinkedNode"], int] | None = None) -> "DoublyLinkedNode":
        """Insert instance node in a sorted linked list."""

        if isinstance(head, self.__class__):
            walk: "DoublyLinkedNode" = head
            if key is None:
                while walk.next and walk <= self:
                    walk = walk.next
            else:
                while walk.next and key(walk) <= key(self):
                    walk = walk.next

            if walk.next is None and (walk <= self if key is None else key(walk) <= key(self)):
                self.insert_after(walk)
            else:
                self.insert_before(walk)

        elif head is None:
            head = self
        else:
            raise TypeError(
                f"head must be an instance of {type(self)} or None")

        while head.prev:
            head = head.prev

        return head

    def remove(self):
        """Remove instance node from linked list."""
        if self.prev:
            self.prev.next = self.next

        if self.next:
            self.next.prev = self.prev

        self.next = None
        self.prev = None

    @classmethod
    def display(cls, head: Optional["DoublyLinkedNode"]) -> None:
        """Print a string of all the items in a linked list.

        Args:
            head (DoublyLinkedNode): head of the linked list.
        """
        if not isinstance(head, (cls, None.__class__)):
            raise TypeError(
                f"head must be an instance of {cls.__name__} or None")

        llst: str = ""
        while head:
            llst += str(head.val) + " -> "
            head = head.next

        print(llst.strip(" -> ") if llst else None)

    def __gt__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.val > other.val
        else:
            return NotImplemented

    def __ge__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.val >= other.val
        else:
            return NotImplemented

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.val == other.val
        else:
            return NotImplemented

    def __hash__(self) -> int:
        return hash(self.val)
