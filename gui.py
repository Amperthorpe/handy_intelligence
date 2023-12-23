import tkinter as tk
from tkinter import simpledialog

# Create a new Tkinter window
root = tk.Tk()
# Hide the main window
root.withdraw()


def prompt_popup():
    return simpledialog.askstring(title="Prompt", prompt="Please enter prompt:")
