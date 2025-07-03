import tkinter as tk

def show_game_screen(win):
    title = tk.Label(
        win,
        text="Art Dealer Game – K–2",
        font=("Comic Sans MS", 24, "bold"),
        bg="white",
        fg="#333"
    )
    title.pack(pady=20)

    instructions = tk.Label(
        win,
        text="Lay out 4 cards and see what the Art Dealer buys!",
        font=("Comic Sans MS", 14),
        bg="white"
    )
    instructions.pack(pady=10)

    # Placeholder for card slots or deck interactions
    card_frame = tk.Frame(win, bg="white")
    card_frame.pack(pady=40)

    for i in range(4):
        tk.Label(card_frame, text=f"Card Slot {i+1}", width=15, height=4, relief="groove").grid(row=0, column=i, padx=10)

    # Add a Next or Submit button
    tk.Button(
        win,
        text="Submit Cards",
        font=("Comic Sans MS", 12, "bold"),
        bg="#66CCFF",
        command=lambda: print("Checking cards...")
    ).pack(pady=20)
