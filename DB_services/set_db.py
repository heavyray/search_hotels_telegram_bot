import sqlite3


def create_db():
    conn = sqlite3.connect('../db.db', check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS history (
    id      INTEGER  PRIMARY KEY UNIQUE,
    chat_id INTEGER,
    command VARCHAR,
    city    VARCHAR,
    date    DATETIME);
    """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS hotel (
        search_id                    REFERENCES history (id),
        name                 VARCHAR,
        count_stars          REAL,
        address              TEXT,
        price                REAL,
        city_center_distance REAL,
        count_night          REAL,
        url                  TEXT);
    """)

    conn.commit()
    cursor.close()


if __name__ == '__main__':
    create_db()
