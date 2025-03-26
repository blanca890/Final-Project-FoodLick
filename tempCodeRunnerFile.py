import tkinter as tk
from ttkbootstrap import Style
from UserGUI import GUIUser, LoginScreen  # Import LoginScreen
from UserFunctions import FunctionUser

def main():
    root = tk.Tk()
    try:
        root.iconbitmap("img/Logo.ico")  # Ensure this file exists
    except Exception as e:
        print(f"Error loading icon: {e}")

    try:
        style = Style("litera")  # Ensure the theme is valid
    except Exception as e:
        print(f"Error loading theme: {e}")

    # Function to open the main app after successful login
    def open_main_app():
        root.withdraw()  # Hide the login window
        main_root = tk.Tk()
        try:
            main_root.iconbitmap("img/Logo.ico")  # Set the icon for the main app
        except Exception as e:
            print(f"Error loading icon for main app: {e}")
        
        # Reinitialize the ttkbootstrap Style object for the new main_root window
        main_style = Style("litera")
        main_style.master = main_root  # Associate the Style object with main_root

        app = GUIUser(main_root, FunctionUser(), main_style)  # Pass the Style object to GUIUser
        main_root.mainloop()
        root.destroy()  # Destroy the login window after the main app is closed

    # Show the login screen first
    login_screen = LoginScreen(root, open_main_app)
    root.mainloop()

if __name__ == "__main__":
    main()

