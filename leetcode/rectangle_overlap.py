#!/usr/bin/python3
"""LEETCODE: Rectangle Overlap.

Given two axis-aligned rectangles rec1 and rec2, return true if they overlap,
otherwise false.
An axis-aligned rectangle has its top and bottom edges parallel to the X-axis,
and its left and right edges parallel to the Y-axis.
The rectangle is represented as a list [x1, y1, x2, y2], where (x1, y1) is the
coordinate of its bottom-left corner, and (x2, y2) is the coordinate of its
top-right corner.
"""


class Solution:
    """LEETCODE."""

    def isRectangleOverlap(self, rec1: list[int], rec2: list[int]) -> bool:
        """Determine if two rectangles overlap."""
        # Get the right-most left edge of the two rectangles
        left: int = max(rec1[0], rec2[0])
        # Get the left-most right edge
        right: int = min(rec1[2], rec2[2])

        # Get the top-most bottom edge
        bottom: int = max(rec1[1], rec2[1])
        # Get the bottom-most top edge
        top: int = min(rec1[3], rec2[3])

        return left < right and bottom < top


if __name__ == "__main__":
    def test_isRectangleOverlap(rec1: list[int], rec2: list[int]) -> None:
        """Test isRectangleOverlap."""
        sol = Solution()
        if sol.isRectangleOverlap(rec1, rec2):
            print(f"{rec1} & {rec2}: True")
        else:
            print(f"{rec1} & {rec2}: False")

    test_isRectangleOverlap([0, 0, 2, 2], [1, 1, 3, 3])  # True
    test_isRectangleOverlap([1, 1, 3, 3], [1, 1, 3, 3])  # True
    test_isRectangleOverlap([0, 0, 1, 1], [1, 0, 2, 1])  # False
    test_isRectangleOverlap([0, 0, 2, 2], [2, 2, 3, 3])  # False
    test_isRectangleOverlap([-1, 0, 1, 1], [0, -1, 0, 1])  # False
