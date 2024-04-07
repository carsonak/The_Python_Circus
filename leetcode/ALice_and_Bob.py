#!/usr/bin/python3
"""LEETCODE: 3025. Find the Number of Ways to Place People I.

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
import unittest
import random


class Solution:
    """LEETCODE."""

    def numberOfPairs(self, points: list[list[int]]) -> int:
        """Return number of possible Alice and Bob's private spaces.

        Args:
            points (list[list[int]]): a list of vectors.

        Return:
            Number of possible pairs for Alice and Bob.
        """
        x_sorted: list[list[int]] = sorted(points)
        y_sorted: list[list[int]] = sorted(points, key=lambda v: (v[1], v[0]))
        # A dict to track a vector's indices in both lists
        points_map: dict[tuple, list[int]] = dict()
        for i in range(len(x_sorted)):
            x_key = tuple(x_sorted[i])
            if x_key in points_map:
                points_map[x_key][0] = i
            else:
                points_map[x_key] = [i, 0]

            y_key = tuple(y_sorted[i])
            if y_key in points_map:
                points_map[y_key][1] = i
            else:
                points_map[y_key] = [0, i]

        pairs: int = 0
        arr_len: int = len(y_sorted)
        # Iterate through the sorted points and count all valid points.
        # At any possible point for Alice, Bob's vector will have an x value
        # greater than Alice's and a y value less than hers.
        # Any vector in this quadrant that forms a rectangle with Alice's
        # vector, whose x-length and y-length aren't both greater or equal
        # to any other possible rectangle, will be valid vectors for Bob.
        for x_idx, alice_pos in enumerate(x_sorted):
            y_idx: int = points_map[tuple(alice_pos)][1]
            max_x: float = float("infinity")
            min_x: int = alice_pos[0]
            min_y: int | None = None
            # If there is a colinear point on x-axis, just right of Alice,
            # the maximum x value of Bob's vector should be updated.
            if y_idx + 1 < arr_len and y_sorted[y_idx + 1][1] == alice_pos[1]:
                pairs += 1
                max_x = y_sorted[y_idx + 1][0]

            # If there is a colinear point on y-axis, just below Alice,
            # the minimum y value of Bob's vector should be updated.
            if x_idx - 1 >= 0 and x_sorted[x_idx - 1][0] == alice_pos[0]:
                pairs += 1
                min_y = x_sorted[x_idx - 1][1]

            y_idx -= 1
            while y_idx >= 0:
                bob_pos: list[int] = y_sorted[y_idx]
                next_bob: list[int] = y_sorted[y_idx - 1]
                # Check if Bob's position is the closest vector to Aice's pos.
                if next_bob[1] == bob_pos[1] and min_x < next_bob[0] < max_x:
                    pass
                # Check if Bob's position is in the valid quadrant
                elif min_x < bob_pos[0] < max_x \
                        and (True if min_y is None else min_y < bob_pos[1]):
                    pairs += 1
                    max_x = bob_pos[0]

                y_idx -= 1

        return pairs


if __name__ == "__main__":
    class NOPtest(unittest.TestCase):
        """Tests for numberOfPairs."""

        def setUp(self) -> None:
            """Create instance of Solution."""
            self.sol: Solution = Solution()

        def test_isosceles(self) -> None:
            """Test vectors of an Isosceles triangle."""
            self.assertEqual(self.sol.numberOfPairs(
                [[1, 4], [1, 1], [4, 1]]), 2)
            self.assertEqual(self.sol.numberOfPairs(
                [[1, 1], [4, 1], [4, 4]]), 2)
            self.assertEqual(self.sol.numberOfPairs(
                [[4, 1], [4, 4], [1, 4]]), 2)
            self.assertEqual(self.sol.numberOfPairs(
                [[4, 4], [1, 4], [1, 1]]), 2)

        def test_scalene(self) -> None:
            """Test vectors of an Scalene triangle."""
            self.assertEqual(self.sol.numberOfPairs(
                [[0, 4], [0, 0], [6, 0]]), 2)
            self.assertEqual(self.sol.numberOfPairs(
                [[0, 0], [6, 0], [6, 4]]), 2)
            self.assertEqual(self.sol.numberOfPairs(
                [[6, 0], [6, 4], [0, 4]]), 2)
            self.assertEqual(self.sol.numberOfPairs(
                [[6, 4], [0, 4], [0, 0]]), 2)

        def test_cross(self) -> None:
            """Test cross shape vectors."""
            pts = [[1, -1], [1, 3], [1, 1], [3, 1], [5, 1]]
            self.assertEqual(self.sol.numberOfPairs(pts), 4)
            pts = [[0, 2], [4, 2], [2, 2], [2, 4], [2, 6]]
            self.assertEqual(self.sol.numberOfPairs(pts), 4)

        def test_X(self) -> None:
            """Test X shape vectors."""
            pts = [[1, 6], [2, 1], [2, 5], [3, 2], [3, 4], [4, 3], [5, 2],
                   [5, 4], [6, 1], [6, 5], [7, 6]]
            self.assertEqual(self.sol.numberOfPairs(pts), 14)

        def test_mixXcross(self) -> None:
            """Test combined X shape and cross shape vectors."""
            pts = [[-2, 8], [-2, 6], [-2, 5], [-2, 3], [-2, 2], [-2, 1],
                   [-2, -1], [-2, -2], [-2, -4], [-2, -6], [-2, -7],
                   [-8, 2], [-6, 2], [-5, 2], [-3, 2], [-1, 2], [1, 2],
                   [2, 2], [4, 2], [6, 2], [8, 2], [-4, 4], [-4, 0], [0, 0],
                   [0, 4], [-5, 5], [1, 5], [-5, -1], [1, -1], [1, 5]]
            self.assertEqual(self.sol.numberOfPairs(pts), 43)

        def test_mix(self) -> None:
            """Test mix vectors."""
            pts = [[0, 1], [4, 5], [10, 11], [0, 0], [2, 3], [6, 2], [8, 6],
                   [4, 1], [6, 7], [7, 7], [6, 3], [8, 3], [9, 3]]
            self.assertEqual(self.sol.numberOfPairs(pts), 13)

        def test_yEqualx(self) -> None:
            """Test vectors on a y=x slope."""
            self.assertEqual(self.sol.numberOfPairs(
                [[-4, -4], [-3, -3],  [-2, -2], [-1, -1], [0, 0], [1, 1],
                 [2, 2], [3, 3], [4, 4]]), 0)

        def test_negyEqualx(self) -> None:
            """Test vectors on a y=-x slope."""
            self.assertEqual(self.sol.numberOfPairs(
                [[-4, 4], [-3, 3],  [-2, 2], [-1, 1], [0, 0], [1, -1],
                 [2, -2], [3, -3], [4, -4]]), 8)

    def print_numberOfPairs(list_of_points: list[list[int]]):
        """Print number of pairs."""
        sol: Solution = Solution()
        print(
            f"Pairs: {sol.numberOfPairs(list_of_points)} :Points: {list_of_points}")

    unittest.main()
    # for i in range(20):
    #     rans = set((random.randint(-100, 100), random.randint(-100, 100))
    #                for v in range(random.randint(5, 12)))
    #     pts = [list(v) for v in rans]
    #     print_numberOfPairs(pts)
