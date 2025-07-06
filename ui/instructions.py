import tkinter as tk
from tkinter import messagebox  
from tkinter import ttk



def show_instructions_screen(win, return_callback):
    for widget in win.winfo_children():
        widget.destroy()

    title = tk.Label(
        win,
        text="How to Play",
        font=("Georgia", 24, "bold"),
        bg="white",
        fg="#333"
    )
    title.pack(pady=20)

    instructions_text = (
        "Welcome to the Art Dealer Game!\n\n"
        "Objective:\n"
        "Try to figure out what pattern the dealer is using to buy artwork (playing cards) from you!\n\n"
        "How to Play:\n"
        "1. Four cards will be randomly displayed.\n"
        "2. The dealer will select one based on a pattern and highlight the artwork (playing card) in green that they would like to buy.\n"
        "3. Use the dropdown menu to guess the pattern.\n"
        "4. You get 3 guesses per round. Each grade level has different patterns available to guess based on difficulty. \n"
        "5. Good luck and have fun!\n\n"
        "Tip: Patterns might be based on color, suit, face value, basic poker hands, single digit prime numbers, and more!\n"
    )

    instructions = tk.Label(
        win,
        text=instructions_text,
        font=("Georgia", 14),
        justify="left",
        bg="white",
        wraplength=600
    )
    instructions.pack(pady=10)

    back_btn = tk.Button(
        win,
        text="Back to Game",
        font=("Georgia", 12),
        bg="#FFDD57",
        command=lambda: (win.destroy(), return_callback())
    )
    back_btn.pack(pady=20)
