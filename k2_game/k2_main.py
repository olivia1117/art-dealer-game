import tkinter as tk
from .game_screen_k2 import show_game_screen

def run_k2_game():
    win = tk.Tk()
    win.title("Art Dealer Game: Grades K–2")
    win.geometry("800x600")
    win.configure(bg="white")
    win.resizable(True, True)

    show_game_screen(win)

    win.mainloop()