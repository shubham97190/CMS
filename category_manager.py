from flask import render_template, request, flash,  redirect, url_for, Blueprint, json, session, Flask
import os
from datetime import datetime
import my_db
import mysql.connector
from functions import uploaded, delete, file_upload
from math import ceil

cat = Flask(__name__)
cat_manager = Blueprint('cat_manager', __name__)
UPLOAD_FOLDER = os.path.expandvars('./uploads/category_image')
cat.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'csv', 'docx', 'ppt'])


@cat_manager.route('/admin/category/category_list')
def category_list():
    if 'username' in session:
        myresult = ''
        total_page = 0
        # temp=1.5
        try:
            page = request.args.get('page')
            my_db.connection()

            sql = "SELECT count(id) FROM category_tbl "
            my_db.cur.execute(sql)
            total_row = my_db.cur.fetchall()
            no_of_row = total_row[0]['count(id)']
            page_size = 2
            

            total_page = ceil(no_of_row / page_size)
            starting_row = page_size * int(page)
            my_db.cur.execute("SELECT * FROM category_tbl LIMIT " + str(page_size) + " OFFSET " + str(starting_row))

            myresult = my_db.cur.fetchall()

        except mysql.connector.Error as err:
            print(err)
            my_db.conn.rollback()
        finally:
            my_db.conn.close()
        return render_template('/category-manager/category-list.html', sec=session['username'],
                               myresult=myresult,total_page=total_page)
    return render_template('homepages/login.htm')


@cat_manager.route('/admin/category/add_category', methods=['POST', 'GET'])
def add_category():
    if 'username' in session:
        error = {}
        val={}
        if request.method == 'POST':

            title = request.form['title']
            val['title'] = title
            file_uploads = ''
            if title == "":
                error['h'] = "title is empty"

            if request.files:
                file_uploads = request.files['image']

            else:
                error['file_error'] = "Image is empty"
            if len(error) == 0:
                name = ""
                if file_uploads:
                    name = file_upload(cat.config['UPLOAD_FOLDER'], file_uploads)
                    print(name)
                try:
                    my_db.connection()
                    sql = "insert into category_tbl(title,image,created_date,modified_date) value(%s,%s,%s,%s)"
                    val = (title, name, str(datetime.now()),str(datetime.now()),)
                    my_db.cur.execute(sql, val)
                    my_db.conn.commit()

                    flash('Category has been added successfully!')
                    return redirect(url_for('cat_manager.category_list'))
                except Exception as err:
                    print(err)
                    my_db.conn.rollback()
                finally:
                    my_db.conn.close()

        return render_template('category-manager/add-category.html', sec=session['username'], error=error, val=val)
    return render_template('homepages/login.htm')


@cat_manager.route('/admin/category/edit', methods=['POST', 'GET'])
def edit():
    if 'username' in session:
        id = request.args.get('id')
        myresult = ""
        old_image=""
        try:
            my_db.connection()
            sql = "SELECT * FROM category_tbl  WHERE  id =%s"
            val = (id,)
            my_db.cur.execute(sql, val)
            myresult = my_db.cur.fetchone()
            if myresult is not  None:
                old_image = myresult['image']
            
        except ValueError as err:
            print(err)
            my_db.conn.rollback()
        finally:
            my_db.conn.close()

        error = {}
        if request.method == 'POST':
            error = {}
            flag=False

            title = request.form['title']

            file_uploads = ''
            if title == "":
                error['h'] = "title is empty"

            if request.files:
                file_uploads = request.files['image']
                flag = True

            if len(error) == 0:
                name = ""
                if file_uploads:
                    name = file_upload(cat.config['UPLOAD_FOLDER'], file_uploads)
                try:
                    my_db.connection()
                    if flag:

                        sql = "update category_tbl set title=%s,image=%s,modified_date=%s WHERE  id =%s"
                        val = (title, name, str(datetime.now()), id, )
                        delete(cat.config['UPLOAD_FOLDER'], old_image)
                    else:

                        if 'pt' in request.form and request.form['pt'] == 'on':
                            delete(cat.config['UPLOAD_FOLDER'], old_image)

                        sql = "update category_tbl set title=%s,image=%s,modified_date=%s WHERE  id =%s"
                        val = (title, name, str(datetime.now()), id,)
                        if request.form['pt']:

                            delete(cat.config['UPLOAD_FOLDER'], old_image)

                        else:
                            sql = "update category_tbl set title=%s,modified_date=%s WHERE  id =%s"
                            val = (title, str(datetime.now()), id, )

                    my_db.cur.execute(sql, val)
                    my_db.conn.commit()

                    flash('Category has been added successfully!')
                    return redirect(url_for('cat_manager.category_list'))
                except Exception as err:
                    print(err)
                    my_db.conn.rollback()
                finally:
                    my_db.conn.close()
        return render_template('category-manager/edit-category.html', sec=session['username'], error=error,  myresults=myresult)
    return render_template('homepages/login.htm')


@cat_manager.route('/category_delete', methods=['POST', 'GET'])
def category_delete():
    id = request.args.get('id')
    try:

        my_db.connection()
        sql = "SELECT * FROM category_tbl WHERE  id =%s"
        val = (id,)
        my_db.cur.execute(sql, val)
        myresult = my_db.cur.fetchone()
        delete(cat.config['UPLOAD_FOLDER'], myresult['image'])
        sql = "delete from category_tbl where id = %s"

        my_db.cur.execute(sql, val)
        my_db.conn.commit()
    except mysql.connector.Error as err:
        print((err))
        my_db.conn.rollback()

    finally:
        my_db.conn.close()
    return json.dumps({"type": "error"})


@cat_manager.route('/uploads/category_image/<filename>')
def get_category_image_path(filename):

    return uploaded(cat.config['UPLOAD_FOLDER'], filename)


