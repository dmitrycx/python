# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    


#Consts
BLACKJACK_VALUE = 21
DEALER_STOP_VALUE = 17
ACE_OFFSET = 10
ACE_RANK = 'A'

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
help_message = ""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
    
    def draw_back(self, canvas, pos):
        card_loc = (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1])
        canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

# define hand class
class Hand:
    def __init__(self):
        self.card_list = []

    def __str__(self):
        cards = ""
        for i in range(len(self.card_list)):
            cards += str(self.card_list[i]) + ' '
        return 'Hand contains ' + cards

    def add_card(self, card):
        self.card_list.append(card)	# add a card object to a hand

    def get_value(self):
        result = 0
        # we can only count 1 ace as 11 points so we only need to know
        # whether there is an Ace in a hand or not
        contains_ace = False 
        for card in self.card_list:
            result += VALUES[card.rank]
            if card.rank == ACE_RANK:
                contains_ace = True

        # if there is an Ace in a hand count it as 11 points if you will not 
        # bust in the result of calculation
        if contains_ace and (result + ACE_OFFSET) <= BLACKJACK_VALUE:
            result += ACE_OFFSET

        return result
   
    # draw cards side to side
    def draw(self, canvas, pos):
          for card in self.card_list:
                card.draw(canvas, pos)
                pos[0] += CARD_SIZE[0]

                
# define deck class 
class Deck:
    def __init__(self):
        self.card_list = []
        for suit in SUITS:
            for rank in RANKS:
                self.card_list.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.card_list)

    def deal_card(self):
        return self.card_list.pop()
    
    def __str__(self):
        cards = ""
        for i in range(len(self.card_list)):
            cards += str(self.card_list[i]) + ' '
        return 'Deck contains ' + cards
    


#define event handlers for buttons
def deal():
    global outcome, in_play, score, help_message
    global player_hand, dealer_hand, deck
    outcome = ''
    
    if in_play:
        outcome = 'You lose.'
        score -= 1
    
    deck = Deck()
    deck.shuffle()
    
    # create hands
    player_hand = Hand()
    dealer_hand = Hand()
    
    #populate player hand
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    #populate dealer hand
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    in_play = True
    help_message = 'Hit or stand?'
    

def hit():
    global player_hand, outcome, in_play, score, help_message
    
    if in_play:
        player_hand.add_card(deck.deal_card())
        
        if player_hand.get_value() > BLACKJACK_VALUE:
            outcome = "You went bust and lose."
            score -= 1
            in_play = False
            help_message = 'New deal?'

def stand():
    global dealer_hand, outcome, score, in_play, help_message

    if in_play:
        while dealer_hand.get_value() < DEALER_STOP_VALUE:
            dealer_hand.add_card(deck.deal_card())
        
        if dealer_hand.get_value() > BLACKJACK_VALUE:
            outcome = "Dealer has busted."
            score += 1
            in_play = False
        elif dealer_hand.get_value() >= player_hand.get_value():
            outcome = "You lose."
            score -= 1
            in_play = False
        else:
            outcome = "You won."
            score += 1
            in_play = False
            
        help_message = 'New deal?'            
            
            
# draw handler    
def draw(canvas):
    canvas.draw_text('BlackJack', (200,70), 40, 'Red')
    canvas.draw_text('Score: ' + str(score), (450,70), 22, 'Black')
    
    canvas.draw_text('Dealer:', (100,240), 22, 'Black')
    dealer_hand.draw(canvas, [100, 250])
    # hide first dealer card
    if in_play:
        card = dealer_hand.card_list[0]
        card.draw_back(canvas, [100, 250])
    
    canvas.draw_text('Player:', (100,390), 22, 'Black')
    player_hand.draw(canvas, [100, 400])
        
    canvas.draw_text(help_message, (300,390), 22, 'Black')
    canvas.draw_text(outcome, (300,240), 22, 'Black')
        

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
