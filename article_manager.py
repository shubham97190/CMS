from flask import render_template, request, json, redirect, flash, url_for, Blueprint, session, Flask
import os
from math import ceil
from datetime import datetime
import my_db
from functions import uploaded, delete, file_upload

art_manager = Blueprint('art_manager', __name__)
UPLOAD_FOLDER = os.path.expandvars('./uploads/article_image')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'csv', 'docx', 'ppt'])
art = Flask(__name__)
art.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def category():
    myresult=''
    try:
        my_db.connection()
        sql = "SELECT * FROM category_tbl "
        my_db.cur.execute(sql)
        myresult = my_db.cur.fetchall()
    except:

        my_db.conn.rollback()
    finally:
        my_db.conn.close()
    return myresult


def update_query():
    result=""
    count=0
    try:
        my_db.connection()
        sql = "SELECT * FROM article_tbl ORDER BY order_step ASC"
        my_db.cur.execute(sql)
        result = my_db.cur.fetchall()
        for row in result:
            count= count+1
            sql = "UPDATE article_tbl SET order_step=%s WHERE id=%s"
            val=(str(count),row['id'],)
            my_db.cur.execute(sql, val)
            my_db.conn.commit()
    except Exception as err:
        print(err)
        my_db.conn.rollback()

    finally:
        my_db.conn.close()
    return True


@art_manager.route('/admin/article/list_article')
def article_list():
    if 'username' in session:
        myresult = ""
        total_page = 0
        page = 0
        try:
            if request.args.get('page'): 
                page = request.args.get('page')

            my_db.connection()

            sql = "SELECT count(id) FROM article_tbl "
            my_db.cur.execute(sql)
            total_row = my_db.cur.fetchall()

            no_of_row = total_row[0]['count(id)']
            page_size = 2
            total_page = ceil(no_of_row/page_size)
            
            starting_row = page_size*int(page)

            my_db.cur.execute("SELECT * FROM article_tbl ORDER BY order_step ASC LIMIT "+str(page_size)+" OFFSET "+str(starting_row)+"")

            myresult = my_db.cur.fetchall()
        except Exception as err:
            print(err)
            my_db.conn.rollback()
        finally:
            my_db.conn.close()
        return render_template('/article-manager/article_list.html', sec=session['username'], myresult=myresult,
                               total_page=total_page)
    return render_template('homepages/login.htm')


@art_manager.route('/admin/article/add_article', methods=['POST', 'GET'])
def add_article():
    if 'username' in session:
        myresult = category()
        error = {}
        val = {}
        if request.method == 'POST':
            title = request.form['title']
            ck = request.form['ck']
            decs = request.form['decs']
            cat_id = request.form['cat_id']

            val['title'] = title
            val['decs'] = decs

            fileupload = ''
            files = ""

            if title == "":
                error['h'] = "Title is empty"
            if decs == "":
                error['decs'] = "Description is empty"

            if 'image' in request.files:
                fileupload = request.files['image'] 
                
            else:
                error['img_error'] = "Image is empty"
                
            if 'f_load' in request.files:
                files = request.files['f_load']
            else:
                error['file_error'] = "File is empty"

            if len(error) == 0:
                image = ""
                file = ""
                if fileupload:
                    image = file_upload(art.config['UPLOAD_FOLDER'], fileupload)

                if files:
                    file = file_upload(art.config['UPLOAD_FOLDER'], files)

                try:

                    my_db.connection()
                    sql = "insert into article_tbl(title,description,image,status," \
                          "created_date,modified_date,file_upload, categary_id)" \
                          " value(%s,%s,%s,%s,%s,%s,%s,%s)"
                    val = (title, decs, image, ck, str(datetime.now()), str(datetime.now()),  file, cat_id)
                    my_db.cur.execute(sql, val)

                    my_db.conn.commit()
                    flash('Article has been added successfully!')
                    return redirect(url_for('art_manager.article_list'))

                except Exception as err:
                    print(err)
                    my_db.conn.rollback()
                finally:
                    my_db.conn.close()

        return render_template('/article-manager/add-article.html', error=error, myresults=myresult,
                               sec=session['username'], val=val)
    return render_template('homepages/login.htm')


@art_manager.route('/article_delete', methods=['POST', 'GET'])
def article_delete():
    id = request.args.get('id')
    try:

        my_db.connection()
        sql = "SELECT * FROM article_tbl WHERE  id =%s"
        val = (id,)
        my_db.cur.execute(sql, val)
        myresult = my_db.cur.fetchone()
        delete(art.config['UPLOAD_FOLDER'], myresult['image'])
        sql = "delete from article_tbl where id = %s"

        my_db.cur.execute(sql, val)
        my_db.conn.commit()
        update_query()
    except Exception as err:
        print(err)
        my_db.conn.rollback()

    finally:
        my_db.conn.close()
    return json.dumps({"type": "error"})


