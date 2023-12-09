#!/usr/bin/python3
import random


def random_pangram():
    """Return a random string from a dictionary"""

    some_pangrams = {
        0: "",
        1: "The quick brown fox jumps over a lazy dog.",
        2: "The five boxing wizards jump quickly.",
        3: "Pack my box with five dozen liquor jugs.",
        4: "Betty Botter bought some butter.",
        5: "Puzzled women bequeath jerks very exotic gifts.",
        6: "She sells seashells by the seashore.",
        7: "Five or six big jet planes zoomed quickly by the tower.",
        8: "1, 2, 3, 4, 5, 6, 7, 8, 9, 10.",
        9: "abcdefghijklmnopqrstuvwxyz",
        10: "RACECAR",
        11: "How quickly daft jumping zebras vex!",
        12: "Sphinx of black quartz, judge my vow.",
        13: "!#$%&'()*+,-./:;<=>?@[]^_`{|}~",
        14: "HalloWEEN",
        15: "☻"
    }

    return some_pangrams[random.randint(0, 15)]


def clean_sentence(sentence=""):
    """Strip a string of punctuation characters"""

    s_cpy = sentence.lower()
    punctuations = ""

    for ascii in range(10, 127):
        if ascii == 10:
            punctuations += chr(ascii)
        elif 32 <= ascii <= 47 or 58 <= ascii <= 64:
            punctuations += chr(ascii)
        elif 91 <= ascii <= 96 or 123 <= ascii <= 126:
            punctuations += chr(ascii)

    for punct in punctuations:
        s_cpy = s_cpy.replace(punct, "")

    return s_cpy


def is_pangram(sentence=""):
    """Determine whether a string is a Pangram."""

    alphabet = sorted("abcdefghijklmnopqrstuvwxyz")
    copy_s = clean_sentence(sentence) if sentence else ""
    if sentence:
        if sorted(copy_s) == alphabet:
            print(f"{sentence:s}\nIs a perfect Pangram")
        else:
            not_pangram(sentence)
    else:
        print(f"{sentence:s}\nIs empty.")


def not_pangram(sentence=""):
    """Determine whether a string is a Pangram.

    Strips a string of punction marks and checks for invaid characters.
    Then determines if the string contains all the letters of the alphabet
    and gives statistics.
    """

    alphabet = "abcdefghijklmnopqrstuvwxyz"
    copy_s = clean_sentence(sentence)
    inval = set()

    for ltr in copy_s:
        if not ltr.isalpha():
            inval.add(ltr)

    if copy_s and inval:
        print(f"{sentence:s}\nHas invalid characters: {sorted(inval)}")
    elif copy_s and not inval:
        for itm in copy_s:
            alphabet = alphabet.replace(itm, "", 1)

        if alphabet:
            print(f"{sentence:s}\nDoesn't contain these letters: {alphabet}")
        else:
            alphabet = "abcdefghijklmnopqrstuvwxyz"
            for ltr in alphabet:
                copy_s = copy_s.replace(ltr, "", 1)

            print(f"{sentence:s}\nIs a Pangram with these repeated letters:")
            print_dictionary_sorted(get_dupes(alphabet, copy_s))
    else:
        print(f"{sentence:s}\nDoesn't contain any letters.")


def get_dupes(str1="", str2=""):
    """Count number of occurences of items in one from one set in another.

    str1: Preferably a string with no repeated items.
    str2: Preferably another string with repeated items to check for

    Return: A dictionary with the values indicating number of repetitions
        of the keys.
    """

    excess = {}
    for ltr in str1:
        cnt = 0
        for itm in str2:
            if ltr == itm:
                cnt += 1
        if cnt:
            excess[ltr] = cnt

    return excess


def print_dictionary_sorted(a_dictionary):
    """Print a dictionary sorted by its keys"""

    for d_key in sorted(a_dictionary.keys()):
        print(f"{d_key:s}: {a_dictionary[d_key]}")


is_pangram(random_pangram())
