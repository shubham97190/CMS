import mysql.connector


def connection():
    global conn
    global cur
    try:
        conn = mysql.connector.connect(host="localhost", user="root", passwd="", database="all_db")
        cur = conn.cursor(dictionary=True)

    except Exception as err:
        print(err)
        conn.rollback()

#connection()