# Group
# Team Members
# Gelton A. Blanca
# Winfred Emmanuel John Armamento
# Antonio Iii Guay
# Josh Gabriel Bautista
# Title: FoodLick




while True:
    print("Welcome to FoodLick")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        import Register
    elif choice == "2":
        import Login
    elif choice == "3":
        break
    else:
        print("Invalid choice")
        print("Please try again")
        print("")