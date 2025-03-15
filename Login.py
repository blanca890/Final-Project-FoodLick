from tkinter import *
from tkinter import messagebox

def login_window():
    login_win = Toplevel()
    login_win.geometry("400x300")
    login_win.title("Login")

    Label(login_win, text="Username:", font=("Arial", 12)).pack(pady=5)
    entry_username = Entry(login_win, font=("Arial", 12))
    entry_username.pack(pady=5)

    Label(login_win, text="Password:", font=("Arial", 12)).pack(pady=5)
    entry_password = Entry(login_win, show="*", font=("Arial", 12))
    entry_password.pack(pady=5)

    def login_user():
        username = entry_username.get()
        password = entry_password.get()
        if username == "admin" and password == "1234":  # Example check
            messagebox.showinfo("Success", "Login successful!")
            login_win.destroy()
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    Button(login_win, text="Login", font=("Arial", 12), command=login_user).pack(pady=10)
