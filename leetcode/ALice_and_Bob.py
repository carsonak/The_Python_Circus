#!/usr/bin/python3
"""LEETCODE: 3025. Find the Number of Ways to Place People I

From a list of points on a cartesian plane determine every pair of points
(Bob and Alice), such that the pair can be secluded with an axis aligned
rectangle or line.
Alice must be on the upper left corner while Bob on the lower right corner.

points[i] = [x, y]

Constraints:
    2 <= n <= 50
    points[i].length == 2
    0 <= points[i][0], points[i][1] <= 50
    All points[i] are distinct.
"""
from typing import Callable, Optional


class DoublyLinkedNode:
    """A doubly linked list node."""

    def __init__(self, val=None, next: Optional["DoublyLinkedNode"] = None,
                 prev: Optional["DoublyLinkedNode"] = None) -> None:
        """Initialise instance variables.

        Args:
            val[any] - data to be held in the list.
            next[DoublyLinkedNode | None] - the next node in the list.
            prev[DoublyLinkedNode | None] - the previous node in the list.
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

    def sort_insert(self, head: Optional["DoublyLinkedNode"],
                    key: Callable[["DoublyLinkedNode"], int] | None = None) -> None:
        """Insert instance node in a sorted linked list."""

        if isinstance(head, self.__class__):
            walk: "DoublyLinkedNode" = head
            if key is None:
                while walk.next and self >= walk:
                    walk = walk.next
            else:
                while walk.next and key(self) >= key(walk):
                    walk = walk.next

            if walk.next is None and (self >= walk if key is None else key(self) >= key(walk)):
                self.insert_after(walk)
            else:
                self.insert_before(walk)

        elif head is None:
            head = self
        else:
            raise TypeError(
                f"head must be an instance of {type(self)} or None")

        while head.prev is not None:
            head = head.prev

    def remove(self):
        """Remove instance node from linked list."""
        if self.prev:
            self.prev.next = self.next

        if self.next:
            self.next.prev = self.prev

        self.next = None
        self.prev = None

    def __gt__(self, __other: object) -> bool:
        if isinstance(__other, self.__class__):
            return self.val > __other.val
        else:
            return NotImplemented

    def __ge__(self, __other: object) -> bool:
        if isinstance(__other, self.__class__):
            return self.val >= __other.val
        else:
            return NotImplemented

    def __eq__(self, __other: object) -> bool:
        if isinstance(__other, self.__class__):
            return self.val == __other.val
        else:
            return NotImplemented

    def __hash__(self) -> int:
        return hash(self.val)


class Solution:
    """LEETCODE."""

    def numberOfPairs(self, points: list[list[int]]) -> int:
        """Return number of possible Alice and Bob's private spaces."""
        head: DoublyLinkedNode = DoublyLinkedNode(tuple(points[1]))
        for p in points[1:]:
            temp = DoublyLinkedNode(tuple(p))
            temp.sort_insert(head)
            while head.prev is not None:
                head = head.prev

        return 0


if __name__ == "__main__":
    def test_numberOfPairs(list_of_points: list[list[int]]):
        """Test number of pairs."""

        sol: Solution = Solution()
        print(
            f"Pairs: {sol.numberOfPairs(list_of_points)} <> {list_of_points}")

    test_numberOfPairs([[0, 1], [4, 5], [10, 11], [2, 3], [4, 1], [6, 7],
                        [7, 7], [6, 3], [6, 7], [4, 1]])
