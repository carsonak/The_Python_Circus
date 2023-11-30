#!/usr/bin/python3

import random
options = ["Rock", "Paper", "Scissors"]


def get_choice():
    """Prompts the user. Randomises a choice from a list.
    Returns a dictionary with user input and the choice"""

    player_choice = input("Rock! Paper! Scissors! GO!!\n")
    comp_choice = random.choice(options)
    choices = {"Computer": comp_choice, "Player": player_choice}

    return choices


def winner(player, comp):
    """Determines the winner with cool onomatopeia"""

    schiing = "shhvwiipp!!"
    crush = "kllaanngg!!"
    cover = "ffwaaampp!!"
    p_win = " YOU WIN!"
    c_win = " YOU LOSE!"

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
        return "Hey! Only Rocks, Papers and Scissors allowed.\n"


def ref():
    """Checks that input is part of the alphabet and determines winner"""

    play = get_choice()
    print(f"Player [{play['Player']}] | Computer [{play['Computer']}]")
    if play["Player"].isalpha():
        print(winner(play["Player"], play["Computer"]))
    else:
        print("Huh!?")


ref()
