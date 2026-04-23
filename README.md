# Personal Information

#### Name: Hamza Serhani
#### GitHub Username: Hamser1001

---

## What SchoolHub Does

At its core, SchoolHub allows an authenticated administrator to perform four main tasks: manage student records, manage classes, track grades, and view a live dashboard summarizing the school's data.

When a user first visits the application, they are redirected to the login page. If they do not yet have an account, they can register by providing a username, first name, last name, email, phone number, and password. Passwords are never stored in plain text — SchoolHub uses Werkzeug's `generate_password_hash` and `check_password_hash` functions to hash and verify passwords securely. Once logged in, the user's identity is stored in a server-side session managed by Flask-Session, so sensitive data is never exposed in the browser's cookies.

The dashboard is the first thing a logged-in user sees. It displays three key statistics at the top — total number of students, total number of classes, and the school-wide average grade across all subjects. Below that, it shows a table of the five most recently added students so the admin can quickly see recent activity. It also includes a bar chart (powered by Chart.js) that visualizes the average grade per subject: Math, Science, English, and History. This gives the administrator an instant visual snapshot of which subjects students are performing well in and which might need attention.

The Students section allows the admin to view all students in a searchable and filterable table. The admin can filter by class or search by name or email. From this page, they can add new students, edit existing ones, or delete them. When a new student is added, the system automatically creates a corresponding grade record for them with default values of zero, so no student is ever missing from the grades view. Deleting a student also automatically removes their grade record to maintain database integrity and avoid orphaned rows.

The Classes section lets the admin create and manage classes. Each class has a name, a subject, and a teacher's name. The system prevents duplicate class/subject combinations from being added. The classes list also shows how many students are currently enrolled in each class, using a SQL JOIN between the `classes` and `students` tables.

The Grades section displays every student's scores across the four subjects, along with their calculated average. The admin can filter the view by class. Editing a student's grades is done through a dedicated form. The system handles both the case where a grade record already exists (UPDATE) and where one does not yet exist (INSERT), making it robust to edge cases.

## File Structure and Description

**`app.py`** — This is the heart of the application. It contains all Flask routes and application logic. It is organized into four logical sections: authentication (register, login, logout), the dashboard, student management (list, add, edit, delete), class management (list, add, delete), and grade management (list, edit). It also includes a `login_required` decorator — inspired by CS50's Finance problem set — that protects all routes from unauthenticated access, and a context processor that injects global statistics (total students, total classes, average grade) into every template automatically, so the sidebar and header always show live data without needing to pass variables from every single route.

**`schema.sql`** — Contains the SQL statements used to define the database structure. There are four tables: `admins` (stores registered administrators), `students` (stores student records including name, age, class, email, phone, and status), `classes` (stores class name, subject, and teacher), and `grades` (stores per-subject scores linked to a student via a foreign key on `student_id`).

**`init_db.py`** — A small utility script used to initialize the database by executing the `schema.sql` file. This is run once at the start to create all tables, making it easy to reset or set up the database in a fresh environment.

**`database.db`** — The SQLite database file generated after running `init_db.py`. It stores all persistent data for the application.

**`requirements.txt`** — Lists all Python packages required to run the project, including Flask, Flask-Session, cs50, and Werkzeug.

**`templates/layout.html`** — The base layout that all other templates extend. It defines the overall page structure including the navigation sidebar, the top header bar (which shows the logged-in user's name and the global stats), and the main content area. Using Jinja2's `{% block %}` system, all other pages slot their content into this layout without repeating the HTML structure.

**`templates/base.html`** — A minimal base template used for the login and register pages, which have a different, simpler layout (no sidebar) compared to the authenticated pages.

**`templates/login.html`** and **`templates/register.html`** — The authentication pages. They display forms for logging in and registering, and show flash messages for errors or success feedback.

**`templates/dashboard.html`** — Displays the summary statistics, the recent students table, and the Chart.js bar chart. The chart data (subject averages) is passed from the route as a JSON-serializable list and injected into the JavaScript.

**`templates/students.html`** — Lists all students in a table with search and class filter controls. Includes edit and delete buttons per row.

**`templates/student_form.html`** — A shared form used for both adding and editing students. The `action` variable passed from the route determines whether the form is in "Add" or "Edit" mode, avoiding the need for two separate template files.

**`templates/classes.html`** — Lists all classes with their subject, teacher, and student count.

**`templates/class_form.html`** — Form for adding a new class.

**`templates/grades.html`** — Lists all students with their subject scores and calculated average, with a class filter.

**`templates/grade_form.html`** — Form for editing a specific student's grades across all four subjects.

## Design Decisions

One decision I thought carefully about was whether to use a single `student_form.html` template for both adding and editing students, rather than creating two separate files. I decided to reuse the same template and pass an `action` variable ("Add" or "Edit") from the route. This keeps the codebase DRY (Don't Repeat Yourself) and means any future changes to the student form only need to be made in one place.

Another decision involved grade initialization. When a student is added, I automatically insert a grade row with zeroes for all subjects. An alternative would have been to only create a grade row when the admin explicitly enters grades. I chose automatic initialization because it ensures every student always appears in the grades view, which makes the interface more predictable and prevents the admin from wondering why a student is missing from the grades table.

I also chose SQLite over a more powerful database like PostgreSQL. For a project of this scope — a single-admin system managing a few hundred students at most — SQLite is perfectly sufficient, requires no separate server process, and keeps deployment simple.

## Use of AI Tools

During the development of this project, I used ChatGPT as a supportive learning tool in several areas: understanding certain Flask concepts, learning how to integrate Chart.js into a Jinja2 template, improving code comments, and assisting with parts of this README. The core design, logic, and implementation decisions were my own. All AI assistance is cited in the relevant code comments as required by CS50's academic honesty policy.
