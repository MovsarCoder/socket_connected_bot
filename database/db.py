import sqlite3


def createTable():
    conn = sqlite3.connect('../database/database.db')
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS all_users(
    name TEXT,
    firstname TEXT,
    lastname TEXT,
    sign_up_people TEXT,
    telegram_id INTEGER,
    unique_id INTEGER
    )
    """)
    conn.commit()
    conn.close()


def insertIntoToTable(name: str,
                      firstname: str,
                      lastname: str,
                      sign_up_people: str,
                      telegram_id: int,
                      unique_id: int
                      ):
    conn = sqlite3.connect('../database/database.db')
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO all_users(name, firstname, lastname, sign_up_people, telegram_id, unique_id) VALUES (?, ?, ?, ?, ?, ?)
    """, (name, firstname, lastname, sign_up_people, telegram_id, unique_id))
    conn.commit()
    conn.close()


def user_exists(telegram_id: int) -> bool:
    conn = sqlite3.connect('../database/database.db')
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM all_users WHERE telegram_id = ?", (telegram_id,))
    count = cur.fetchone()[0]
    conn.close()
    return count > 0


def selectToTable(telegram_id: int):
    conn = sqlite3.connect('../database/database.db')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM all_users WHERE telegram_id = ?""", (telegram_id,))
    get_info = cur.fetchone()
    conn.close()
    return_info = {
        "name": get_info[0],
        "firstname": get_info[1],
        "lastname": get_info[2],
        "sign_up_people": get_info[3],
        "telegram_id": get_info[4],
        "unique_id": get_info[5],
    }
    return return_info