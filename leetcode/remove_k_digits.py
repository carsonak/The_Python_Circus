#!/usr/bin/python3
"""LEETCODE: 402. Remove K Digits.

Return the smallest possible number after removing 'k' digits
from an integer 'num'.

Example 1:
    Input: num = "1432219", k = 3
    Output: "1219"

Example 2:
    Input: num = "10200", k = 1
    Output: "200"

Example 3:
    Input: num = "10", k = 2
    Output: "0"

Constraints:
    1 <= k <= num.length <= 105
    'num' consists of only digits.
    'num' does not have any leading zeros except for the zero itself.
"""


class Solution:
    """LEETCODE."""

    def removeKdigits(self, num: str, k: int) -> str:
        """Return smallest number after removing 'k' digits from 'num'."""
        digits = len(num)
        if k >= digits:
            return "0"

        new_num: list[str] = []
        for idx, val in enumerate(num):
            if k > 0:
                if idx + 1 < digits and num[idx + 1] >= val:
                    new_num.append(val)
                elif idx + 1 >= digits:
                    new_num.append(val)
                else:
                    k -= 1
            else:
                new_num += list(num[idx:])
                break

        num_str = "".join(new_num).lstrip("0")
        if num_str and k:
            new_num.clear()
            for idx in range(len(num_str) - 1, -1, -1):
                if k > 0:
                    if idx - 1 >= 0 and num_str[idx] < num_str[idx - 1]:
                        new_num.insert(0, num_str[idx])
                    else:
                        k -= 1
                else:
                    new_num = list(num_str[:idx + 1]) + new_num
                    break

            num_str = "".join(new_num).lstrip("0")

        return num_str if num_str else "0"


if __name__ == "__main__":
    sol = Solution()
    print(sol.removeKdigits("1432219", 3))  # 1219
    print(sol.removeKdigits("112", 1))  # 11
    print(sol.removeKdigits("5337", 2))  # 33
    print(sol.removeKdigits("12345", 3))  # 12
    print(sol.removeKdigits("54321", 3))  # 21
