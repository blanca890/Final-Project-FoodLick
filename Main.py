import tkinter as tk
from gui import OrderingSystemGUI
from functions import OrderingSystemLogic

if __name__ == "__main__":
    root = tk.Tk()
    try:
        root.iconbitmap("img/Logo.ico")  # Ensure this file exists
    except Exception as e:
        print(f"Error loading icon: {e}")

    # Initialize logic
    logic = OrderingSystemLogic()

    # Pass logic to GUI
    app = OrderingSystemGUI(root, logic)

    root.mainloop()

