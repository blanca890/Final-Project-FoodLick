import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.dialogs import Messagebox
from UserGUI import GUIUser
from UserFunctions import FunctionUser
from UserGUI import LoginScreen  
from AdminGUI import GUIAdmin  

def main():
    root = tk.Tk()
    style = Style("litera") 

    try:
        root.iconbitmap("img/Logo.ico")  
    except Exception as e:
        print(f"Error loading icon: {e}")

    def open_main_app(username, role):
        """Open the main application based on the role."""
        for widget in root.winfo_children():
            widget.destroy()
        if role == "admin":
            from AdminData import DataAdmin
            logic = DataAdmin()
            from AdminGUI import GUIAdmin
            GUIAdmin(root, logic)
        elif role in ["user", "cashier"]:  # Treat cashiers as users
            from UserFunctions import FunctionUser
            logic = FunctionUser()
            from UserGUI import GUIUser
            GUIUser(root, logic)
            
    LoginScreen(root, style, open_main_app)  # Pass the callback here
    root.mainloop()

if __name__ == "__main__":
    main()