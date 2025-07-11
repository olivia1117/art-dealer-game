import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
import os
import sys
from PIL import Image, ImageTk
from game_k2.logic_k2 import DEALER_PATTERNS
import pygame

# Initialize pygame mixer for sound effects
def resource_path(relative_path):
    # Get absolute path to resource, works for dev and for PyInstaller .exe
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Initialize pygame mixer for sound effects
pygame.mixer.init()
correct_sound = pygame.mixer.Sound(resource_path('assets/sounds/correct_guess.wav'))
try_again_sound = pygame.mixer.Sound(resource_path('assets/sounds/try_again.mp3'))
game_over_sound = pygame.mixer.Sound(resource_path('assets/sounds/game_over.wav'))


# Constants for card dimensions and directory
CARD_WIDTH = 100
CARD_HEIGHT = 140
CARD_DIR = "assets/deck"


# show the game screen
def show_game_screen(win):
    win.used_cards = set()
    win.guess_attempts = 0
    win.dealer_choices = []
    win.guessed_patterns = [] 

    
    setup_new_round(win)

# Function to format card names for display and replace underscores with spaces
def format_card_name(filename):
    if filename:
        formatted = filename.replace(".png", "")
        formatted = formatted.replace("_", " ")
        return formatted.title()
    else:
        return "None"


def setup_new_round(win):

    # Cancel confetti animation if it's running
    if hasattr(win, "confetti_after_id"):
        try:
            win.after_cancel(win.confetti_after_id)
        except Exception:
            pass
        del win.confetti_after_id

    # Destroy any lingering confetti canvases
    for child in win.winfo_children():
        if isinstance(child, tk.Canvas) and child not in win.card_images:
            try:
                child.destroy()
            except Exception:
                pass


    for widget in win.winfo_children():
        widget.destroy()

    if win.guess_attempts == 0:
        win.used_cards.clear()
        pattern_name, pattern_rule = random.choice(list(DEALER_PATTERNS.items()))
        win.dealer_pattern_name = pattern_name
        win.dealer_rule = pattern_rule
        win.dealer_choices.clear()
        win.guessed_patterns = []

    win.guess_counter_label = tk.Label(
        win,
        text=f"Guesses: {win.guess_attempts}/3",
        font=("Georgia", 12, "bold"),
        bg="white",
        fg="#555"
    )
    win.guess_counter_label.place(x=10, y=10)

    # keep track of previous guesses for the user to see
    
    joined_guesses = "None" 
    if win.guessed_patterns:
        joined_guesses = ""
        for guess in win.guessed_patterns:
            if joined_guesses: 
                joined_guesses += ", "
            joined_guesses += guess


    win.guessed_patterns_label = tk.Label(
        win,
        text=f"Guessed Patterns: {joined_guesses}",
        font=("Georgia", 12, "bold"),
        bg="white",
        fg="#555"
    )
    win.guessed_patterns_label.place(x=10, y=520)


    title = tk.Label(
        win,
        text="Art Dealer Game Grades K-2",
        font=("Georgia", 24, "bold"),
        bg="white",
        fg="#333"
    )
    title.pack(pady=20)

    instructions = tk.Label(
        win,
        text="Lay out 4 cards and see what the Art Dealer buys!",
        font=("Georgia", 14),
        bg="white"
    )
    instructions.pack(pady=10)

    card_frame = tk.Frame(win, bg="white")
    card_frame.pack(pady=40)

    interaction_frame = tk.Frame(win, bg="white")
    interaction_frame.pack(padx=20, pady=20)



    # Get all card filenames and filter out used cards
    # this is to make sure that each card is only used once
    # until the deck is reset

    all_card_filenames = []
    for f in os.listdir(CARD_DIR):
        if f.endswith(".png"):
            all_card_filenames.append(f)

    
    available_cards = []
    for card in all_card_filenames:
        if card not in win.used_cards:
            available_cards.append(card)

 
    # If there are not enough cards left, show a message and return
    if len(available_cards) < 4:
        messagebox.showinfo("No More Cards", "All cards have been used!")
        return

    # Randomly select 4 cards that match the dealer's rule
    # from the available deck as long as the rule is met and it 
    # doesn't take too long to find a valid set
    # otherwise it resets the deck 

    MAX_ATTEMPTS = 1000
    attempts = 0
    rule = win.dealer_rule
    selected_cards = None

    while attempts < MAX_ATTEMPTS:
        attempts += 1
        selected = random.sample(available_cards, 4)
        try:
            if any(rule(card) for card in selected):
                selected_cards = selected
                break
        except Exception as e:
            print("Error applying rule:", e)
            break

    if selected_cards is None:
        messagebox.showerror("No Valid Cards", "Couldn't find a valid set of cards. Resetting deck.")
        win.used_cards.clear()  # Force reset
        setup_new_round(win)
        return


    win.used_cards.update(selected_cards)
    win.selected_cards = selected_cards
    win.card_images = []

    print("Dealer pattern:", win.dealer_pattern_name)
    print("Selected cards:", selected_cards)

    # Find matching cards based on the dealer's rule
    # then checks which selected cards match the dealer's rule
    # and dealer's choice is stored

    matching_cards = []
    for card in selected_cards:
        if rule(card):
            matching_cards.append(card)

    dealer_choice = None
    if matching_cards:
        dealer_choice = random.choice(matching_cards)

    win.dealer_choice = dealer_choice

    if dealer_choice:
        win.dealer_choices.append(dealer_choice)

    all_choices = []
    for card in win.dealer_choices:
        all_choices.append(format_card_name(card))

    joined_names = "None"
    if all_choices:
        joined_names = ""
        for name in all_choices:
            if joined_names:
                joined_names += ", "
            joined_names += name



    win.guessed_cards_label = tk.Label(
        win,
        text=f"Dealer Picks: {joined_names}",
        font=("Georgia", 12, "bold"),
        bg="white",
        fg="#555"
    )
    win.guessed_cards_label.place(x=10, y=500)


    # display the cards on the screen and format it correctly
    for i in range(len(selected_cards)):
        card_file = selected_cards[i]
        card_path = resource_path(os.path.join(CARD_DIR, card_file))
        img = Image.open(card_path).resize((CARD_WIDTH, CARD_HEIGHT))
        photo = ImageTk.PhotoImage(img)
        win.card_images.append(photo)


        # highlight the dealer's choice card with a green border         
        border_color = "white"
        if card_file == dealer_choice:
            border_color = "green"
        
        
        card_label = tk.Label(
            card_frame,
            image=photo,
            bg="white",
            highlightthickness=5,
            highlightbackground=border_color,
            relief="solid"
        )
        card_label.grid(row=0, column=i, padx=10)

    # Dropdown menu for guesses
    guess_label = tk.Label(interaction_frame, text="Guess the pattern:", bg="white", font=("Georgia", 12))
    guess_label.grid(row=0, column=0, padx=5)

    guess_var = tk.StringVar()
    guess_menu = ttk.Combobox(interaction_frame, textvariable=guess_var, state="readonly",
                          values=list(DEALER_PATTERNS.keys()), font=("Georgia", 14), width=25)
    guess_menu.grid(row=0, column=1, padx=10)

    # when the user successfully guesses within 3 tries, trigger confetti pieces on screen
    def show_confetti():
        confetti_pieces = []
        colors = ["#FF5733", "#33FF57", "#3357FF", "#F1C40F", "#9B59B6", "#E67E22"]

        for _ in range(30):
            x = random.randint(0, win.winfo_width())
            y = random.randint(-50, 0)
            size = random.randint(5, 10)
            color = random.choice(colors)
            confetti = tk.Canvas(win, width=size, height=size, bg="white", highlightthickness=0)
            # confetti.place(x=x, y=y)
            if str(confetti) in win.children or confetti.winfo_exists():
                confetti.place(x=x, y=y)


            confetti.create_rectangle(0, 0, size, size, fill=color, outline="")
            confetti_pieces.append([confetti, x, y, size, random.randint(2, 5)])

        def animate():
            all_off_screen = True
            for i, (confetti, x, y, size, speed) in enumerate(confetti_pieces):
                y += speed
                # confetti.place(x=x, y=y)
                if str(confetti) in win.children or confetti.winfo_exists():
                    confetti.place(x=x, y=y)

                confetti_pieces[i][2] = y
                if y < win.winfo_height():
                    all_off_screen = False
            if not all_off_screen:
                win.after(30, animate)
            else:
                for confetti, _, _, _, _ in confetti_pieces:
                    # confetti.destroy()
                    if confetti.winfo_exists():
                        confetti.destroy()


        animate()

    
