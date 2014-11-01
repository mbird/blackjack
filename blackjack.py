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

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

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
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []

    def __str__(self):
        # return a string representation of a hand
        self.hand_rep = "Hand contains "
        for i in range(len(self.hand)):
            self.hand_rep += str(self.hand[i]) + " "
        return self.hand_rep

    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        self.value = 0
        for card in self.hand:
            self.value += VALUES[str(card)[1]]
            if VALUES[str(card)[1]] == 1 and self.value + 10 <= 21:
                self.value += 10
                
        return self.value
   
    def draw(self, canvas, pos):
        pass	# draw a hand on the canvas, use the draw method for cards
 
    
 
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        # remember to remove the dealt card from the deck
        return self.deck.pop(-1)
    
    def __str__(self):
        # return a string representing the deck
        self.deck_rep = "Deck contains "
        for i in range(len(self.deck)):
            self.deck_rep += str(self.deck[i]) + " "
        return self.deck_rep



#define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, dealer_hand, new_deck

    # create and shuffle the deck
    new_deck = Deck()
    new_deck.shuffle()
    
    # deal two cards to player
    player_hand = Hand()
    player_hand.add_card(new_deck.deal_card())
    player_hand.add_card(new_deck.deal_card())
    print "Player: ", player_hand
    
    
    # deal two cards to dealer
    dealer_hand = Hand()
    dealer_hand.add_card(new_deck.deal_card())
    dealer_hand.add_card(new_deck.deal_card())
    print "Dealer: ", dealer_hand
    
    in_play = True

def hit():
    global outcome, in_play, player_hand, dealer_hand, new_deck
    # if the hand is in play, hit the player
    if player_hand.get_value() <= 21:
         player_hand.add_card(new_deck.deal_card())
         print "Player: ", player_hand
         if player_hand.get_value() > 21:
                print "You have busted!"
                in_play = False
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    if in_play == False:
        print "Remember: You have busted!"
    else:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(new_deck.deal_card())
            print "Dealer: ", dealer_hand
        if dealer_hand.get_value() > 21:
            print "The dealer has busted!"
        else:
            if player_hand.get_value() > dealer_hand.get_value():
                print "Player wins!"
            else:
                print "Dealer wins!"
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    card = Card("S", "A")
    card.draw(canvas, [300, 300])


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


# remember to review the gradic rubric