import re
import os
import hashlib
from flask import send_from_directory
from datetime import datetime
import smtplib
import my_db
from flask import json

def lower_error(password):
    return re.search(r"[a-z]", password)


def upcase_error(password):
    return re.search(r"[A-Z]", password)


def digit_error(password):
    return re.search(r"\d", password)


def symbol_error(password):
    regex = re.compile('[@_!#$%^&*()<>?/}{~:]')
    return regex.search(password)


def hash_password(password):
    salt = "5gt"
    return hashlib.md5(salt.encode() + password.encode()).hexdigest()


def email_error(email):
    return re.match("^.+@([?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$)", email)


def uploaded(folder, filename):
    return send_from_directory(folder, filename)


def delete(folder, filename):
    if os.path.exists(folder + "/" + filename):
        os.remove(folder + "/" + filename)
        return True
    else:
        return "The file does not exist"


def file_upload(folder, file_up):
    new_file = file_up.filename.split('.')
    file_up.filename = "image" + str(datetime.now()) + "." + new_file[-1]
    f = os.path.join(folder, file_up.filename)
    file_up.save(f)
    return file_up.filename


def send_email(subject, msg, email_reciver):
  try:
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login('projectcms.2019dotsquares@gmail.com', 'dots@123')
    message = 'subject : {} \n\n {}'.format(subject, msg)
    server.sendmail('projectcms.2019dotsquares@gmail.com', email_reciver, message)
    server.quit()
  except Exception as err:
    print(err)


def get_conutry():
    myresult = ""
    try:
        my_db.connection()
        my_db.cur.execute("SELECT * FROM countries")
        myresult = my_db.cur.fetchall()
    except:
        my_db.conn.rollback()
    finally:
        my_db.conn.close()
    return myresult


def slug(text, delim=u'-'):
    _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
    result = []

    for word in _punct_re.split(text.lower()):
        # word = word.encode('translit/long')
        if word:
            result.append(word)

    return delim.join(result)


def retrive(tables):
    myresult=""
    try:
        my_db.connection()
        sql = "select * from "+tables  # +" where id=17"
        #  val = (tables,)
        my_db.cur.execute(sql)
        myresult = my_db.cur.fetchall()

    except Exception as err:
        print(err)
        my_db.conn.rollback()
    finally:
        my_db.conn.close()
    return myresult


def filter_article(id):
    myresult = ""
    try:
        my_db.connection()
        sql = "select * from  article_tbl where categary_id=%s" # +" where id=17"
        val = (id,)
        my_db.cur.execute(sql,val)
        myresult = my_db.cur.fetchall()

    except Exception as err:
        print(err)
        my_db.conn.rollback()
    finally:
        my_db.conn.close()
    return json.dumps({"type": "fliter", "result":  myresult})
