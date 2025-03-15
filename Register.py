from tkinter import *
from tkinter import messagebox

def register_window():
    reg_win = Toplevel()
    reg_win.geometry("400x300")
    reg_win.title("Register")

    Label(reg_win, text="Username:", font=("Arial", 12)).pack(pady=5)
    entry_username = Entry(reg_win, font=("Arial", 12))
    entry_username.pack(pady=5)

    Label(reg_win, text="Password:", font=("Arial", 12)).pack(pady=5)
    entry_password = Entry(reg_win, show="*", font=("Arial", 12))
    entry_password.pack(pady=5)

    def register_user():
        username = entry_username.get()
        password = entry_password.get()
        if username and password:
            messagebox.showinfo("Success", f"User {username} registered!")
            reg_win.destroy()
        else:
            messagebox.showerror("Error", "All fields are required!")

    Button(reg_win, text="Register", font=("Arial", 12), command=register_user).pack(pady=10)
