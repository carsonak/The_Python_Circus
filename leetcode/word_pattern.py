#!/usr/bin/python3
"""LEETCODE: Word Pattern.

Given a 'pattern' and a string 's', find if 's' follows the same 'pattern'.
Here follow means a full match, such that there is a bijection between a
letter in 'pattern' and a non-empty word in 's'.

Example 1:
    Input: pattern = "abba", s = "dog cat cat dog"
    Output: true

Example 2:
    Input: pattern = "aaaa", s = "dog cat cat dog"
    Output: false

Constraints:
    1 <= pattern.length <= 300
    'pattern' contains only lower-case English letters.
    1 <= s.length <= 3000
    's' contains only lowercase English letters and spaces ' '.
    's' does not contain any leading or trailing spaces.
    All the words in 's' are separated by a single space.
"""


class Solution:
    """LEETCODE."""

    def wordPattern(self, pattern: str, s: str) -> bool:
        """Check if string 's' matches the pattern 'pattern'."""
        if type(pattern) is not str or type(s) is not str:
            raise TypeError("'pattern' and 's' must be strings.")

        words = s.split()
        if len(pattern) != len(words):
            return False

        word_map: dict[str, str] = {}  # map a word to a letter
        pattern_map: dict[str, str] = {}  # map a letter to a word
        for lett, wrd in zip(pattern, words):
            if wrd not in word_map:
                word_map[wrd] = lett
            elif word_map[wrd] != lett:
                return False

            if lett not in pattern_map:
                pattern_map[lett] = wrd
            elif pattern_map[lett] != wrd:
                return False

        return True


if __name__ == "__main__":
    def test_wordPattern(p: str, s: str) -> None:
        """Test wordPattern."""
        sol = Solution()
        if sol.wordPattern(p, s):
            print(f"[{p:s}] - '{s:s}'\nMATCH", end="\n\n")
        else:
            print(f"[{p:s}] - '{s:s}'\nNOT MATCH", end="\n\n")

    test_wordPattern("", "")  # Match
    test_wordPattern("vvvv", "police police police police")  # Match
    test_wordPattern("abba", "dog cat cat dog")  # Match
    test_wordPattern("aaaa", "dog cat cat dog")  # Not Match
    test_wordPattern("abba", "dog cat cat fish")  # Not Match
    test_wordPattern(
        "abcdef", "betty botter bought bitter butter")  # Not Match
