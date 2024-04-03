#!/usr/bin/python3
"""LEETCODE: Isomorphic strings.

Given two strings 's' and 't', determine if they are isomorphic.
Two strings 's' and 't' are isomorphic if the characters in 's'
can be replaced to get 't'.

Every occurence of a character in the 's' will be replaced by the character it
first maps to in 't'. Therefore a character shall not map to more than one
other character and the order of appearance in 's' shall be the same in both
strings.

Example 1:
    Input: s = "paper", t = "title"
    Output: true

Constraints:
    1 <= s.length <= 5 * 104
    t.length == s.length
    s and t consist of any valid ascii character.
"""


class Solution:
    """LEETCODE."""

    def isIsomorphic(self, s1: str, s2: str) -> bool:
        """Check if two strings are isomorphic."""
        if type(s1) is not str or type(s2) is not str:
            raise TypeError("s1 and s2 must be strings.")

        if len(s1) != len(s2):
            return False

        s1_letter_map: dict[str, str] = {}
        s2_letter_map: dict[str, str] = {}
        for l1, l2 in zip(s1, s2):
            if l1 not in s1_letter_map:
                s1_letter_map[l1] = l2
            elif s1_letter_map[l1] != l2:
                return False

            if l2 not in s2_letter_map:
                s2_letter_map[l2] = l1
            elif s2_letter_map[l2] != l1:
                return False

        return True


if __name__ == "__main__":
    def test_isometric(s: str, t: str) -> None:
        """Test isIsomorphic."""
        sol = Solution()
        if sol.isIsomorphic(s, t):
            print(f"True:  '{s:s}' - '{t:s}'")
        else:
            print(f"False: '{s:s}' - '{t:s}'")

    test_isometric("egg", "add")  # True
    test_isometric("woah", "woah")  # True
    test_isometric("title", "paper")  # True
    test_isometric("spoon", "gloom")  # True
    test_isometric("apple", "bbnbm")  # False
    test_isometric("badc", "baba")  # False
    test_isometric("foo", "bar")  # False
