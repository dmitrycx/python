# implementation of card game - Memory

import simplegui
import random

#consts
card_width = 50
card_height = 100
card_list_size = 16

#global fields
first_card_opened_index = -1
second_card_opened_index = -1

def init():
    """
    Initializes required fields
    """
    global card_list, card_list_exposed
    card_list = []
    card_list_exposed = []
    card_list.extend(range(8))
    card_list.extend(range(8))
    random.shuffle(card_list)
    card_list_exposed = [False for number in range(card_list_size)]
    

# helper function to initialize globals
def new_game():
    global card_list, state, counter
    
    state = 0
    counter = 0
    label.set_text('Turns = ' + str(counter))
    
    init()

     
# define event handlers
def mouseclick(pos):
    global label, counter
    global state # quantity of cards opened
    global first_card_opened_index, second_card_opened_index
    
    card_index = pos[0] / card_width
    
    #action only if click on closed card
    if not card_list_exposed[card_index]:
        if state == 0: # 0 cards exposed
            state = 1
            first_card_opened_index = card_index #remember 1st open card index
            card_list_exposed[card_index] = True
        elif state == 1: # 1 cards exposed
            state = 2
            second_card_opened_index = card_index
            card_list_exposed[card_index] = True
        else: # 2 cards exposed
            state = 1
            
            # close 2 cards if they are not equal
            if not card_list[first_card_opened_index] == card_list[second_card_opened_index]:
                card_list_exposed[first_card_opened_index] = False
                card_list_exposed[second_card_opened_index] = False
            
                # increment counter by 1
                counter += 1
                label.set_text('Turns = ' + str(counter))
            
            first_card_opened_index = card_index
            card_list_exposed[card_index] = True
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    i = 0
    font_size = 85

    # draw green rectangles for all cards that are not exposed
    for index, card in enumerate(card_list):
        if card_list_exposed[index]:
            canvas.draw_text(str(card), [i, font_size] , card_height, 'White')
        else:
            canvas.draw_polygon([[i, 0], [i + card_width, 0], [i + card_width, card_height], [i, card_height]], 4, 'Black', 'Green')
        i += card_width


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns1 = 0")
# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
