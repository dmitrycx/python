import simplegui
import random
import math

num_range = 100
secret_number = 0
remaining_guesses = 0

# helper function to start and restart the game
def new_game():
    """ Restarts the game"""
    global secret_number, num_range, remaining_guesses
    
    print
    print "New game. Range is from 0 to " + str(num_range)
    
    secret_number = random.randrange(num_range)
    compute_remaining_guesses()
    
    print "Number of remainig guesses is " + str(remaining_guesses)
    
def compute_remaining_guesses():
    """ can always be found in at most n guesses where n is the 
    smallest integer such that 2 ** n >= high - low + 1 """
    global remaining_guesses
    remaining_guesses = int(math.ceil(math.log(num_range + 1, 2)))
    
    
# define event handlers for control panel
def range100():
    set_range(100)

    
def range1000():
    set_range(1000)

    
def set_range(range):
    global num_range
    num_range = range
    new_game()
    
    
def input_guess(guess):
    global remaining_guesses
    
    try:
        number_guess = int(guess)
    except ValueError:
        print
        print guess + " is not a valid number. Try again"
        return

    remaining_guesses -= 1
    
    print
    print "Guess was " + guess
    print "Number of remainig guesses is " + str(remaining_guesses)
    
    if remaining_guesses == 0:
        print "Out of guesses"
        new_game()
    else:
        if number_guess < secret_number:
            print "Higher"
        elif number_guess > secret_number:
            print "Lower"
        else:
            print "Correct"
            new_game()
    
            
# create frame
frame = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements and start frame
frame.add_button("Range is [0, 100)", range100, 200)
frame.add_button("Range is [0, 1000)", range1000, 200)
frame.add_input("Enter a guess", input_guess, 200)

frame.start()

# call new_game 
new_game()

