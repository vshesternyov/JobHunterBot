import datetime
import sqlite3

conn = sqlite3.connect('vacancies.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS jobs
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT,
                   company TEXT,
                   link TEXT,
                   created_date DATE)''')

conn.commit()
conn.close()


def insert_record(title, company, link) -> bool:
    conn = sqlite3.connect('vacancies.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM jobs
                      WHERE title = ? AND company = ? AND link = ?''',
                   (title, company, link))
    existing_record = cursor.fetchone()

    if existing_record is None:
        current_date = datetime.date.today().strftime("%Y-%m-%d")
        cursor.execute('''INSERT INTO jobs (title, company, link, created_date)
                          VALUES (?, ?, ?, ?)''',
                       (title, company, link, current_date))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False

    conn.close()


def refresh_db():
    conn = sqlite3.connect('vacancies.db')
    cursor = conn.cursor()

    two_weeks_ago = (datetime.datetime.now() - datetime.timedelta(weeks=4)).strftime('%Y-%m-%d')
    cursor.execute('''DELETE FROM jobs WHERE created_date < ?''', (two_weeks_ago,))

    conn.commit()
    conn.close()
