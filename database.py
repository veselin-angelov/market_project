import sqlite3

DB_NAME = 'market.db'

conn = sqlite3.connect(DB_NAME)

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS users 
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
        name TEXT NOT NULL,
        address TEXT NOT NULL,
        mobile INTEGER NOT NULL
    )
''')

conn.commit()

class DB:
    def __connect__(self):
        self.conn = sqlite3.connect(DB_NAME)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()