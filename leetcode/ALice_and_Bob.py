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


class Solution:
    """LEETCODE."""

    def numberOfPairs(self, points: list[list[int]]) -> int:
        """Return number of possible Alice and Bob's private spaces."""
        x_sorted: list[list[int]] = sorted(points)
        y_sorted: list[list[int]] = sorted(points, key=lambda l: (l[1], l[0]))
        # A dictionary to map each vector to its indices in both sorted lists
        points_map: dict[str, list[int]] = dict()
        for i in range(len(x_sorted)):
            x_key = str(x_sorted[i])
            if x_key in points_map:
                points_map[x_key][0] = i
            else:
                points_map[x_key] = [i, 0]

            y_key = str(y_sorted[i])
            if y_key in points_map:
                points_map[y_key][1] = i
            else:
                points_map[y_key] = [0, i]

        pairs: int = 0
        array_len: int = len(y_sorted)
        # Iterate through the sorted points and count all valid points.
        # At any possible point for Alice, Bob's vector will have an x value
        # greater than Alice's and a y value less than hers. But only the
        # vectors closest to Alice's in this range will be valid points.
        for alice_pos in x_sorted:
            bob_pos: int = points_map[str(alice_pos)][1]
            if bob_pos + 1 < array_len and y_sorted[bob_pos + 1][1] <= alice_pos[1]:
                bob_pos += 1
            else:
                bob_pos -= 1

            if bob_pos >= 0:
                min_x: int = alice_pos[0]
                max_x: int = y_sorted[bob_pos][0] + 1

            while 0 <= bob_pos < array_len:
                if y_sorted[bob_pos] != alice_pos and min_x <= y_sorted[bob_pos][0] < max_x:
                    pairs += 1
                    max_x = y_sorted[bob_pos][0]

                bob_pos -= 1

        return pairs


if __name__ == "__main__":
    def test_numberOfPairs(list_of_points: list[list[int]]):
        """Test number of pairs."""

        sol: Solution = Solution()
        print(
            f"Pairs: {sol.numberOfPairs(list_of_points)} :Points: {list_of_points}")

    # test_numberOfPairs([[0, 1], [4, 5], [10, 11], [2, 3], [4, 1], [6, 7],
    #                     [7, 7], [6, 3]])
    # test_numberOfPairs([[1, 1], [2, 2], [3, 3]])
    # test_numberOfPairs([[6, 2], [4, 4], [2, 6]])
    test_numberOfPairs([[3, 1], [1, 3], [1, 1]])
