from cs50 import SQL

db = SQL("sqlite:///library.db")


class User:
    def __init__(self, username, first_name, last_name, email, password):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def print_info(self):
        print(f"""
            username = {self.username}
            first_name = {self.first_name}
            last_name = {self.last_name}
            email = {self.email}
            password = {self.password}
        """)


admin = User("username", "hamza", "serhani", "email@gmail.com", "hamzahamza")
admin.print_info()
