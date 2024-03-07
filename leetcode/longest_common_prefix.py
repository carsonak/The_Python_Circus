#!/usr/bin/env python3

class Solution:
    """LEETCODE"""

    def longestCommonPrefix(self, strs: list[str]) -> str:
        """Return the longest common prefix of a list of strings"""

        prefix = str(strs[0])
        brk = len(prefix)
        for g in range(1, len(strs)):
            if len(strs[g]) < brk:
                brk = len(strs[g])

            for h in range(brk - 1, -1, -1):
                if strs[g][h] != prefix[h]:
                    brk = h
        else:
            prefix = prefix[:brk]

        return prefix


if __name__ == "__main__":
    sl = Solution()
    print(sl.longestCommonPrefix(["flower", "flow", "flight"]))
