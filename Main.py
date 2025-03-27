import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.dialogs import Messagebox
from UserGUI import GUIUser
from UserFunctions import FunctionUser
from UserGUI import LoginScreen  # Import the LoginScreen class
from AdminGUI import GUIAdmin  # Import the GuiAdmin class

def main():
    root = tk.Tk()
    style = Style("litera")  # Initialize the Style object once

    try:
        root.iconbitmap("img/Logo.ico")  # Ensure this file exists
    except Exception as e:
        print(f"Error loading icon: {e}")

    def open_main_app(username, role):
        # Destroy the login screen and open the appropriate GUI
        for widget in root.winfo_children():
            widget.destroy()
        if role == "admin":
            from AdminData import DataAdmin
            logic = DataAdmin()
            GUIAdmin(root, logic)
        elif role == "user":
            logic = FunctionUser()
            GUIUser(root, logic)

    # Show the login screen
    LoginScreen(root, style, open_main_app)
    root.mainloop()

if __name__ == "__main__":
    main()