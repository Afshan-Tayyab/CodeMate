import sqlite3

DATABASE_NAME = "codemate.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS code_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            language TEXT NOT NULL,
            code TEXT NOT NULL,
            lines INTEGER NOT NULL,
            functions INTEGER NOT NULL,
            loops INTEGER NOT NULL,
            variables INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_analysis(language, code, lines, functions, loops, variables):
    connection = get_connection()

    connection.execute("""
        INSERT INTO code_history
        (language, code, lines, functions, loops, variables)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        language,
        code,
        lines,
        functions,
        loops,
        variables
    ))

    connection.commit()
    connection.close()


def get_history():
    connection = get_connection()

    rows = connection.execute("""
        SELECT *
        FROM code_history
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    return [dict(row) for row in rows]


def delete_history(history_id):
    connection = get_connection()

    connection.execute(
        "DELETE FROM code_history WHERE id = ?",
        (history_id,)
    )

    connection.commit()
    connection.close()