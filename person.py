class Person:
    def __init__(self, name, surname) -> None:
        self.name = name
        self.surname = surname
        self.adress: str
        self.email: str
        self.users = []

    def create_user(self):
        "Make the person a user of the system"
        print("se ha creado un usuario")
        #user = User(user_name, email, password) #Class to be defined
        #self.users.append(user)


    