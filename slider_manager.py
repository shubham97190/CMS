from flask import render_template, request, json, redirect, flash, url_for, Blueprint, session, Flask
import os
from datetime import datetime
import my_db
import mysql.connector
from functions import uploaded, delete, file_upload

sld_manager = Blueprint('sld_manager', __name__)
UPLOAD_FOLDER = os.path.expandvars('./uploads/slider_image')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
sld = Flask(__name__)
sld.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@sld_manager.route('/admin/slider/list_slider')
def silder_list():
    if 'username' in session:
        myresult = ""
        try:
            my_db.connection()
            sql = "SELECT * FROM slider_tbl "
            my_db.cur.execute(sql)
            myresult = my_db.cur.fetchall()
        except:

            my_db.conn.rollback()
        finally:
            my_db.conn.close()
        
        return render_template('/slider-manager/list-slider.html', sec=session['username'], myresult=myresult)
    return render_template('homepages/login.htm')


@sld_manager.route('/admin/slider/add_slider', methods=['POST', 'GET'])
def add_slider():
    if 'username' in session:
        error = {}
        val = {}
        if request.method == 'POST':
            title = request.form['title']
            ck = request.form['ck']
            val['title'] = title
            fileupload = ''

            if title == "":
                error['h'] = "Title is empty"

            if request.files:
                fileupload = request.files['image']
            else:
                error['im']="Images is empty"

            if len(error) == 0:
                image = ""
               
                if fileupload:
                    image = file_upload(sld.config['UPLOAD_FOLDER'], fileupload)

                try:

                    my_db.connection()
                    sql = "insert into slider_tbl(title,image,status," \
                          "created_date,modified_date)" \
                          " value(%s,%s,%s,%s,%s)"
                    val = (title,  image, ck,  str(datetime.now()), str(datetime.now()),)
                    my_db.cur.execute(sql, val)
                    my_db.conn.commit()

                    flash('Slider has been added successfully!')
                    return redirect(url_for('sld_manager.silder_list'))

                except mysql.connector.Error as err:
                    print(err)
                    my_db.conn.rollback()
                finally:
                    my_db.conn.close()
        return render_template('/slider-manager/add-slider.html', error=error,
                               sec=session['username'], val=val)
    return render_template('homepages/login.htm')


@sld_manager.route('/slider_delete', methods=['POST', 'GET'])
def slider_delete():
    id = request.args.get('id')
    try:
        my_db.connection()
        sql = "SELECT * FROM slider_tbl WHERE  id =%s"
        val = (id,)
        my_db.cur.execute(sql, val)
        myresult = my_db.cur.fetchone()
        delete(sld.config['UPLOAD_FOLDER'], myresult['image'])
        sql = "delete from slider_tbl where id = %s"

        my_db.cur.execute(sql, val)
        my_db.conn.commit()
    except mysql.connector.Error as err:
        print(err)
        my_db.conn.rollback()

    finally:
        my_db.conn.close()
    return json.dumps({"type": "error"})


@sld_manager.route('/admin/slider/edit', methods=['POST', 'GET'])
def edit():
    if 'username' in session:

        id = request.args.get('id')
        myresult = ''
        old_image = ''
        try:
            my_db.connection()
            sql = "SELECT * FROM slider_tbl WHERE  id =%s"
            val = (id,)
            my_db.cur.execute(sql, val)

            myresult = my_db.cur.fetchone()
            if myresult is not None:
                old_image = myresult['image']
            my_db.conn.commit()

        except mysql.connector.Error as err:
            print(err)
            my_db.conn.rollback()

        finally:
            my_db.conn.close()

        error = {}
        if request.method == 'POST':
            
            title = request.form['title']
            ck = request.form['ck']
            flag = False

            fileuploads = ''

            if title == "":
                error['title'] = "Title is empty"

            if request.files:
                fileuploads = request.files['image']
                flag = True
            
            if len(error) == 0:
                image = ""
              
                if fileuploads and flag:
                    
                    image = file_upload(sld.config['UPLOAD_FOLDER'], fileuploads)
                try:
                    my_db.connection()
                   
                    if flag:
                        print("flag")
                        sql = "update slider_tbl set title=%s ,image=%s, status=%s, " \
                            "modified_date=%s where id=%s"
                        val = (title, image,  ck, str(datetime.now()), id,)
                        delete(sld.config['UPLOAD_FOLDER'],old_image)

                    else:
                       
                        sql = "update slider_tbl set title=%s , status=%s, " \
                            "modified_date=%s where id=%s"
                        val = (title,  ck, str(datetime.now()),  id,)

                    my_db.cur.execute(sql, val)
                    my_db.conn.commit()

                    flash('Slider has been updated successfully!')
                    return redirect(url_for('sld_manager.silder_list'))
                except mysql.connector.Error as err:
                    print(err)
                    my_db.conn.rollback()
                finally:
                    my_db.conn.close()
            print(len(myresult))
        return render_template('/slider-manager/edit-slider.html', error=error, sec=session['username'],
                               myresults=myresult)
    return render_template('homepages/login.htm')


@sld_manager.route('/uploads/slider_image/<filename>')
def get_slider_image_path(filename):
    return uploaded(sld.config['UPLOAD_FOLDER'], filename)


