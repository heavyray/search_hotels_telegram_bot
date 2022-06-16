import datetime
import sqlite3
from typing import List

from user import Hotel


def save_search(chat_id: int, command: str, city: str, hotels_list: List[Hotel]) -> None:
    """Функция сохраняет параметры поиска в БД"""
    sqlite_connection = sqlite3.connect('../db.sqlite3', check_same_thread=False)
    cursor = sqlite_connection.cursor()

    cursor.execute(f"""INSERT INTO history(chat_id, city, command, date) 
   VALUES('{chat_id}', '{city}', '{command}', '{datetime.datetime.now()}');""")

    search_id = cursor.lastrowid
    save_hotels(cursor, search_id, hotels_list)

    sqlite_connection.commit()
    cursor.close()


def save_hotels(cursor, search_id, hotels_list):
    """Функция сохраняет найденные отели в БД"""
    for hotel in hotels_list:
        cursor.execute(
            f"""
            INSERT INTO hotel(search_id, name, count_stars, address, price, city_center_distance, count_night, url)
            VALUES("{search_id}", "{hotel.name}", "{hotel.stars}", "{hotel.address}", "{hotel.price}",
            "{hotel.city_center_distance}", "{hotel.count_night}", "{hotel.url}");
            """
        )


def get_history(chat_id: int) -> list:
    """Функция возвращает последние запросы пользователя"""
    sqlite_connection = sqlite3.connect('../db.sqlite3', check_same_thread=False)
    cursor = sqlite_connection.cursor()
    sqlite_select_query = f"""SELECT * from history WHERE chat_id = {chat_id} ORDER BY date DESC LIMIT 5"""
    cursor.execute(sqlite_select_query)
    res = cursor.fetchall()
    sqlite_connection.commit()
    cursor.close()

    return res


def get_hotels(search_id: int) -> list:
    """Функция возвращает найденные отели по id поиска"""
    sqlite_connection = sqlite3.connect('../db.sqlite3', check_same_thread=False)
    cursor = sqlite_connection.cursor()
    sqlite_select_query = f"""SELECT * from hotel WHERE search_id = '{search_id}'"""
    cursor.execute(sqlite_select_query)
    res = cursor.fetchall()
    sqlite_connection.commit()
    cursor.close()

    return res
