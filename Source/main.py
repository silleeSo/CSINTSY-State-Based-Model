import tkinter as tk
import subprocess 
from tkinter.scrolledtext import ScrolledText

# Create the main window
root = tk.Tk()
root.title("MCO1 - State Based Model - CSINTSY - S13 - GRP3")

# Create a menu frame
menu_frame = tk.Frame(root)
menu_frame.pack(pady=10)

# Create a welcome message
welcome_label = tk.Label(menu_frame, text="Choose a Search Algorithm", font=("Helvetica", 16))
welcome_label.pack(pady=10, padx=10)

# Function to open AStar GUI in another file
def open_astar_gui():
    subprocess.Popen(["python", "astarGUI.py"])

# Button to open AStar GUI
astar_button = tk.Button(menu_frame, text="AStar Search", command=open_astar_gui, width=20, height=2)
astar_button.pack(pady=10)

# Function to open Uniform Cost Search GUI in another file
def open_ucs_gui():
    subprocess.Popen(["python", "ucsGUI.py"])

# Button to open Uniform Cost Search GUI
ucs_button = tk.Button(menu_frame, text="Uniform Cost Search", command=open_ucs_gui, width=20, height=2)
ucs_button.pack(pady=10)

# Start the Tkinter main loop
root.mainloop()
