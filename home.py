import my_db
def home_list():
    myresult = ""
    try:
        my_db.connection()
        sql = "SELECT id,image,categary_id FROM article_tbl WHERE status='yes'"
        my_db.cur.execute(sql)
        myresult = my_db.cur.fetchall()
    except:

        my_db.conn.rollback()
    finally:
        my_db.conn.close()
    return myresult

print(home_list())

#description