import re
import os
import hashlib
from flask import send_from_directory
from datetime import datetime
import smtplib
import my_db
from flask import json
from math import ceil

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
        if word:
            result.append(word)

    return delim.join(result)


def retrive(tables):
    myresult=""
    try:
        my_db.connection()
        sql=''
        if tables is 'page_tbl' or tables is 'category_tbl':
            sql = "select * from "+tables
            my_db.cur.execute(sql)
        else:
            status = ('yes',)
            sql = "select * from "+tables+" WHERE status = %s"
            my_db.cur.execute(sql,status)
            
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
        sql = "select * from  article_tbl where categary_id=%s" 
        val = (id,)
        my_db.cur.execute(sql,val)
        myresult = my_db.cur.fetchall()

    except Exception as err:
        print(err)
        my_db.conn.rollback()
    finally:
        my_db.conn.close()
    return json.dumps({"type": "fliter", "result":  myresult})

def update_query(table_name):
    result=""
    count=0
    try:
        my_db.connection()
        sql = "SELECT * FROM "+table_name+" ORDER BY order_step ASC"
        my_db.cur.execute(sql)
        result = my_db.cur.fetchall()
        for row in result:
            count= count+1
            sql = "UPDATE "+table_name+" SET order_step=%s WHERE id=%s"
            val=(str(count),row['id'],)
            my_db.cur.execute(sql, val)
            my_db.conn.commit()
    except Exception as err:
        print(err)
        my_db.conn.rollback()

    finally:
        my_db.conn.close()
    return True


class Pagination(object):

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num
