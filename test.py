from flask import Flask, render_template, request, flash, json, redirect, url_for, session, Blueprint
from flask_mail import Mail, Message
import os
from datetime import datetime

app = Flask(__name__)

'''UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def hello_world():
    return render_template('category-manager/add-category.html', sec='sec')


@app.route('/upload', methods=['POST'])
def upload_file():

    file = request.files['image']
    new_file = file.filename.split('.')
    file.filename = "image"+str(datetime.now())+"."+new_file[-1]
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(f)

    return render_template('index.html')




app.run(debug=True)





import my_db
import os

UPLOAD_FOLDER = os.path.expandvars('./uploads/article_image')
art = Flask(__name__)
art.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
var=art.config['UPLOAD_FOLDER']

try:
  my_db.connection()

  my_db.cur.execute("SELECT * FROM article_tbl")

  myresult = my_db.cur.fetchone()

  print(myresult['image'])
except:
  my_db.conn.rollback()

finally:
  my_db.conn.close()
if os.path.exists(art.config['UPLOAD_FOLDER']+"/"+myresult['image']):
  print('exists')
  #os.remove(art.config['UPLOAD_FOLDER']+"/index.jpeg")
else:
  print("The file does not exist")


import smtplib


def send_email(subject, msg):
  try:
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    print('shubham')
    server.login('projectcms.2019dotsquares@gmail.com','dots@123')
    print('shubham')
    message = 'subject : {} \n\n {}'.format(subject, msg)
    server.sendmail('projectcms.2019dotsquares@gmail.com', 'cms.2019dotsquares@gmail.com',message)

    server.quit()
  except ValueError as val:
    print(val)
    print("problem")


subject = "test"

msg = "hello friends "

send_email(subject, msg)'''


@app.route('/')
def index():
  return render_template('/page-manager/add-page.html', sec="rajat@gmail.com")


app.run( debug=True)
 

