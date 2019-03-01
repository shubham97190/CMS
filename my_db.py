import mysql.connector


def connection():
    global conn
    global cur
    try:
        conn = mysql.connector.connect(host="localhost", user="root", passwd="root", database="all_db")
        cur = conn.cursor(dictionary=True)

    except:

        conn.rollback()

