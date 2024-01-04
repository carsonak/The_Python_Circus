#!/usr/bin/python3
def find_pangram(sentence):
    """Check whether a string is Pangram"""

    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for ltr in sentence:
        for check in alphabet:
            if ltr == check:
                alphabet = alphabet.replace(check, "")
        if not alphabet:
            break

    if len(alphabet) > 0:
        print("Not Pangram")
    else:
        print("Is Pangram")


find_pangram("123")
