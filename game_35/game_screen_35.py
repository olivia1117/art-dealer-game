import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
import os
from PIL import Image, ImageTk
from game_35.logic_35 import DEALER_PATTERNS
import pygame

pygame.mixer.init()
correct_sound = pygame.mixer.Sound('assets/sounds/correct_guess.wav')
try_again_sound = pygame.mixer.Sound('assets/sounds/try_again.mp3')
game_over_sound = pygame.mixer.Sound('assets/sounds/game_over.wav')

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
    if filename:
        name = filename.replace(".png", "").replace("_", " ").title()
        return name
    else:
        return "None"

def is_multi_card_rule(rule):
    # Expanded without __code__.co_argcount (you might want to change logic if needed)
    # Here just assume if callable and accepts one argument named 'cards'
    # For simplicity, we'll keep original:
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
    children = win.winfo_children()
    for child in children:
        if isinstance(child, tk.Canvas) and child not in getattr(win, "card_images", []):
            try:
                child.destroy()
            except Exception:
                pass

    # Destroy all widgets before setting up new round
    children = win.winfo_children()
    for widget in children:
        try:
            widget.destroy()
        except Exception:
            pass

    # Reset the dealer pattern if no guesses have been made
    if win.guess_attempts == 0:
        patterns = list(DEALER_PATTERNS.items())
        index = random.randint(0, len(patterns) - 1)
        pattern_name = patterns[index][0]
        pattern_rule = patterns[index][1]
        win.dealer_pattern_name = pattern_name
        win.dealer_rule = pattern_rule
        win.dealer_choices.clear()

    # Display the number of guess attempts
    win.guess_counter_label = tk.Label(
        win,
        text="Guesses: " + str(win.guess_attempts) + "/3",
        font=("Georgia", 12, "bold"),
        bg="white",
        fg="#555"
    )
    win.guess_counter_label.place(x=10, y=10)

    # Display the guessed patterns (expanded join)
    if win.guessed_patterns:
        joined_guesses = ""
        for i in range(len(win.guessed_patterns)):
            joined_guesses += win.guessed_patterns[i]
            if i != len(win.guessed_patterns) - 1:
                joined_guesses += ", "
    else:
        joined_guesses = "None"

    win.guessed_patterns_label = tk.Label(
        win,
        text="Guessed Patterns: " + joined_guesses,
        font=("Georgia", 12, "bold"),
        bg="white",
        fg="#555"
    )
    win.guessed_patterns_label.place(x=10, y=520)

    title = tk.Label(
        win,
        text="Art Dealer Game Grades 3-5",
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

    # Frames for card display and interaction
    card_frame = tk.Frame(win, bg="white")
    card_frame.pack(pady=40)

    interaction_frame = tk.Frame(win, bg="white")
    interaction_frame.pack(padx=20, pady=20)

    # Load all card filenames (expanded)
    card_filenames = []
    all_files = os.listdir(CARD_DIR)
    for f in all_files:
        if f.endswith(".png"):
            card_filenames.append(f)

    if len(card_filenames) < 4:
        messagebox.showinfo("No More Cards", "All cards have been used!")
        return

    # Loop until a valid selection of cards matching dealer rule is found
    while True:
        selected_cards = random.sample(card_filenames, 4)
        rule = win.dealer_rule
        if is_multi_card_rule(rule):
            try:
                is_match = rule(selected_cards)
            except Exception:
                is_match = False
        else:
            is_match = False
            for card in selected_cards:
                try:
                    if rule(card):
                        is_match = True
                        break
                except Exception:
                    pass
        if is_match:
            break

    # Update used cards and selected cards
    for card in selected_cards:
        win.used_cards.add(card)
    win.selected_cards = selected_cards
    win.card_images = []

    print("Dealer pattern:", win.dealer_pattern_name)
    print("Selected cards:", selected_cards)

    rule = win.dealer_rule
    if is_multi_card_rule(rule):
        try:
            if rule(selected_cards):
                matching_cards = selected_cards
            else:
                matching_cards = []
        except Exception:
            matching_cards = []
    else:
        matching_cards = []
        for card in selected_cards:
            try:
                if rule(card):
                    matching_cards.append(card)
            except Exception:
                pass

    if matching_cards:
        dealer_choice = random.choice(matching_cards)
    else:
        dealer_choice = None
    win.dealer_choice = dealer_choice

    if dealer_choice:
        win.dealer_choices.append(dealer_choice)

    # Expanded formatting dealer choices
    all_choices = []
    for card in win.dealer_choices:
        formatted_name = format_card_name(card)
        all_choices.append(formatted_name)

    if all_choices:
        joined_names = ""
        for i in range(len(all_choices)):
            joined_names += all_choices[i]
            if i != len(all_choices) - 1:
                joined_names += ", "
    else:
        joined_names = "None"

    win.guessed_cards_label = tk.Label(
        win,
        text="Dealer Picks: " + joined_names,
        font=("Georgia", 12, "bold"),
        bg="white",
        fg="#555"
    )
    win.guessed_cards_label.place(x=10, y=500)

    # Display cards with images and highlight dealer choice
    for i in range(len(selected_cards)):
        card_file = selected_cards[i]
        card_path = os.path.join(CARD_DIR, card_file)
        img = Image.open(card_path)
        img = img.resize((CARD_WIDTH, CARD_HEIGHT))
        photo = ImageTk.PhotoImage(img)
        win.card_images.append(photo)

        if card_file == dealer_choice:
            border_color = "green"
        else:
            border_color = "white"

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
    guess_menu = ttk.Combobox(
        interaction_frame,
        textvariable=guess_var,
        state="readonly",
        values=list(DEALER_PATTERNS.keys()),
        font=("Georgia", 14),
        width=25
    )
    guess_menu.grid(row=0, column=1, padx=10)

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
            for i in range(len(confetti_pieces)):
                confetti, x, y, size, speed = confetti_pieces[i]
                y += speed
                confetti.place(x=x, y=y)
                confetti_pieces[i][2] = y
                if y < win.winfo_height():
                    all_off_screen = False
            if not all_off_screen:
                win.after(30, animate)
            else:
                for i in range(len(confetti_pieces)):
                    confetti = confetti_pieces[i][0]
                    if confetti.winfo_exists():
                        confetti.destroy()

        animate()

    def check_guess():
        guess = guess_var.get()
        if not guess:
            messagebox.showwarning("No Guess", "Please select a pattern to guess.")
            return

        win.guess_attempts += 1
        win.guess_counter_label.config(text="Guesses: " + str(win.guess_attempts) + "/3")

        # Append guess to guessed_patterns
        win.guessed_patterns.append(guess)

        # Update guessed_patterns_label text (expanded join)
        if win.guessed_patterns:
            text = ""
            for i in range(len(win.guessed_patterns)):
                text += win.guessed_patterns[i]
                if i != len(win.guessed_patterns) - 1:
                    text += ", "
        else:
            text = "None"
        win.guessed_patterns_label.config(text="Guessed Patterns: " + text)

        if guess == win.dealer_pattern_name:
            show_confetti()
            correct_sound.play()
            messagebox.showinfo("Correct!", "🎉 You guessed the dealer's pattern!")
            win.guess_attempts = 0
            win.guessed_patterns.clear()
            setup_new_round(win)
        elif win.guess_attempts >= 3:
            game_over_sound.play()
            messagebox.showinfo("Game Over", "The correct pattern was: " + win.dealer_pattern_name)
            win.guess_attempts = 0
            win.guessed_patterns.clear()
            setup_new_round(win)
        else:
            remaining = 3 - win.guess_attempts
            try_again_sound.play()
            messagebox.showwarning(
                "Try Again",
                "Incorrect. You have " + str(remaining) + " guess" + ("es" if remaining > 1 else "") + " left."
            )
            setup_new_round(win)

    guess_btn = tk.Button(
        interaction_frame,
        text="Submit Guess",
        font=("Georgia", 12),
        bg="#FFD700",
        command=check_guess
    )
    guess_btn.grid(row=0, column=2, padx=10)
