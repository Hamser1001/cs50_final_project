# -- I’ll use the SQLite library since I’ve learned a bit about it.
import sqlite3


def init_database():
    with open("schema.sql", "r") as file:
        schema = file.read()

    # connect database
    with sqlite3.connect("database.db") as conn:
        # Enable foreign key constraints
        conn.execute("PRAGMA foreign_keys = ON;")

        cursor = conn.cursor()

        # execute the schema
        cursor.executescript(schema)

        # Commit
        conn.commit()

        # Confirm whether foreign_keys is turned on.
        result = cursor.execute("PRAGMA foreign_keys;").fetchone()
        print(f"Foreign keys enabled: {bool(result[0])}")

        # Verify tables were created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables created:", [table[0] for table in tables])

        # get users
        cursor.execute("SELECT COUNT(*) FROM admins")
        admin_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM students")
        student_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM classes")
        class_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM grades")
        grade_count = cursor.fetchone()[0]

        print(
            f"Admins: {admin_count}, Students: {student_count}, Classes: {class_count}, Grades: {grade_count}"
        )

    print("Database initialized successfully!")


if __name__ == "__main__":
    init_database()
