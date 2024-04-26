#!/usr/bin/python3
"""Module for linked_list_mid."""
# /usr/bin/env python3
"""Leetcode: find the middle of a linked list"""
from typing import Optional


class ListNode:
    """Linked List Structure"""

    def __init__(self, val=0, next=None) -> None:
        self.val = val
        self.next = next


class Solution:
    """LEETCODE"""

    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """Find the middle node of the linked list"""

        fast: Optional[ListNode] = head
        slow: Optional[ListNode] = head
        while (fast and fast.next):
            fast = fast.next.next
            slow = slow.next

        return slow


if __name__ == "__main__":
    def print_linkedlist(head: Optional[ListNode]) -> None:
        """Print a linked list"""

        if not head:
            print(None)
            return

        while (head):
            print(head.val, end=", " if head.next else "\n")
            head = head.next

    def main() -> None:
        head = ListNode()
        node = head
        for i in range(1, 5):
            node.next = ListNode(i)
            node = node.next

        print_linkedlist(head)
        print_linkedlist(Solution().middleNode(head))
        # print_linkedlist(ListNode())
        # print_linkedlist(Solution().middleNode(ListNode()))
        # print_linkedlist(None)
        # print_linkedlist(Solution().middleNode(None))

    main()
