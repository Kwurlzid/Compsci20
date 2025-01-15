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

balance = 100
player_bet = 0
banker_bet = 0
tie_bet = 0

chips = [5, 25, 50, 100]

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

def update_balance():
    balance_label.config(text=f"Balance: ${balance}")
    player_bet_label.config(text=f"Player Bet: ${player_bet}")
    banker_bet_label.config(text=f"Banker Bet: ${banker_bet}")
    tie_bet_label.config(text=f"Tie Bet: ${tie_bet}")

def bet_player(amount):
    global player_bet, balance, banker_bet
    if balance >= amount:
        if banker_bet > 0:
            messagebox.showerror("Error", "Cannot bet on Player and Banker at the same time!")
        else:
            player_bet += amount
            balance -= amount
            update_balance()
    else:
        messagebox.showerror("Error", "Insufficient balance!")

def bet_banker(amount):
    global banker_bet, balance, player_bet
    if balance >= amount:
        if player_bet > 0:
            messagebox.showerror("Error", "Cannot bet on Player and Banker at the same time!")
        else:
            banker_bet += amount
            balance -= amount
            update_balance()
    else:
        messagebox.showerror("Error", "Insufficient balance!")

def bet_tie(amount):
    global tie_bet, balance
    if balance >= amount:
        tie_bet += amount
        balance -= amount
        update_balance()
    else:
        messagebox.showerror("Error", "Insufficient balance!")

def calculate_winnings(player_total, banker_total):
    global balance, player_bet, banker_bet, tie_bet

    winnings = 0
    if player_total > banker_total:
        winner = "Player"
        winnings = player_bet * 2  
    elif banker_total > player_total:
        winner = "Banker"
        winnings = banker_bet * 1.95 
    else:
        winner = "Tie"
        winnings = tie_bet * 9

    balance += winnings
    player_bet, banker_bet, tie_bet = 0, 0, 0

    update_balance()
    
    messagebox.showinfo("Game Result", f"{winner} wins! You won ${winnings:.2f}")


def start_game():
    global player_images, banker_images, player_bet, banker_bet, tie_bet

    player_hand = deal_hand()
    banker_hand = deal_hand()

    player_hand = draw_additional_card(player_hand)
    banker_hand = draw_additional_card(banker_hand)

    player_total = hand_total(player_hand)
    banker_total = hand_total(banker_hand)

    player_hand_label.configure(text=f"Player Hand: {player_hand} (Total: {player_total})")
    banker_hand_label.configure(text=f"Banker Hand: {banker_hand} (Total: {banker_total})")

    display_cards(player_hand, banker_hand)

    calculate_winnings(player_total, banker_total)

def display_cards(player_hand, banker_hand):
    # clear cards that were pulled last round
    for image_label in player_images:
        image_label.destroy()
    for image_label in banker_images:
        image_label.destroy()

    # player hand pic
    for card in player_hand:
        card_image = PhotoImage(file=f"{card}.png")
        label = Label(player_frame, image=card_image)
        label.image = card_image
        label.pack(side=LEFT)
        player_images.append(label)

    # banker hand pic
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

#Placing all widgets
BC = Image.open("Table.png").resize((800, 600), Image.LANCZOS)
BK = ImageTk.PhotoImage(BC)
Background = Label(root, image=BK)
Background.place(x=0, y=0)

player_frame = Frame(root, bg="green")
player_frame.pack(side=LEFT, padx=20, pady=20)

banker_frame = Frame(root)
banker_frame.pack(side=RIGHT, padx=20, pady=20)

player_card_frame = Frame(player_frame, bg="pink")
player_card_frame.pack(side=TOP)

banker_card_frame = Frame(banker_frame)
banker_card_frame.pack(side=TOP)

player_hand_label = Label(player_card_frame, text="Player Hand: --", font=("Bell Gothic Std Black", 12), bg="pink")
player_hand_label.pack(pady=5)

banker_hand_label = Label(banker_card_frame, text="Banker Hand: --", font=("Bell Gothic Std Black", 12))
banker_hand_label.pack(pady=5)

title_label = Label(root, text="Baccarat", font=("Bell Gothic Std Black", 16))
title_label.pack(pady=10)

player_images = []
banker_images = []

bet_player_button = Button(player_frame, text="Bet Player $5", font=("Bell Gothic Std Black", 12), command=lambda: bet_player(5))
bet_player_button.pack(pady=5)

bet_banker_button = Button(banker_frame, text="Bet Banker $5", font=("Bell Gothic Std Black", 12), command=lambda: bet_banker(5))
bet_banker_button.pack(pady=5)

bet_tie_button = Button(root, text="Bet Tie $5", font=("Bell Gothic Std Black", 12), command=lambda: bet_tie(5))
bet_tie_button.pack(pady=5)

start_button = Button(root, text="Start Game", font=("Bell Gothic Std Black", 14), command=start_game)
start_button.pack(pady=20)

balance_label = Label(root, text=f"Balance: ${balance}", font=("Bell Gothic Std Black", 14))
balance_label.pack(pady=10)

player_bet_label = Label(root, text=f"Player Bet: ${player_bet}", font=("Bell Gothic Std Black", 12))
player_bet_label.pack()

banker_bet_label = Label(root, text=f"Banker Bet: ${banker_bet}", font=("Bell Gothic Std Black", 12))
banker_bet_label.pack()

tie_bet_label = Label(root, text=f"Tie Bet: ${tie_bet}", font=("Bell Gothic Std Black", 12))
tie_bet_label.pack()

root.mainloop()
