#!/usr/bin/python3
"""LEETCODE: 34. Find First and Last Position of Element in Sorted Array.

Given an array of integers nums sorted in non-decreasing order,
find the starting and ending position of a given target value.
If target is not found in the array, return [-1, -1].
You must write an algorithm with O(log n) runtime complexity.

Example 1:
Input: nums = [5,7,7,8,8,10], target = 8
Output: [3,4]

Example 2:
Input: nums = [5,7,7,8,8,10], target = 6
Output: [-1,-1]

Example 3:
Input: nums = [], target = 0
Output: [-1,-1]

Constraints:
    0 <= nums.length <= 105
    -109 <= nums[i] <= 109
    nums is a non-decreasing array.
    -109 <= target <= 109
"""
import unittest


class Solution:
    """LEETCODE."""

    def searchRange(self, nums: list[int], target: int) -> list[int]:
        """Return range of a number in a sorted list.

        Args:
            nums (list[int]): sorted list of integers.
            target (int): integer to get range of.

        Return:
            (list[int]): a list of of 2 ints indicating the range of target,
                [-1, -1] if not found.
        """
        range: list[int] = [-1, -1]
        end: int = len(nums) - 1
        start: int = 0
        if nums and nums[start] <= target <= nums[end]:
            while nums[end] > target:
                mid: int = int((end - start) / 2)
                if mid == 0:
                    break

                if nums[start + mid] >= target:
                    end = start + mid

                if nums[start + mid] < target:
                    start += mid

            if nums[end] == target:
                n_len: int = len(nums)
                while (end + 1 < n_len and nums[end + 1] <= target) or nums[start] < target:
                    if end + 1 < n_len and nums[end + 1] <= target:
                        end += 1

                    if nums[start] < target:
                        start += 1

                range = [start, end]
            elif nums[start] == target:
                while end > 0 and nums[end] > target:
                    end -= 1

                range = [start, end]

        return range


