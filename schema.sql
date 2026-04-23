-- SchooHub Databse Schema
--
-- I used to add PRIMARY KEY (id) at the end of my query,
-- but I discovered a new syntax in the W3Schools SQL documentation:
-- id INTEGER PRIMARY KEY AUTOINCREMENT.
-- I’m currently in the final week of the CS50 SQL course.
-- I also learned how to use the Python sqlite3 library
-- from the documentation at https://docs.python.org/3/library/sqlite3.html
--
CREATE TABLE
    IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        phone TEXT,
        password TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

CREATE TABLE
    IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        age INTEGER,
        class TEXT,
        email TEXT,
        phone TEXT,
        status TEXT DEFAULT 'Active',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

CREATE TABLE
    IF NOT EXISTS classes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class TEXT NOT NULL,
        subject TEXT NOT NULL,
        teacher TEXT
    );

-- Update grades using DELETE CASCADE
CREATE TABLE
    IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        math INTEGER DEFAULT 0,
        science INTEGER DEFAULT 0,
        english INTEGER DEFAULT 0,
        history INTEGER DEFAULT 0,
        FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
    );