# function for checking if the user's guess matches the dealer's pattern
    def check_guess():
        guess = guess_var.get()
        # if the user doesn't select a pattern, show warning message
        if not guess:
            messagebox.showwarning("No Guess", "Please select a pattern to guess.")
            return


        win.guess_attempts += 1
        win.guess_counter_label.config(text=f"Guesses: {win.guess_attempts}/3")

        # append the guess to the list of guessed patterns
        # this allows the user to see their previous guesses
        win.guessed_patterns.append(guess)
        win.guessed_patterns_label.config(
        text=f"Guessed Patterns: {', '.join(win.guessed_patterns)}"
        )


        # if the guess matches the dealer's pattern, show confetti and reset for next round
        if guess == win.dealer_pattern_name:
            show_confetti()
            correct_sound.play()
            messagebox.showinfo("Correct!", "🎉 You guessed the dealer's pattern!")
            win.guess_attempts = 0
            win.guessed_patterns.clear()  # Clear guessed patterns for next round
            setup_new_round(win)
        # if the guess does not match the dealer's pattern, check how many attempts have been made and show message
        elif win.guess_attempts >= 3:
            game_over_sound.play()
            messagebox.showinfo("Game Over", f"The correct pattern was: {win.dealer_pattern_name}")
            win.guess_attempts = 0
            win.guessed_patterns.clear()  
            setup_new_round(win)
        # if the guess is incorrect but attempts are still available, show try again message
        else:
            remaining = 3 - win.guess_attempts
            try_again_sound.play()
            messagebox.showwarning("Try Again", f"Incorrect. You have {remaining} guess{'es' if remaining > 1 else ''} left.")
            win.used_cards.update(win.selected_cards)  # prevent repeats during same round
            setup_new_round(win)

    # Guess button formatting
    guess_btn = tk.Button(interaction_frame, text="Submit Guess", font=("Georgia", 12), bg="#FFD700", command=check_guess)
    guess_btn.grid(row=0, column=2, padx=10)



