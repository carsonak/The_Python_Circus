#!/usr/bin/python3
"""LEETCODE: Rectangle Area.

Find the total area covered by two rectangles 'a' and 'b' on a cartesian plane.
The recatgles are described by two points, the bottom left corner
(<id>x1, <id>y1) and top right corner (<id>x2, <id>y2), where <id> is the name
of the rectangle (i.e, 'a' or 'b').

Constrcaints:
    -10^4 <= <id>x1 <= <id>x2 <= 10^4
    -10^4 <= <id>y1 <= <id>y2 <= 10^4
"""
from typing import Optional


class Rectangle:
    """A rectangle on a cartesian plane."""

    def __init__(self, bottom_left_coordinates: tuple[int, int], top_right_coordinates: tuple[int, int]) -> None:
        self.blc = bottom_left_coordinates
        self.trc = top_right_coordinates

    @property
    def blc(self) -> tuple[int, int]:
        return self.__blc

    @blc.setter
    def blc(self, bottom_left_coordinates: tuple[int, int]) -> None:
        """Initialise bottom left coordinates and update length and width."""
        if all([isinstance(p, int) for p in bottom_left_coordinates]):
            self.__blc = bottom_left_coordinates
            self.init_len_width()
        else:
            raise TypeError(
                "The bottom left coordinates must all be integers.")

    @property
    def trc(self) -> tuple[int, int]:
        return self.__trc

    @trc.setter
    def trc(self, top_right_coordinates: tuple[int, int]) -> None:
        """Initialise top right coordinates and update length and width."""
        if all([isinstance(p, int) for p in top_right_coordinates]):
            self.__trc = top_right_coordinates
            self.init_len_width()
        else:
            raise TypeError(
                "The top right coordinates must all be integers.")

    @property
    def length(self) -> int:
        return self.__length

    @property
    def width(self) -> int:
        return self.__width

    def init_len_width(self) -> None:
        """Set values for width and length.

        width is the vertical-length or y-length.
        length is the horizontal-length or x-length.
        """
        y1: int = self.blc[1] if hasattr(self, "_Rectangle__blc") else 0
        y2: int = self.trc[1] if hasattr(self, "_Rectangle__trc") else 0

        if y1 <= y2:
            self.__width: int = abs(y2 - y1)
        else:
            self.__width = 0

        x1: int = self.blc[0] if hasattr(self, "_Rectangle__blc") else 0
        x2: int = self.trc[0] if hasattr(self, "_Rectangle__trc") else 0

        if x1 <= x2:
            self.__length: int = abs(x2 - x1)
        else:
            self.__length = 0

    @property
    def area(self) -> int:
        return self.__length * self.__width

    def getOverlap(self, other: "Rectangle") -> Optional["Rectangle"]:
        """Return an instance of an overlapping rectangle if any else None."""
        if not self.area or not other.area:
            return None

        # Get the right-most left edge of the two rectangles
        left: int = max(self.blc[0], other.blc[0])
        # Get the left-most right edge
        right: int = min(self.trc[0], other.trc[0])

        # Get the top-most bottom edge
        bottom: int = max(self.blc[1], other.blc[1])
        # Get the bottom-most top edge
        top: int = min(self.trc[1], other.trc[1])

        if left >= right or bottom >= top:
            return None

        return Rectangle((bottom, left), (top, right))


class Solution:
    """LEETCODE."""

    def computeArea(self, ax1: int, ay1: int, ax2: int, ay2: int, bx1: int, by1: int, bx2: int, by2: int) -> int:
        """Calculate the total area covered by two rectangles."""
        rec1: Rectangle = Rectangle((ax1, ay1), (ax2, ay2))
        rec2: Rectangle = Rectangle((bx1, by1), (bx2, by2))
        overlap: Rectangle | None = rec1.getOverlap(rec2)

        o_area: int = overlap.area if overlap else 0
        area: int = rec1.area + rec2.area - o_area
        return area


if __name__ == "__main__":
    t = Solution()

    # 0
    print(
        f"[(0, 0), (0, 0)] + [(0, 0), (0, 0)] = {t.computeArea(*(0, 0), *(0, 0), *(0, 0), *(0, 0))}")

    # 30
    print(
        f"[(0, 0), (5, 3)] + [(5, 3), (10,6)] = {t.computeArea(*(0, 0), *(5, 3), *(5, 3), *(10,6))}")

    # 9
    print(
        f"[(0, 0), (0, 0)] + [(-1, -1), (2, 2)] = {t.computeArea(*(0, 0), *(0, 0), *(-1, -1), *(2, 2))}")

    # 45
    print(
        f"[(-3, 0), (3, 4)] + [(0, -1), (9, 2)] = {t.computeArea(*(-3, 0), *(3, 4), *(0, -1), *(9, 2))}")

    # 42
    print(
        f"[(-5, 0), (0, 3)] + [(-3, -3), (3, 3)] = {t.computeArea(*(-5, 0), *(0, 3), *(-3, -3), *(3, 3))}")

    # 54
    print(
        f"[(-3, -4), (6, 2)] + [(-3, -4), (6, 2)] = {t.computeArea(*(-3, -4), *(6, 2), *(-3, -4), *(6, 2))}")

    # 16
    print(
        f"[(-2, -2), (2, 2)] + [(-2, -2), (2, 2)] = {t.computeArea(*(-2, -2), *(2, 2), *(-2, -2), *(2, 2))}")

    # 16
    print(
        f"[(-2, -2), (2, 2)] + [(-1, -1), (1, 1)] = {t.computeArea(*(-2, -2), *(2, 2), *(-1, -1), *(1, 1))}")