@art_manager.route('/admin/article/edit', methods=['POST', 'GET'])
def edit():
    if 'username' in session:

        id = request.args.get('id')
        myresult = ''
        old_image = ''
        old_file = ''
        try:
            my_db.connection()
            sql = "SELECT * FROM article_tbl WHERE  id =%s"
            val = (id,)
            my_db.cur.execute(sql, val)
            myresult = my_db.cur.fetchone()
            if myresult is not  None:
                old_image = myresult['image']
                old_file = myresult['file_upload']
                
            my_db.conn.commit()
        except Exception as err:
            print(err)
            my_db.conn.rollback()

        finally:
            my_db.conn.close()

        error = {}
        if request.method == 'POST':

            title = request.form['title']
            ck = request.form['ck']
            decs = request.form['decs']
            cat_id = request.form['cat_id']
            flag = False
            flag_file = False
            fileuploads = ''
            files_doc = ""

            if title == "":
                error['title'] = "Title is empty"

            if decs == "":
                error['decs'] = "Description is empty"
            if request.files:
                for d in request.files:
                   if d == 'image':
                       fileuploads = request.files['image']
                       flag = True
                   if d == 'f_load':
                       files_doc = request.files['f_load']
                       flag_file = True

            if len(error) == 0:
                image = ""
                file_name = ""
                if fileuploads and flag:
                    image = file_upload(art.config['UPLOAD_FOLDER'], fileuploads)

                if files_doc and flag:
                    file_name = file_upload(art.config['UPLOAD_FOLDER'], files_doc)

                try:
                    my_db.connection()
                    if flag and not flag_file:

                        sql = "update article_tbl set title=%s ,image=%s, description=%s, status=%s, " \
                            "modified_date=%s, categary_id=%s where id=%s"
                        val = (title, image, decs, ck, str(datetime.now()), cat_id, id,)
                        delete(art.config['UPLOAD_FOLDER'],old_image)

                    elif flag_file and not flag:

                        sql = "update article_tbl set title=%s , description=%s, status=%s, modified_date=%s ," \
                            " file_upload=%s,categary_id=%s where id=%s"
                        val = (title, decs, ck, str(datetime.now()),file_name , cat_id, id,)
                        delete(art.config['UPLOAD_FOLDER'],old_file)

                    elif flag and flag_file:

                        sql = "update article_tbl set title=%s , description=%s,image=%s, status=%s," \
                            " modified_date=%s, file_upload=%s,categary_id=%s where id=%s"
                        val = (title, decs, image, ck, str(datetime.now()),file_name, cat_id, id,)
                        delete(art.config['UPLOAD_FOLDER'], old_image)
                        delete(art.config['UPLOAD_FOLDER'], old_file)

                    else:
                        if 'pt' in request.form and request.form['pt'] == 'on':

                            delete(art.config['UPLOAD_FOLDER'], old_image)
                        if 'pt_file' in request.form and request.form['pt_file'] == 'on':
                            
                            delete(art.config['UPLOAD_FOLDER'], old_file)


                        sql = "update article_tbl set title=%s , description=%s, status=%s, " \
                            "modified_date=%s, categary_id=%s where id=%s"
                        val = (title, decs, ck, str(datetime.now()), cat_id, id,)

                    my_db.cur.execute(sql, val)
                    my_db.conn.commit()

                    flash('Article has been updated successfully!')
                    return redirect(url_for('art_manager.article_list'))
                except Exception as err:
                    print(err)
                    my_db.conn.rollback()
                finally:
                    my_db.conn.close()
        return render_template('/article-manager/edit-article.html', error=error, sec=session['username'], category=category(),
                               myresults=myresult)
    return render_template('homepages/login.htm')


@art_manager.route('/uploads/article_image/<filename>')
def get_article_image_path(filename):
    return uploaded(art.config['UPLOAD_FOLDER'], filename)


@art_manager.route('/article_order', methods=['POST', 'GET'])
def article_order():
    id = request.args.get('id')
    action = request.args.get('title')
    order = request.args.get('order')
    oder_step=""
    try:
        my_db.connection()
        if action == 'UP':
            oder_step = str(float(order) - 1.5)
            
        else:
            oder_step = str(float(order) + 1.5)

        sql = "UPDATE article_tbl SET order_step=%s WHERE id=%s"
        val=(oder_step,id)
        my_db.cur.execute(sql, val)
        my_db.conn.commit()
        update_query()
       
    except Exception as err:
        print(err)
        my_db.conn.rollback()
    finally:
        my_db.conn.close()
    return json.dumps({"type": "error"})
