import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
import os
import sys
from PIL import Image, ImageTk
from game_68.logic_68 import DEALER_PATTERNS
import pygame

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


CARD_WIDTH = 100
CARD_HEIGHT = 140
CARD_DIR = "assets/deck"

def show_game_screen(win):
    win.used_cards = set()
    win.guess_attempts = 0
    win.dealer_choices = []
    win.guessed_patterns = [] 
    setup_new_round(win)

def format_card_name(filename):
    return filename.replace(".png", "").replace("_", " ").title() if filename else "None"

def is_multi_card_rule(rule):
    return rule.__code__.co_argcount == 1 and 'cards' in rule.__code__.co_varnames[0]

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

    # Reset the game state
    for widget in win.winfo_children():
        widget.destroy()

    # Reset the dealer pattern if no guesses have been made
    if win.guess_attempts == 0:
        pattern_name, pattern_rule = random.choice(list(DEALER_PATTERNS.items()))
        win.dealer_pattern_name = pattern_name
        win.dealer_rule = pattern_rule
        win.dealer_choices.clear()

    # Display the number of guess attempts
    win.guess_counter_label = tk.Label(
        win,
        text=f"Guesses: {win.guess_attempts}/3",
        font=("Georgia", 12, "bold"),
        bg="white",
        fg="#555"
    )
    win.guess_counter_label.place(x=10, y=10)

    joined_guesses = ", ".join(win.guessed_patterns) if win.guessed_patterns else "None"

    # Display the guessed patterns
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
        text="Art Dealer Game Grades 6-8",
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

    # set up frames for card display and interaction
    card_frame = tk.Frame(win, bg="white")
    card_frame.pack(pady=40)

    interaction_frame = tk.Frame(win, bg="white")
    interaction_frame.pack(padx=20, pady=20)

    # Load card images from the CARD_DIR
    card_filenames = [f for f in os.listdir(CARD_DIR) if f.endswith(".png")]


    if len(card_filenames) < 4:
        messagebox.showinfo("No More Cards", "All cards have been used!")
        return

    # Select 4 random cards that haven't been used yet
    while True:
        selected_cards = random.sample(card_filenames, 4)
        rule = win.dealer_rule
        try:
            is_match = rule(selected_cards) if is_multi_card_rule(rule) else any(rule(card) for card in selected_cards)
        except Exception:
            is_match = False
        if is_match:
            break

    # Ensure selected cards are not already used
    win.used_cards.update(selected_cards)
    win.selected_cards = selected_cards
    win.card_images = []

    print("Dealer pattern:", win.dealer_pattern_name)
    print("Selected cards:", selected_cards)

    rule = win.dealer_rule
    
    if is_multi_card_rule(rule):
        matching_cards = selected_cards if rule(selected_cards) else []
    else:
        matching_cards = [card for card in selected_cards if rule(card)]

    # Select a random card from the matching cards
    dealer_choice = random.choice(matching_cards) if matching_cards else None
    win.dealer_choice = dealer_choice

    # add the dealer's choice to the dealer_choices list
    if dealer_choice:
        win.dealer_choices.append(dealer_choice)

    all_choices = []

    for card in win.dealer_choices:
        formatted_name = format_card_name(card)
        all_choices.append(formatted_name)


    joined_names = ", ".join(all_choices) if all_choices else "None"

    # Display the dealer's previous picks label
    win.guessed_cards_label = tk.Label(
        win,
        text=f"Dealer Picks: {joined_names}",
        font=("Georgia", 12, "bold"),
        bg="white",
        fg="#555"
    )
    win.guessed_cards_label.place(x=10, y=500)

    # Display the selected cards
    for i, card_file in enumerate(selected_cards):
        card_path = resource_path(os.path.join(CARD_DIR, card_file))
        img = Image.open(card_path).resize((CARD_WIDTH, CARD_HEIGHT))
        photo = ImageTk.PhotoImage(img)
        win.card_images.append(photo)

        # show the dealer's choice with a green border
        border_color = "green" if card_file == dealer_choice else "white"
        card_label = tk.Label(
            card_frame,
            image=photo,
            bg="white",
            highlightthickness=5,
            highlightbackground=border_color,
            relief="solid"
        )
        card_label.grid(row=0, column=i, padx=10)

    # dropdown menu for selecting the pattern
    guess_label = tk.Label(interaction_frame, text="Guess the pattern:", bg="white", font=("Georgia", 12))
    guess_label.grid(row=0, column=0, padx=5)

    guess_var = tk.StringVar()
    guess_menu = ttk.Combobox(interaction_frame, textvariable=guess_var, state="readonly",
                          values=list(DEALER_PATTERNS.keys()), font=("Georgia", 14), width=25)
    guess_menu.grid(row=0, column=1, padx=10)

    # Function to show confetti animation when the player guesses correctly
    def show_confetti():
        confetti_pieces = []
        colors = ["#FF5733", "#33FF57", "#3357FF", "#F1C40F", "#9B59B6", "#E67E22"]

        for _ in range(30):
            x = random.randint(0, win.winfo_width())
            y = random.randint(-50, 0)
            size = random.randint(5, 10)
            color = random.choice(colors)
            confetti = tk.Canvas(win, width=size, height=size, bg="white", highlightthickness=0)
            confetti.place(x=x, y=y)
            confetti.create_rectangle(0, 0, size, size, fill=color, outline="")
            confetti_pieces.append([confetti, x, y, size, random.randint(2, 5)])

        def animate():
            all_off_screen = True
            for i, (confetti, x, y, size, speed) in enumerate(confetti_pieces):
                y += speed
                confetti.place(x=x, y=y)
                confetti_pieces[i][2] = y
                if y < win.winfo_height():
                    all_off_screen = False
            if not all_off_screen:
                win.after(30, animate)
            else:
                for confetti, _, _, _, _ in confetti_pieces:
                    confetti.destroy()

        animate()

    # Function to check the guess against the dealer's pattern
    def check_guess():
        guess = guess_var.get()
        if not guess:
            messagebox.showwarning("No Guess", "Please select a pattern to guess.")
            return

        win.guess_attempts += 1
        win.guess_counter_label.config(text=f"Guesses: {win.guess_attempts}/3")

        win.guessed_patterns.append(guess)
        win.guessed_patterns_label.config(
        text=f"Guessed Patterns: {', '.join(win.guessed_patterns)}"
        )

        # Check if the guess is correct, if it matches the dealer's pattern, then show confetti
        if guess == win.dealer_pattern_name:
            show_confetti()
            correct_sound.play()
            messagebox.showinfo("Correct!", "🎉 You guessed the dealer's pattern!")
            # Reset the game for new round
            win.guess_attempts = 0
            win.guessed_patterns.clear()
            setup_new_round(win)
        # if the guess is incorrect, check how many attempts have been made
        # if it's 3 or more, then show game over
        elif win.guess_attempts >= 3:
            game_over_sound.play()
            messagebox.showinfo("Game Over", f"The correct pattern was: {win.dealer_pattern_name}")
            win.guess_attempts = 0
            win.guessed_patterns.clear()
            setup_new_round(win)
        # if the guess is incorrect and less than 3 attempts have been made, then show try again message
        else:
            remaining = 3 - win.guess_attempts
            try_again_sound.play()
            messagebox.showwarning("Try Again", f"Incorrect. You have {remaining} guess{'es' if remaining > 1 else ''} left.")
            setup_new_round(win)

    # guess button
    guess_btn = tk.Button(interaction_frame, text="Submit Guess", font=("Georgia", 12), bg="#FFD700", command=check_guess)
    guess_btn.grid(row=0, column=2, padx=10)