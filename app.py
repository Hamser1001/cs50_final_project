from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from cs50 import SQL

app = Flask(__name__)
# Database
db = SQL("sqlite:///database.db")

# Configure the session / use filesystem
app.secret_key = "SECRET_KEY"
app.config["SESSION_PERMANANT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/registeration", methods=["GET", "POST"])
def registeration():
    if request.method == "POST":

        username = request.form.get("username")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        phone = request.form.get("number_phone")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check the inputs
        if not username:
            flash("Insert the username")
            return render_template("registeration.html")

        if not password:
            flash("Insert the password")
            return render_template("registeration.html")

        if password != confirmation:
            flash("Password does not match")
            return render_template("registeration.html")

        # Check existing username
        existing = db.execute("SELECT id FROM admins WHERE username = ?", username)
        if existing:
            # flash("The username already exists")
            return render_template("registeration.html")

        # Insert into database
        hash_password = generate_password_hash(password)

        db.execute(
            """INSERT INTO admins
               (username, first_name, last_name, email, phone, password)
               VALUES (?, ?, ?, ?, ?, ?)""",
            username,
            first_name,
            last_name,
            email,
            phone,
            hash_password,
        )

        flash("Registration successful!")
        return redirect("/login")

    return render_template("registeration.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user_info = db.execute("SELECT * FROM admins WHERE username = ?", username)

        # check the user exists:
        if len(user_info) != 1:
            error = "Invalid username or password"
            print(error)

        user = user_info[0]

        if not check_password_hash(user["password"], password):
            error = "Invalid username or password"
            print(error)

        session["username"] = user["username"]
        session["first_name"] = user["first_name"]
        session["last_name"] = user["last_name"]

        print(f"""
            session["username"] = {user["username"]}
            session["first_name"] = {user["first_name"]}
            session["last_name"] = {user["last_name"]}
        """)

        return redirect("/dashboard")
    return render_template("login.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    username = session["username"]
    first_name = session["first_name"]
    last_name = session["last_name"]
    return render_template(
        "dashboard.html", first_name=first_name, last_name=last_name, username=username
    )


@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        print("That's happend")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        age = request.form.get("age")
        class_name = request.form.get("class")
        email = request.form.get("email")
        number_phone = request.form.get("number_phone")
        status = request.form.get("status")

        print(f"""
            first_name: {first_name},
            last_name: {last_name},
            age: {age},
            class_name: {class_name},
            email: {email},
            number_phone: {number_phone},
            status: {status}
        """)

        db.execute(
            """
            INSERT INTO students (first_name, last_name, age, phone, email, class, status)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """,
            first_name,
            last_name,
            age,
            number_phone,
            email,
            class_name,
            status,
        )

    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/layout", methods=["GET", "POST"])
def layout():
    return render_template("layout.html")
