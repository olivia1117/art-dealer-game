import tkinter as tk
from .game_screen_35 import show_game_screen

def run_35_game():
    win = tk.Tk()
    win.title("Art Dealer Game: Grades 3-5")
    win.geometry("800x600")
    win.configure(bg="white")
    win.resizable(True, True)

    show_game_screen(win)

    win.mainloop()