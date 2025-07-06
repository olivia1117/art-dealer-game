import tkinter as tk
from .game_screen_68 import show_game_screen

def run_68_game():
    win = tk.Tk()
    win.title("Art Dealer Game: Grades 6-8")
    win.geometry("800x600")
    win.configure(bg="white")
    win.resizable(True, True)

    show_game_screen(win)

    win.mainloop()