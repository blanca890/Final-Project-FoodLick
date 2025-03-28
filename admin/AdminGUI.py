import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk
from ttkbootstrap import Style
import os
from admin.AdminFunction import FunctionsAdmin
from user.UserGUI import GUIUser

class AdminLogin:
    def __init__(self, root, logic, on_success):
        """
        Initialize the AdminLogin popup.
        :param root: The root Tkinter window.
        :param logic: The logic instance for admin validation.
        :param on_success: Callback function to execute on successful login.
        """
        self.root = root
        self.logic = logic
        self.on_success = on_success
        self.create_login_popup()

    def center_popup(self, popup, width, height):
        """Center a popup window on the screen."""
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")

    def create_login_popup(self):
        """Create the admin login popup."""
        popup = tk.Toplevel(self.root)
        popup.title("Admin Login")
        self.center_popup(popup, 300, 200)  # Center the popup
        popup.grab_set()

        ttk.Label(popup, text="Admin Username:", font=("Montserrat", 12)).pack(pady=10)
        username_entry = ttk.Entry(popup, font=("Montserrat", 12))
        username_entry.pack(pady=5)

        ttk.Label(popup, text="Admin Password:", font=("Montserrat", 12)).pack(pady=10)
        password_entry = ttk.Entry(popup, font=("Montserrat", 12), show="*")
        password_entry.pack(pady=5)

        def confirm_login():
            """Handle admin or cashier login."""
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            role = self.logic.validate_admin(username, password)
            if role == "admin":
                Messagebox.show_info("Login Successful", "Welcome, Admin!")
                popup.after(500, lambda: (popup.destroy(), self.on_success()))
            elif role == "cashier":
                Messagebox.show_info("Login Successful", "Welcome, Cashier!")
                popup.after(500, lambda: (popup.destroy(), self.open_cashier_interface(username)))
            else:
                Messagebox.show_error("Login Failed", "Invalid username or password.")

        def open_cashier_interface(username):
            """Open the cashier interface."""
            for widget in self.root.winfo_children():
                widget.destroy()
            from user.UserFunctions import FunctionUser
            logic = FunctionUser()
            GUIUser(self.root, logic, username)  # Pass the username

        ttk.Button(popup, text="Login", command=confirm_login, bootstyle="success").pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(popup, text="Cancel", command=popup.destroy, bootstyle="danger").pack(side=tk.RIGHT, padx=10, pady=10)


class GUIAdmin:
    def __init__(self, root, logic):
        self.root = root
        self.logic = logic
        self.style = Style("litera")
        self.root.title("Admin Panel")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="white")

        self.functions_admin = FunctionsAdmin(self.root)

        self.init_admin_interface()

    def init_admin_interface(self):
        """Initialize the admin interface."""
        self.create_widgets()

    def create_widgets(self):
        """Create the admin panel widgets."""

        title_label = ttk.Label(self.root, text="Admin Panel", font=("Montserrat", 24), background="white", anchor="center", bootstyle="primary")
        title_label.pack(pady=20)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=50)

        manage_items_button = ttk.Button(button_frame, text="Manage Items", command=self.functions_admin.manage_items, bootstyle="primary")
        manage_items_button.grid(row=0, column=0, padx=20, pady=10)

        manage_users_button = ttk.Button(button_frame, text="Manage Users", command=self.functions_admin.manage_users, bootstyle="primary")
        manage_users_button.grid(row=0, column=1, padx=20, pady=10)

        view_reports_button = ttk.Button(button_frame, text="View Reports", command=self.functions_admin.view_reports, bootstyle="primary")
        view_reports_button.grid(row=0, column=2, padx=20, pady=10)

        logout_button = ttk.Button(button_frame, text="Logout", command=self.logout, bootstyle="primary")
        logout_button.grid(row=0, column=3, padx=20, pady=10)

    def logout(self):
        """Logout and return to the login page."""
        for widget in self.root.winfo_children():
            widget.destroy()
        from user.UserGUI import LoginScreen
        LoginScreen(self.root, self.style, self.open_main_app)  # Pass the correct callback

    def open_main_app(self, username, role):
        """Open the main application based on the role."""
        for widget in self.root.winfo_children():
            widget.destroy()
        if role == "admin":
            from admin.AdminData import DataAdmin
            logic = DataAdmin()
            GUIAdmin(self.root, logic)
        elif role in ["user", "cashier"]:  # Treat cashiers as users
            from user.UserFunctions import FunctionUser
            logic = FunctionUser()
            from user.UserGUI import GUIUser
            GUIUser(self.root, logic, username)  # Pass the username


# Temporary code to run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    style = Style("litera")
    root.iconbitmap("img/Logo.ico")
    root.title("Admin Panel")
    root.geometry("800x600")
    root.resizable(False, False)
    root.configure(bg="white")

    # Directly open the Admin Panel without login
    class DummyLogic:
        """A dummy logic class to bypass admin validation."""
        def validate_admin(self, username, password):
            return "admin"  # Always return "admin" for testing purposes

    admin_logic = DummyLogic()
    GUIAdmin(root, admin_logic)

    root.mainloop()