import random
from tkinter import *
from tkinter import messagebox


suits = ["S", "D", "C", "H"]
values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "K", "Q"]
deck = []
for suit in suits:
    for val in values:
        deck.append(suit + val)

deck=deck*8
random.shuffle(deck)


def card_value(card):
    if card in ['J', 'Q', 'K', '10']:
        return 0
    elif card == 'A':
        return 1
    else:
        return int(card)


def deal_hand():
    hand = [deck.pop(), deck.pop()]
    return hand


def hand_total(hand):
    total = sum(card_value(card) for card in hand)
    return total % 10  

# Draw additional card if necessary
def draw_additional_card(hand):
    if hand_total(hand) <= 5:
        hand.append(deck.pop())  
    return hand

def start_game():
    # Initial hands
    player_hand = deal_hand()
    banker_hand = deal_hand()

    player_hand = draw_additional_card(player_hand)
    banker_hand = draw_additional_card(banker_hand)

    player_total = hand_total(player_hand)
    banker_total = hand_total(banker_hand)


    player_hand_label = Label(text=f"Player Hand: {player_hand} (Total: {player_total})")
    banker_hand_label = Label(text=f"Banker Hand: {banker_hand} (Total: {banker_total})")



    if player_total > banker_total:
            winner = "Player wins!"
    elif banker_total > player_total:
            winner = "Banker wins!"
    else:
            winner = "It's a tie!"
    
    
    messagebox.showinfo("Game Result", winner)


root = Tk()
root.title("Baccarat")
root.geometry("500x400")


title_label = Label(root, text="Baccarat Game", font=("Helvetica", 16))
title_label.pack(pady=10)


player_hand_label = Label(root, text="Player Hand: --", font=("Helvetica", 12))
player_hand_label.pack(pady=5)

banker_hand_label = Label(root, text="Banker Hand: --", font=("Helvetica", 12))
banker_hand_label.pack(pady=5)


start_button = Button(root, text="Start Game", font=("Helvetica", 14), command=start_game)
start_button.pack(pady=20)


root.mainloop()
