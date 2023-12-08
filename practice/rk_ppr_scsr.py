#!/usr/bin/python3
"""A game of Rock, Paper, Scissors against the computer"""

import random
options = ["Rock", "Paper", "Scissors"]  # Global variables not recommended


def get_choice():
    """Prompt for input, choose item from list, return a dictionary.

    Return:
    choices -- A dictionary with the selected string and user iput.

    Side effect:
    Reads from the global variable 'options'
    """

    player_choice = input("Rock! Paper! Scissors! GO!!\n")
    comp_choice = random.choice(options)
    choices = {"Computer": comp_choice, "Player": player_choice}

    return choices


def winner(player, comp):
    """Compare two strings, return different strings based on the results.

    Arguments:
    player -- a string with only alphabets
    comp -- a string with only alphabets

    Return:
    A string which typically consists of concatenated values annoucing the
    winner.

    Side effect:
    Reads from the global variable 'options'
    """

    schiing = "shhvwiipp!! "
    crush = "kllaanngg!! "
    cover = "ffwaaampp!! "
    p_win, c_win = "YOU WIN!", "YOU LOSE!"

    if player.lower() == comp.lower():
        return "JINXX!! It's a tie!!"
    elif player.lower() == "rock":
        if comp == options[1]:
            return cover.upper() + c_win.capitalize() + "\n"
        else:
            return crush.upper() + p_win.capitalize() + "\n"
    elif player.lower() == "paper":
        if comp == options[2]:
            return schiing.upper() + c_win.capitalize() + "\n"
        else:
            return cover.upper() + p_win.capitalize() + "\n"
    elif player.lower() == "scissors":
        if comp == options[0]:
            return crush.upper() + c_win.capitalize() + "\n"
        else:
            return schiing.upper() + p_win.capitalize() + "\n"
    else:
        return "Hey! Only Rocks, Papers and Scissors allowed."


def ref():
    """Call get_choice(), check user input then print the return of winner()"""

    play = get_choice()
    print(f"Player [{play['Player']}] | Computer [{play['Computer']}]")
    if play["Player"].isalpha():
        print(winner(play["Player"], play["Computer"]), end="")
    else:
        print("Huh!?")


ref()