if __name__ == "__main__":
    class TestsearchRange(unittest.TestCase):
        """Tests for searchRange."""

        def setUp(self) -> None:
            """Create instance of Solution."""
            self.sol: Solution = Solution()

        def test_emptyList(self) -> None:
            """Test empty list."""
            self.assertEqual(self.sol.searchRange([], 1), [-1, -1])

        def test_oneItem_extremes_oddLength(self) -> None:
            """Test range of one item in sorted list on the extremes."""
            self.assertEqual(self.sol.searchRange([1, 2, 3, 4, 5], 1), [0, 0])
            self.assertEqual(self.sol.searchRange([1, 2, 3, 4, 5], 5), [4, 4])

        def test_oneItem_extremes_evenLength(self) -> None:
            """Test range of one item in sorted list on the extremes."""
            self.assertEqual(self.sol.searchRange(
                [1, 2, 3, 4, 5, 6], 1), [0, 0])
            self.assertEqual(self.sol.searchRange(
                [1, 2, 3, 4, 5, 6], 6), [5, 5])

        def test_oneItem_lengthOne(self):
            """Test range of one item in a sorted list of length one."""
            self.assertEqual(self.sol.searchRange([-100], -100), [0, 0])
            self.assertEqual(self.sol.searchRange([100], 100), [0, 0])
            self.assertEqual(self.sol.searchRange([0], 0), [0, 0])

        def test_oneItem_lengthTwo(self):
            """Test range of one item in a sorted list of length two."""
            self.assertEqual(self.sol.searchRange([-100, 100], -100), [0, 0])
            self.assertEqual(self.sol.searchRange([-100, -10], -10), [1, 1])

        def test_oneItem_lengthThree(self):
            """Test range of one item in a sorted list of length one."""
            self.assertEqual(self.sol.searchRange([-100, 0, 4], -100), [0, 0])
            self.assertEqual(self.sol.searchRange([10, 12, 44], 44), [2, 2])

        def test_twoItems_lengthTwo(self):
            """Test range of two items in a sorted list of length two."""
            self.assertEqual(self.sol.searchRange([0, 0], 0), [0, 1])

        def test_twoItems_lengthThree(self):
            """Test range of two items in a sorted list of length three."""
            self.assertEqual(self.sol.searchRange(
                [-10, -10, -7], -10), [0, 1])
            self.assertEqual(self.sol.searchRange([0, 10, 10], 10), [1, 2])

        def test_threeItems_lengthThree(self):
            """Test range of three items in a sorted list of length three."""
            self.assertEqual(self.sol.searchRange(
                [-10, -10, -10], -10), [0, 2])

        def test_oneItem_oddLength(self) -> None:
            """Test range of one item in sorted list of an odd length."""
            test_case: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

            for i in range(1, len(test_case) - 1):
                with self.subTest(i=i):
                    self.assertEqual(self.sol.searchRange(
                        test_case, i + 1), [i, i])

        def test_oneItem_oddLength_signed(self) -> None:
            """Test range of one item in sorted list of an odd length."""
            test_case: list[int] = [-4, -3, -2, -1, 0, 1, 2, 3, 4]

            for i in range(1, len(test_case) - 1):
                with self.subTest(i=i):
                    self.assertEqual(self.sol.searchRange(
                        test_case, test_case[i]), [i, i])

        def test_oneItem_evenLength(self) -> None:
            """Test range of one item in sorted list of an even length."""
            test_case: list[int] = [1, 2, 3, 4, 5, 6, 7, 8]

            for i in range(1, len(test_case) - 1):
                with self.subTest(i=i):
                    self.assertEqual(self.sol.searchRange(
                        test_case, i + 1), [i, i])

        def test_oneItem_evenLength_signed(self) -> None:
            """Test range of one item in sorted list of an even length."""
            test_case: list[int] = [-3, -2, -1, 0, 1, 2, 3, 4]

            for i in range(1, len(test_case) - 1):
                with self.subTest(i=i):
                    self.assertEqual(self.sol.searchRange(
                        test_case, test_case[i]), [i, i])

            test_case = [-4, -3, -2, -1, 0, 1, 2, 3]

            for i in range(1, len(test_case) - 1):
                with self.subTest(i=i):
                    self.assertEqual(self.sol.searchRange(
                        test_case, test_case[i]), [i, i])

        def test_rangeOfOddItems_oddLength(self) -> None:
            """Test odd range of items in sorted lists of an odd length."""
            template: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

            for len_mul in range(1, 11, 2):
                test_case: list[int] = sorted(template * len_mul)

                with self.subTest(len_mul=len_mul):
                    for i in range(1, len(template) - 1):
                        with self.subTest(i=i):
                            self.assertEqual(self.sol.searchRange(
                                test_case, i + 1), [i * len_mul, ((i + 1) * len_mul) - 1])

        def test_rangeOfOddItems_EvenLength(self) -> None:
            """Test odd range of items in sorted lists of an odd length."""
            template: list[int] = [1, 2, 3, 4, 5, 6, 7, 8]

            for len_mul in range(1, 11, 2):
                test_case: list[int] = sorted(template * len_mul)

                with self.subTest(len_mul=len_mul):
                    for i in range(1, len(template) - 1):
                        with self.subTest(i=i):
                            self.assertEqual(self.sol.searchRange(
                                test_case, i + 1), [i * len_mul, ((i + 1) * len_mul) - 1])

        def test_rangeOfEvenItems_oddLength(self) -> None:
            """Test even range of items in sorted lists of an odd length."""
            template: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

            for len_mul in range(2, 12, 2):
                test_case: list[int] = sorted(template * len_mul)

                with self.subTest(len_mul=len_mul):
                    for i in range(1, len(template) - 1):
                        with self.subTest(i=i):
                            self.assertEqual(self.sol.searchRange(
                                test_case, i + 1), [i * len_mul, ((i + 1) * len_mul) - 1])

        def test_rangeOfEvenItems_EvenLength(self) -> None:
            """Test even range of items in sorted lists of an odd length."""
            template: list[int] = [1, 2, 3, 4, 5, 6, 7, 8]

            for len_mul in range(2, 12, 2):
                test_case: list[int] = sorted(template * len_mul)

                with self.subTest(len_mul=len_mul):
                    for i in range(1, len(template) - 1):
                        with self.subTest(i=i):
                            self.assertEqual(self.sol.searchRange(
                                test_case, i + 1), [i * len_mul, ((i + 1) * len_mul) - 1])

        def test_OOBitem_lesser(self) -> None:
            """Test range of item not in the list."""
            self.assertEqual(self.sol.searchRange([0, 1, 2, 3], -1), [-1, -1])

        def test_OOBitem_greater(self) -> None:
            """Test range of item not in the list."""
            self.assertEqual(self.sol.searchRange([0, 1, 2, 3], 5), [-1, -1])

    unittest.main()
