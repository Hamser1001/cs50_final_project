from cs50 import SQL

db = SQL("sqlite:///database.db")


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

    def insert_data(self):
        db.execute(
            "INSERT INTO users (username, first_name, last_name, email, password) VALUES (?, ?, ?, ?, ?)",
            self.username,
            self.first_name,
            self.last_name,
            self.email,
            self.password,
        )

    def check_user(self):
        username = db.execute(
            "SELECT username FROM users WHERE username = ?", self.username
        )
        print(f"checking the user: {username}")
        if self.username == username:
            return True
        return False


admin = User("username", "hamza", "serhani", "email@gmail.com", "hamzahamza")
admin.print_info()
