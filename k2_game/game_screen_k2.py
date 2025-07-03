import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
import os
from PIL import Image, ImageTk  # PIL for image handling
from k2_game.logic import DEALER_PATTERNS

CARD_WIDTH = 100
CARD_HEIGHT = 140
CARD_DIR = "assets/deck"

def show_game_screen(win):
    win.used_cards = set()  # Track used cards to avoid duplicates
    win.guess_attempts = 0
    setup_new_round(win)

def setup_new_round(win):
    # Clear previous round data
    for widget in win.winfo_children():
        widget.destroy()

    if win.guess_attempts == 0:
        pattern_name, pattern_rule = random.choice(list(DEALER_PATTERNS.items()))
        win.dealer_pattern_name = pattern_name
        win.dealer_rule = pattern_rule
    # # Pick a pattern
    # pattern_name, pattern_rule = random.choice(list(DEALER_PATTERNS.items()))
    # win.dealer_pattern_name = pattern_name
    # win.dealer_rule = pattern_rule
    # win.guess_attempts = 0

    # Guess counter label in top-left corner
    win.guess_counter_label = tk.Label(
        win,
        text=f"Guesses: {win.guess_attempts}/3",
        font=("Georgia", 12, "bold"),
        bg="white",
        fg="#555"
    )
    win.guess_counter_label.place(x=10, y=10)

    title = tk.Label(
        win,
        text="Art Dealer Game K–2",
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

    # Placeholder for card slots or deck interactions
    card_frame = tk.Frame(win, bg="white")
    card_frame.pack(pady=40)

    # Frame for dropdown menu and button
    interaction_frame = tk.Frame(win, bg="white")
    interaction_frame.pack(padx=20, pady=20)

    # Load all card filenames
    card_filenames = [f for f in os.listdir(CARD_DIR) if f.endswith(".png")]

    if len(card_filenames) < 4:
        messagebox.showinfo("No More Cards", "All cards have been used!")
        return

    # Pick 4 random cards
    selected_cards = random.sample(card_filenames, 4)
    win.used_cards.update(selected_cards)
    win.selected_cards = selected_cards  # Store selected cards in the window object

    # Store images to prevent garbage collection
    win.card_images = []

        # Debug prints to check matching cards
    print("Dealer pattern:", win.dealer_pattern_name)
    print("Selected cards:", selected_cards)
    for card in selected_cards:
        print(f"Card '{card}' matches pattern? {win.dealer_rule(card)}")

    matching_cards = [card for card in selected_cards if win.dealer_rule(card)]

    if matching_cards:
        dealer_choice = random.choice(matching_cards)
        print(f"Dealer chooses card: {dealer_choice}")

    else:
        dealer_choice = None
        print("No cards matched dealer pattern!")
    

    matching_cards = [f for f in selected_cards if win.dealer_rule(f)]
    dealer_choice = random.choice(matching_cards) if matching_cards else None
    win.dealer_choice = dealer_choice  # store for reference

    # Display the 4 randomly selected cards
    for i, card_file in enumerate(selected_cards):
        card_path = os.path.join(CARD_DIR, card_file)
        img = Image.open(card_path).resize((CARD_WIDTH, CARD_HEIGHT))
        photo = ImageTk.PhotoImage(img)

        win.card_images.append(photo) 

        
        # Display card with green border if dealer picked it
        border_color = "green" if card_file == dealer_choice else "white"
        card_label = tk.Label(
            card_frame,
            image=photo,
            bg="white",
            highlightthickness=3,
            highlightbackground=border_color,
            relief="solid"
        )
        card_label.grid(row=0, column=i, padx=10)

        # win.card_images.append(photo)
        # border_color = "green" if card_file == dealer_choice else "white"
        # card_label = tk.Label(card_frame, image=photo, bg=border_color, bd=3, relief="solid")
        # card_label.grid(row=0, column=i, padx=10)

        # label = tk.Label(card_frame, image=photo, bg="white")
        # label.image = photo
        # label.grid(row=0, column=i, padx=10)

    # for i in range(4):
    #     tk.Label(card_frame, text=f"Card Slot {i+1}", width=15, height=4, relief="groove").grid(row=0, column=i, padx=10)

    # Dropdown menu for guesses
    guess_label = tk.Label(interaction_frame, text="Guess the pattern:", bg="white", font=("Georgia", 12))
    guess_label.grid(row=0, column=0, padx=5)

    guess_var = tk.StringVar()
    guess_menu = ttk.Combobox(interaction_frame, textvariable=guess_var, state="readonly",
                          values=list(DEALER_PATTERNS.keys()), font=("Georgia", 14), width=25)
    # guess_menu = tk.OptionMenu(interaction_frame, guess_var, *DEALER_PATTERNS.keys())
    # guess_menu.config(font=("Georgia", 14), width=20)
    guess_menu.grid(row=0, column=1, padx=10)

    
    def show_confetti():
        confetti_pieces = []
        colors = ["#FF5733", "#33FF57", "#3357FF", "#F1C40F", "#9B59B6", "#E67E22"]

        # Spawn 30 confetti pieces at random positions near the top
        for _ in range(30):
            x = random.randint(0, win.winfo_width())
            y = random.randint(-50, 0)  # start slightly above the window
            size = random.randint(5, 10)
            color = random.choice(colors)
            confetti = tk.Canvas(win, width=size, height=size, bg="white", highlightthickness=0)
            confetti.place(x=x, y=y)
            confetti.create_rectangle(0, 0, size, size, fill=color, outline="")
            confetti_pieces.append([confetti, x, y, size, random.randint(2, 5)])  # [widget, x, y, size, speed]

        def animate():
            all_off_screen = True
            for i, (confetti, x, y, size, speed) in enumerate(confetti_pieces):
                y += speed  # fall speed
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


    # Guess button
    def check_guess():
        guess = guess_var.get()
        if not guess:
            messagebox.showwarning("No Guess", "Please select a pattern to guess.")
            return

        win.guess_attempts += 1
        win.guess_counter_label.config(text=f"Guesses: {win.guess_attempts}/3")

        if guess == win.dealer_pattern_name:
            show_confetti()
            messagebox.showinfo("Correct!", "🎉 You guessed the dealer's pattern!")
            win.guess_attempts = 0  # Reset attempts for next round
            setup_new_round(win)

        elif win.guess_attempts >= 3:
            messagebox.showinfo("Game Over", f"The correct pattern was: {win.dealer_pattern_name}")
            win.guess_attempts = 0
            setup_new_round(win)
        else:
            remaining = 3 - win.guess_attempts
            messagebox.showwarning("Try Again", f"Incorrect. You have {remaining} guess{'es' if remaining > 1 else ''} left.")
            setup_new_round(win)

    guess_btn = tk.Button(interaction_frame, text="Submit Guess", font=("Georgia", 12), bg="#FFD700", command=check_guess)
    guess_btn.grid(row=0, column=2, padx=10)


    # # Add a Next or Submit button
    # tk.Button(
    #     win,
    #     text="Submit Cards",
    #     font=("Comic Sans MS", 12, "bold"),
    #     bg="#66CCFF",
    #     command=lambda: print("Checking cards...")
    # ).pack(pady=20)
