import random
from tkinter import *
from tkinter import messagebox

# Define suits and values
suits = ["S", "D", "C", "H"]
values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "K", "Q"]

# Create a deck of cards
deck = []
for suit in suits:
    for val in values:
        deck.append(val + suit)

deck = deck * 8  # Multiply deck to have more cards (for multiple decks)
random.shuffle(deck)  # Shuffle the deck

# Define card value function
def card_value(card):
    # Extract value part of card, excluding the suit (last part of the card string)
    card_value = card[:-1]  # Get the value part, removing the suit letter
    
    # Convert face cards and 10 to value 0, Ace to value 1
    if card_value in ['J', 'Q', 'K', '10']:
        return 0
    elif card_value == 'A':
        return 1
    else:
        # Convert numeric cards (2-9) to integer
        return int(card_value)

# Deal a hand of two cards
def deal_hand():
    hand = [deck.pop(), deck.pop()]
    return hand

# Calculate hand total
def hand_total(hand):
    total = sum(card_value(card) for card in hand)
    return total % 10  # Baccarat is played mod 10

# Draw additional card if necessary
def draw_additional_card(hand):
    if hand_total(hand) <= 5:
        hand.append(deck.pop())
    return hand

# Start the game
def start_game():
    # Initial hands
    player_hand = deal_hand()
    banker_hand = deal_hand()

    player_hand = draw_additional_card(player_hand)
    banker_hand = draw_additional_card(banker_hand)

    player_total = hand_total(player_hand)
    banker_total = hand_total(banker_hand)

    # Update labels
    player_hand_label.config(text=f"Player Hand: {player_hand} (Total: {player_total})")
    banker_hand_label.config(text=f"Banker Hand: {banker_hand} (Total: {banker_total})")

    # Determine winner
    if player_total > banker_total:
        winner = "Player wins!"
    elif banker_total > player_total:
        winner = "Banker wins!"
    else:
        winner = "It's a tie!"

    # Show game result
    messagebox.showinfo("Game Result", winner)


# Initialize Tkinter root window
root = Tk()
root.title("Baccarat")
root.geometry("500x400")

# Title label
title_label = Label(root, text="Baccarat Game", font=("Helvetica", 16))
title_label.pack(pady=10)

# Player and banker hand labels
player_hand_label = Label(root, text="Player Hand: --", font=("Helvetica", 12))
player_hand_label.pack(pady=5)

banker_hand_label = Label(root, text="Banker Hand: --", font=("Helvetica", 12))
banker_hand_label.pack(pady=5)

# Start button
start_button = Button(root, text="Start Game", font=("Helvetica", 14), command=start_game)
start_button.pack(pady=20)

# Run the main loop of the Tkinter app
root.mainloop()
