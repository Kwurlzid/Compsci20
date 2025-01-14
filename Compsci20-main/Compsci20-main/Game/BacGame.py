import random
from tkinter import *
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk

suits = ["S", "D", "C", "H"]
values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "K", "Q"]

deck = []
for suit in suits:
    for val in values:
        deck.append(val + suit)

deck = deck * 8 
random.shuffle(deck)

def card_value(card):
    card_value = card[:-1]
    
    if card_value in ['J', 'Q', 'K', '10']:
        return 0
    elif card_value == 'A':
        return 1
    else:
        return int(card_value)

def deal_hand():
    hand = [deck.pop(), deck.pop()]
    return hand

def hand_total(hand):
    total = sum(card_value(card) for card in hand)
    return total % 10

def draw_additional_card(hand):
    if hand_total(hand) <= 5:
        hand.append(deck.pop())
    return hand

def start_game():
    global player_images, banker_images

    player_hand = deal_hand()
    banker_hand = deal_hand()

    player_hand = draw_additional_card(player_hand)
    banker_hand = draw_additional_card(banker_hand)

    player_total = hand_total(player_hand)
    banker_total = hand_total(banker_hand)

    player_hand_label.configure(text=f"Player Hand: {player_hand} (Total: {player_total})")
    banker_hand_label.configure(text=f"Banker Hand: {banker_hand} (Total: {banker_total})")

    if player_total > banker_total:
        winner = "Player wins!"
    elif banker_total > player_total:
        winner = "Banker wins!"
    else:
        winner = "It's a tie!"

    messagebox.showinfo("Game Result", winner)

    display_cards(player_hand, banker_hand)

def display_cards(player_hand, banker_hand):
    for image_label in player_images:
        image_label.destroy()
    for image_label in banker_images:
        image_label.destroy()

    #player hand image
    for card in player_hand:
        card_image = PhotoImage(file=f"{card}.png")
        label = Label(player_frame, image=card_image)
        label.image = card_image
        label.pack(side=LEFT)
        player_images.append(label)

    # banker hand image
    for card in banker_hand:
        card_image = PhotoImage(file=f"{card}.png")
        label = Label(banker_frame, image=card_image)
        label.image = card_image
        label.pack(side=LEFT)
        banker_images.append(label)

root = Tk()
root.title("Baccarat")
root.geometry("800x600")
root.resizable(width=False, height=False)
BC =Image.open("Table.png").resize((800, 600), Image.LANCZOS)
BK= ImageTk.PhotoImage(BC)
Background =Label(root, image=BK)
Background.place(x=0,y=0)

player_frame = Frame(root, bg = "green")
player_frame.pack(side=LEFT, padx=20, pady=20)

banker_frame = Frame(root)
banker_frame.pack(side=RIGHT, padx=20, pady=20)

player_card_frame = Frame(player_frame, bg = "pink")
player_card_frame.pack(side=TOP)

banker_card_frame = Frame(banker_frame)
banker_card_frame.pack(side=TOP)

player_hand_label = Label(player_card_frame, text="Player Hand: --", font=("Helvetica", 12), bg = "pink")
player_hand_label.pack(pady=5)

banker_hand_label = Label(banker_card_frame, text="Banker Hand: --", font=("Helvetica", 12))
banker_hand_label.pack(pady=5)

title_label = Label(root, text="Baccarat", font=("Helvetica", 16))
title_label.pack(pady=10)

player_images = []
banker_images = []

start_button = Button(root, text="Start Game", font=("Helvetica", 14), command=start_game)
start_button.pack(pady=20)

root.mainloop()
