from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
# Here i will use cs50 sql library
from cs50 import SQL
from functools import wraps

app = Flask(__name__)

# Database
db = SQL("sqlite:///database.db")

# Configure session
app.secret_key = "secret_key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

# Login-required decorator (inspired by CS50 Finance)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Context processor


@app.context_processor
def inject_user():
    try:
        total = db.execute(
            "SELECT COUNT(*) as total FROM students")[0]["total"]
        total_classes = db.execute(
            "SELECT COUNT(*) as total FROM classes")[0]["total"]
        avg_result = db.execute(
            "SELECT AVG((math + science + english + history) / 4.0) as avg FROM grades"
        )
        avg_grade = round(avg_result[0]["avg"] or 0, 1)
        return {
            "first_name": session.get("first_name", ""),
            "last_name": session.get("last_name", ""),
            "username": session.get("username", ""),
            "total_students": total,
            "total_classes": total_classes,
            "avg_grade": avg_grade,
        }
    except Exception:
        return {
            "first_name": "",
            "last_name": "",
            "username": "",
            "total_students": 0,
            "total_classes": 0,
            "avg_grade": 0,
        }


# Authentication
@app.route("/")
def index():
    if session.get("user_id"):
        return redirect("/dashboard")
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirmation", "")

        if not username:
            flash("Username is required.", "error")
            return render_template("register.html")
        if not password:
            flash("Password is required.", "error")
            return render_template("register.html")
        if password != confirm:
            flash("Passwords do not match.", "error")
            return render_template("register.html")

        existing = db.execute(
            "SELECT id FROM admins WHERE username = ?", username)
        if existing:
            flash("Username already taken.", "error")
            return render_template("register.html")

        hash_pw = generate_password_hash(password)
        db.execute(
            "INSERT INTO admins (username, first_name, last_name, email, phone, password) VALUES (?, ?, ?, ?, ?, ?)",
            username,
            first_name,
            last_name,
            email,
            phone,
            hash_pw,
        )
        flash("Account created! Please log in.", "success")
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect("/dashboard")

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        rows = db.execute("SELECT * FROM admins WHERE username = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], password):
            flash("Invalid username or password.", "error")
            return render_template("login.html")

        user = rows[0]
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["first_name"] = user["first_name"]
        session["last_name"] = user["last_name"]
        return redirect("/dashboard")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect("/login")


@app.route("/dashboard")
@login_required
def dashboard():
    recent_students = db.execute(
        "SELECT first_name, last_name, class, created_at FROM students ORDER BY id DESC LIMIT 5"
    )
    avgs = db.execute("""
        SELECT
            ROUND(AVG(math),1)    as math,
            ROUND(AVG(science),1) as science,
            ROUND(AVG(english),1) as english,
            ROUND(AVG(history),1) as history
        FROM grades
    """)
    grade_avgs = (
        [
            avgs[0]["math"] or 0,
            avgs[0]["science"] or 0,
            avgs[0]["english"] or 0,
            avgs[0]["history"] or 0,
        ]
        if avgs
        else [0, 0, 0, 0]
    )
    return render_template(
        "dashboard.html", recent_students=recent_students, grade_avgs=grade_avgs
    )


@app.route("/students")
@login_required
def students():
    class_filter = request.args.get("class", "all")
    search = request.args.get("q", "").strip()

    query = "SELECT * FROM students WHERE 1=1"
    params = []

    if class_filter != "all":
        query += " AND class = ?"
        params.append(class_filter)

    if search:
        query += " AND (first_name LIKE ? OR last_name LIKE ? OR email LIKE ?)"
        like = f"%{search}%"
        params.extend([like, like, like])

    query += " ORDER BY first_name"
    all_students = db.execute(query, *params)

    classes = db.execute("SELECT DISTINCT class FROM students ORDER BY class")
    return render_template(
        "students.html",
        students=all_students,
        classes=classes,
        class_filter=class_filter,
        search=search,
    )


@app.route("/students/add", methods=["GET", "POST"])
@login_required
def add_student():
    classes = db.execute("SELECT DISTINCT class FROM classes ORDER BY class")

    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        age = request.form.get("age", "")
        class_name = request.form.get("class", "")
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        status = request.form.get("status", "Active")

        if not first_name or not last_name:
            flash("First and last name are required.", "error")
            return render_template("student_form.html", student=None, classes=classes, action="Add")

       # add a students
        result = db.execute(
            "INSERT INTO students (first_name, last_name, age, class, email, phone, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
            first_name, last_name, age, class_name, email, phone, status,
        )

        # get new student id
        student_id = result

        # Create default grades for the new student (all subjects = 0)
        db.execute(
            "INSERT INTO grades (student_id, math, science, english, history) VALUES (?, ?, ?, ?, ?)",
            student_id, 0, 0, 0, 0
        )

        flash(
            f"{first_name} {last_name} added successfully with default grades!", "success")
        return redirect("/students")

    return render_template("student_form.html", student=None, classes=classes, action="Add")


@app.route("/students/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_student(id):
    student = db.execute("SELECT * FROM students WHERE id = ?", id)
    if not student:
        flash("Studewhy nt not found.", "error")
        return redirect("/students")
    student = student[0]
    classes = db.execute("SELECT DISTINCT class FROM classes ORDER BY class")

    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        age = request.form.get("age", "")
        class_name = request.form.get("class", "")
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        status = request.form.get("status", "Active")

        if not first_name or not last_name:
            flash("First and last name are required.", "error")
            return render_template(
                "student_form.html", student=student, classes=classes, action="Edit"
            )

        db.execute(
            "UPDATE students SET first_name=?, last_name=?, age=?, class=?, email=?, phone=?, status=? WHERE id=?",
            first_name,
            last_name,
            age,
            class_name,
            email,
            phone,
            status,
            id,
        )
        flash("Student updated successfully!", "success")
        return redirect("/students")

    return render_template(
        "student_form.html", student=student, classes=classes, action="Edit"
    )


@app.route("/students/<int:id>/delete", methods=["POST"])
@login_required
def delete_student(id):
    student = db.execute(
        "SELECT first_name, last_name FROM students WHERE id = ?", id)
    if student:
        # First delete related grades (foreign key constraint)
        db.execute("DELETE FROM grades WHERE student_id = ?", id)
        # Then delete the student
        db.execute("DELETE FROM students WHERE id = ?", id)
        flash(
            f"{student[0]['first_name']} {student[0]['last_name']} removed.", "success"
        )
    else:
        flash("Student not found.", "error")
    return redirect("/students")


# Classes

@app.route("/classes")
@login_required
def classes():
    all_classes = db.execute("""
        SELECT c.*, COUNT(s.id) as student_count
        FROM classes c
        LEFT JOIN students s ON s.class = c.class
        GROUP BY c.id
        ORDER BY c.class
    """)
    return render_template("classes.html", classes=all_classes)


@app.route("/classes/add", methods=["GET", "POST"])
@login_required
def add_class():
    if request.method == "POST":
        class_name = request.form.get("class", "").strip()
        subject = request.form.get("subject", "").strip()
        teacher = request.form.get("teacher", "").strip()

        if not class_name or not subject:
            flash("Class name and subject are required.", "error")
            return render_template("class_form.html", cls=None, action="Add")

        existing = db.execute(
            "SELECT id FROM classes WHERE class = ? AND subject = ?",
            class_name,
            subject,
        )
        if existing:
            flash("This class/subject combination already exists.", "error")
            return render_template("class_form.html", cls=None, action="Add")

        db.execute(
            "INSERT INTO classes (class, subject, teacher) VALUES (?, ?, ?)",
            class_name,
            subject,
            teacher,
        )
        flash("Class added successfully!", "success")
        return redirect("/classes")

    return render_template("class_form.html", cls=None, action="Add")


@app.route("/classes/<int:id>/delete", methods=["POST"])
@login_required
def delete_class(id):
    db.execute("DELETE FROM classes WHERE id = ?", id)
    flash("Class removed.", "success")
    return redirect("/classes")


@app.route("/grades")
@login_required
def grades():
    class_filter = request.args.get("class", "all")

    query = """
        SELECT s.id, s.first_name, s.last_name, s.class,
               g.math, g.science, g.english, g.history,
               ROUND((g.math + g.science + g.english + g.history) / 4.0, 1) as avg
        FROM students s
        LEFT JOIN grades g ON g.student_id = s.id
        WHERE g.id IS NOT NULL
    """
    params = []
    if class_filter != "all":
        query += " AND s.class = ?"
        params.append(class_filter)

    query += " ORDER BY s.first_name"
    grade_rows = db.execute(query, *params)

    classes = db.execute("SELECT DISTINCT class FROM students ORDER BY class")
    return render_template(
        "grades.html", grades=grade_rows, classes=classes, class_filter=class_filter
    )


@app.route("/grades/<int:student_id>/edit", methods=["GET", "POST"])
@login_required
def edit_grades(student_id):
    student = db.execute("SELECT * FROM students WHERE id = ?", student_id)
    if not student:
        flash("Student not found.", "error")
        return redirect("/grades")
    student = student[0]

    existing = db.execute(
        "SELECT * FROM grades WHERE student_id = ?", student_id)
    grade = existing[0] if existing else None

    if request.method == "POST":
        math = int(request.form.get("math", 0))
        science = int(request.form.get("science", 0))
        english = int(request.form.get("english", 0))
        history = int(request.form.get("history", 0))

        if grade:
            db.execute(
                "UPDATE grades SET math=?, science=?, english=?, history=? WHERE student_id=?",
                math,
                science,
                english,
                history,
                student_id,
            )
        else:
            db.execute(
                "INSERT INTO grades (student_id, math, science, english, history) VALUES (?, ?, ?, ?, ?)",
                student_id,
                math,
                science,
                english,
                history,
            )
        flash("Grades updated!", "success")
        return redirect("/grades")

    return render_template("grade_form.html", student=student, grade=grade)



if __name__ == "__main__":
    app.run(debug=True)