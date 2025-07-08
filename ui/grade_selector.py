# ui/grade_selector.py

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk 

from ui.instructions import show_instructions_screen

from game_k2.main_k2 import run_k2_game
from game_k2.game_screen_k2 import show_game_screen

from game_35.main_35 import run_35_game
from game_35.game_screen_35 import show_game_screen

from game_68.main_68 import run_68_game
from game_68.game_screen_68 import show_game_screen

import pygame
import sys 
import os

def resource_path(relative_path):
    # Get absolute path to resource, works for dev and for PyInstaller .exe
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

pygame.mixer.init()
main_menu_sound = pygame.mixer.Sound(resource_path('assets/sounds/main_menu.wav'))


def launch_main_menu():

    root = tk.Tk()
    root.title("The Art Dealer Game")
    root.geometry("800x600")
    root.resizable(True, True) #this allows for resizing the window 

    # Load and display background
    bg_image = Image.open(resource_path("assets/background.png"))
    bg_image = bg_image.resize((800, 600))  
    bg_photo = ImageTk.PhotoImage(bg_image)

    background_label = tk.Label(root, image=bg_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # place widgets on top of background
    overlay = tk.Frame(root, bg="black")  
    overlay.place(relx=0.5, rely=0.2, anchor="n")

    # Play main menu sound
    main_menu_sound.play(-1)  

    # title 
    title_label = tk.Label(
        overlay,
        text="Welcome to the Art Dealer Game!",
        font=("Georgia", 24, "bold"),
        fg="white",
        bg="black"
    )
    title_label.pack(pady=20)

    # frame for the buttons
    button_frame = tk.Frame(root, bg="black")
    button_frame.place(relx=0.5, rely=0.7, anchor="center")

    # changing the button colors and fonts
    btn_k2 = tk.Button(button_frame, text="Grades K–2", font=("Arial", 14), width=15,
                       bg="#FF9999", fg="black", activebackground="#FF6666",
                       command=lambda: launch_k2_game(root))

    btn_35 = tk.Button(button_frame, text="Grades 3–5", font=("Arial", 14), width=15,
                       bg="#99CCFF", fg="black", activebackground="#6699FF",
                       command=lambda: launch_35_game(root))

    btn_68 = tk.Button(button_frame, text="Grades 6–8", font=("Arial", 14), width=15,
                       bg="#99FF99", fg="black", activebackground="#66CC66",
                       command=lambda: launch_68_game(root))
    
    btn_instructions = tk.Button(
        button_frame,
        text="How to Play",
        font=("Arial", 14),
        width=15,
        bg="#FFFF99",
        fg="black",
        activebackground="#FFEB3B",
        command=lambda: (main_menu_sound.stop(), show_instructions_screen(root, launch_main_menu))
    )
    

    # layout of the main menu buttons for grades and instructions
    btn_k2.grid(row=0, column=0, padx=15, pady=10)
    btn_35.grid(row=0, column=1, padx=15, pady=10)
    btn_68.grid(row=0, column=2, padx=15, pady=10)
    btn_instructions.grid(row=1, column=1, pady=10)  

    root.mainloop()


def launch_k2_game(root):
    root.destroy()  # Close the grade selector window
    main_menu_sound.stop()  # Stop the main menu sound
    run_k2_game()   # Launch the K-2 game window

def launch_35_game(root):
    root.destroy()  
    main_menu_sound.stop()  
    run_35_game()   # Launch the 3-5 game window

def launch_68_game(root):
    root.destroy()  
    main_menu_sound.stop()  
    run_68_game()   # Launch the 6-8 game window
