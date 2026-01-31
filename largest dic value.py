def login():
    username = "admin"
    password = "12345"
    for _ in range(3):
        input_username = input("Enter username: ")
        input_password = input("Enter password: ")
        if input_username == username and input_password == password:
            print("Login successful")
            return
        else:
            print("Incorrect username or password. Please try again.")
    print("Login failed")

login()
