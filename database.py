import sqlite3

def get_tariffs_family():
    connection = sqlite3.connect("taryfy.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM 'Smart Family'")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    return rows

def get_tariffs_unlimited():
    connection = sqlite3.connect("taryfy.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM 'unlimited'")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    return rows

def get_tariff_gb(text):
    connection = sqlite3.connect("taryfy.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM 'internet' WHERE internet = '{text}'")
    row = cursor.fetchone()
    cursor.close()
    connection.close()

    return row

def get_tariff_call():
    connection = sqlite3.connect("taryfy.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM 'internet' WHERE id = '3'")
    row = cursor.fetchone()
    cursor.close()
    connection.close()

    return row

def get_tariff_any():
    connection = sqlite3.connect("taryfy.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM 'internet' WHERE id = '7'")
    row = cursor.fetchone()
    cursor.close()
    connection.close()

    return row