import tkinter as tk
from ttkbootstrap import Style
from UserGUI import GUIUser
from UserFunctions import FunctionUser
from UserGUI import LoginScreen  # Import the LoginScreen class

def main():
    root = tk.Tk()
    style = Style("litera")  # Initialize the Style object once

    try:
        root.iconbitmap("img/Logo.ico")  # Ensure this file exists
    except Exception as e:
        print(f"Error loading icon: {e}")

    def open_main_app():
        # Destroy the login screen and open the main GUI
        for widget in root.winfo_children():
            widget.destroy()
        logic = FunctionUser()  # Pass the logic instance to GUIUser
        GUIUser(root, logic)

    # Show the login screen
    LoginScreen(root, style, open_main_app)
    root.mainloop()

if __name__ == "__main__":
    main()