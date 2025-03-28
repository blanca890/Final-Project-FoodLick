import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.dialogs import Messagebox
from user.UserGUI import GUIUser
from user.UserFunctions import FunctionUser
from user.UserGUI import LoginScreen  
from admin.AdminGUI import GUIAdmin  

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
            from admin.AdminData import DataAdmin
            logic = DataAdmin()
            from admin.AdminGUI import GUIAdmin
            GUIAdmin(root, logic)
        elif role in ["user", "cashier"]:  # Treat cashiers as users
            from user.UserFunctions import FunctionUser
            logic = FunctionUser()
            from user.UserGUI import GUIUser
            GUIUser(root, logic, username)  # Pass the username
            
    LoginScreen(root, style, open_main_app)  # Pass the callback here
    root.mainloop()

if __name__ == "__main__":
    main()