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
import __init__
from utilities.data_structures.doubly_linked_list_class import DoublyLinkedNode


class Solution:
    """LEETCODE."""

    def numberOfPairs(self, points: list[list[int]]) -> int:
        """Return number of possible Alice and Bob's private spaces."""
        hx: DoublyLinkedNode | None = None
        hy: DoublyLinkedNode | None = None
        for p in points:
            x_sorted = DoublyLinkedNode(tuple(p))
            hx = x_sorted.sorted_insert(hx, key=lambda nd: nd.val[0])
            y_sorted = DoublyLinkedNode(tuple(p))
            hy = y_sorted.sorted_insert(hy, key=lambda nd: nd.val[1])

        pairs: int = 0
        # Iterate through the sorted points and while counting valid points for Alice and Bob
        return pairs


if __name__ == "__main__":
    def test_numberOfPairs(list_of_points: list[list[int]]):
        """Test number of pairs."""

        sol: Solution = Solution()
        print(
            f"Pairs: {sol.numberOfPairs(list_of_points)} <> {list_of_points}")

    test_numberOfPairs([[0, 1], [4, 5], [10, 11], [2, 3], [4, 1], [6, 7],
                        [7, 7], [6, 3], [6, 7], [4, 1]])
