from flask import Flask, render_template, session, request
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configure the session / use filesystem
app.config["SESSION_PERMANANT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        print(f"username: {username}, password: {password}")
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # if request.method == "POST":
    #     username = request.form.get("username")
    #     password = request.form.get("password")
    #     print(f"username: {username}, password: {password}")
    return render_template("register.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    return render_template("dashboard.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/layout", methods=["GET", "POST"])
def layout():
    return render_template("layout.html")
