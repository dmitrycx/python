import random

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

#define dictionary not to use countless if-else statements
game_units = {'rock':0, 'Spock':1, 'paper':2, 'lizard':3, 'scissors':4}

def name_to_number(name):
    return game_units[name]


def number_to_name(number):
    # Dictionary is not usually used to get key by value but Enum implemented 
    # in python3 only so we need to use key-value pair
    for name, num in game_units.items():
        if num == number:
            return name

def rpsls(player_choice): 
    print
    
    print "Player chooses: " + player_choice
    
    player_number = name_to_number(player_choice)
    
    comp_number = random.randrange(len(game_units))
    comp_choice = number_to_name(comp_number)
    
    print "Computer chooses: " + comp_choice
    
    # compute difference of comp_number and player_number modulo five
    difference = (comp_number - player_number) % 5
    
    # use rpsls-wheel logic
    if difference == 0:
        print "Player and computer tie!"
    elif (difference == 1 or difference == 2):
        print "Computer wins!"
    else:
        print "Player wins!"
    
# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")



