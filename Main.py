# Group
# Team Members
# Gelton A. Blanca
# Winfred Emmanuel John Armamento
# Antonio Iii Guay
# Josh Gabriel Bautista
# Title: FoodLick




from tkinter import *
from tkinter import messagebox
import Register
import Login


sc = Tk()
sc.geometry("600x400+400+200")  
sc.title("FoodLick")  

compFont = ("Arial", 14)


def open_register():
    Register.register_window()

def open_login():
    Login.login_window()

def exit_app():
    sc.destroy()


lblHeader = Label(sc, text="Welcome to FoodLick", foreground="red", font=("Arial", 20))
lblHeader.pack(pady=20)


btnRegister = Button(sc, text="Register", font=compFont, command=open_register, width=20)
btnRegister.pack(pady=10)

btnLogin = Button(sc, text="Login", font=compFont, command=open_login, width=20)
btnLogin.pack(pady=10)

btnExit = Button(sc, text="Exit", font=compFont, command=exit_app, width=20)
btnExit.pack(pady=10)


sc.mainloop()
