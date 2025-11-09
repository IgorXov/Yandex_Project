import sqlite3


def get_connection():
    conn = sqlite3.connect('task.db')
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS tasks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    description TEXT,
    date        TEXT,
    priority    TEXT    NOT NULL
                        DEFAULT NORMAL,
        completed   BOOLEAN NOT NULL DEFAULT 0);''')
    conn.commit()

    cur.execute('''CREATE TABLE IF NOT EXISTS subtasks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    description TEXT,
    priority    TEXT    NOT NULL
                        DEFAULT NORMAL,
    completed   BOOLEAN NOT NULL DEFAULT 0,
    id_task     INTEGER NOT NULL
                        REFERENCES tasks (id));''')

    conn.commit()
    conn.close()


