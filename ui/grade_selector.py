# ui/grade_selector.py

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # PIL for image handling
from k2_game.k2_main import run_k2_game
from k2_game.game_screen_k2 import show_game_screen

def launch_main_menu():
    root = tk.Tk()
    root.title("The Art Dealer Game")
    root.geometry("800x600")
    root.resizable(True, True) #this allows for resizing the window 

    # Load and display background
    bg_image = Image.open("assets/background.png")
    bg_image = bg_image.resize((800, 600))  # Resize to fit window
    bg_photo = ImageTk.PhotoImage(bg_image)

    background_label = tk.Label(root, image=bg_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Overlay Frame (to place widgets on top of background)
    overlay = tk.Frame(root, bg="black")  # transparent bg
    overlay.place(relx=0.5, rely=0.2, anchor="n")


    # Title Label
    title_label = tk.Label(
        overlay,
        text="Welcome to the Art Dealer Game!",
        font=("Georgia", 24, "bold"),
        fg="white",
        bg="black"
    )
    title_label.pack(pady=20)

    # Button Frame
    button_frame = tk.Frame(root, bg="black")
    button_frame.place(relx=0.5, rely=0.7, anchor="center")

    # Custom-colored Buttons
    btn_k2 = tk.Button(button_frame, text="Grades K–2", font=("Arial", 14), width=15,
                       bg="#FF9999", fg="black", activebackground="#FF6666",
                       command=lambda: launch_k2_game(root))

    btn_35 = tk.Button(button_frame, text="Grades 3–5", font=("Arial", 14), width=15,
                       bg="#99CCFF", fg="black", activebackground="#6699FF",
                       command=lambda: launch_35_game(root))

    btn_68 = tk.Button(button_frame, text="Grades 6–8", font=("Arial", 14), width=15,
                       bg="#99FF99", fg="black", activebackground="#66CC66",
                       command=lambda: launch_68_game(root))

    # Layout
    btn_k2.grid(row=0, column=0, padx=15, pady=10)
    btn_35.grid(row=0, column=1, padx=15, pady=10)
    btn_68.grid(row=0, column=2, padx=15, pady=10)

    root.mainloop()


# Placeholder handlers
def launch_k2_game(root):
    root.destroy()  # Close the grade selector window
    run_k2_game()   # Launch the K-2 game window

def launch_35_game(root):
    messagebox.showinfo("3–5 Mode", "Starting the 3–5 version of the game!")

def launch_68_game(root):
    messagebox.showinfo("6–8 Mode", "Starting the 6–8 version of the game!")