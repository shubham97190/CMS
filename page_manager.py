from flask import render_template, request, json, redirect, flash, url_for, Blueprint, session
from datetime import datetime
import my_db
import mysql.connector
from functions import slug
from math import ceil

page = Blueprint('page', __name__)


@page.route('/admin/page/add-page', methods=['POST', 'GET'])
def add_page():
    if 'username' in session:
        error = {}
        val = {}
        if request.method == 'POST':
            title = request.form['title']
            decs = request.form['decs']
            slugs = request.form['slug']

            val['title'] = title
            val['decs'] = decs
            val['slug'] = slugs

            if title == "":
                error['h'] = "Title is empty"
            
            if decs == "":
                error['decs'] = "Description is empty"
            
            if slugs == "":

                error['slug'] = "Slug is empty"

            if len(error) == 0:
                slugfy = str(slug(slugs))
                try:

                    my_db.connection()
                    sql = "insert into page_tbl(title,slug,description,created_date,modified_date)" \
                          " values(%s,%s,%s,%s,%s)"
                    val = (title, slugfy, decs, str(datetime.now()), str(datetime.now()))

                    my_db.cur.execute(sql, val)
                    my_db.conn.commit()

                    flash('Page has been added successfully!')
                    return redirect(url_for('page.page_list'))
                except mysql.connector.Error as err:
                    print(err)
                    my_db.conn.rollback()
                finally:
                    my_db.conn.close()

        return render_template('/page-manager/add-page.html'
                               , error=error, val=val, sec=session['username'])
    return render_template('/homepages/login.htm')


@page.route('/admin/page/page-list', methods=['POST', 'GET'])
def page_list():
    if 'username' in session:
        total_page = 0
        myresult=""
        try:
            page = request.args.get('page')
            my_db.connection()

            sql = "SELECT count(id) FROM page_tbl "
            my_db.cur.execute(sql)
            total_row = my_db.cur.fetchall()

            no_of_row = total_row[0]['count(id)']
            page_size = 2
            total_page = ceil(no_of_row / page_size)
            starting_row = page_size * int(page)

            my_db.cur.execute("SELECT * FROM page_tbl LIMIT " + str(page_size) + " OFFSET " + str(starting_row))

            myresult = my_db.cur.fetchall()
        except mysql.connector.Error as err:
            print(err)
            my_db.conn.rollback()
        finally:
            my_db.conn.close()
        print(myresult)
        return render_template('/page-manager/page_list.html', sec=session['username'],  myresult=myresult,
                               total_page=total_page)
    return render_template('/homepages/login.htm')


@page.route('/admin/page/edit-page', methods=['POST', 'GET'])
def edit():
    if 'username' in session:
        print("entry")
        myresult = ''
        id = request.args.get('id')
        try:
            my_db.connection()
            sql = "SELECT * FROM page_tbl  WHERE  id =%s"
            val = (id, )
            my_db.cur.execute(sql,val)
            myresult = my_db.cur.fetchone()

        except mysql.connector.Error as err:
            print(err)
            my_db.conn.rollback()
        finally:
            my_db.conn.close()
        print("end select")

        error = {}
        if request.method == 'POST':
            print('entry post')
            title = request.form['title']
            decs = request.form['decs']
            slugs = request.form['slug']

            if title == "":
                error['h'] = "Title is empty"

            if decs == "":
                error['decs'] = "Description is empty"

            if slugs == "":
                error['slug'] = "Slug is empty"

            if len(error) == 0:
                print('entry without error')
                slugfy = str(slug(slugs))
                try:

                    my_db.connection()
                    print('try')
                    print(id)
                    sql = "update page_tbl set title=%s , slug=%s, description=%s,  " \
                          "modified_date=%s  WHERE  id =%s"
                    val = (title, slugfy, decs, str(datetime.now()), id)

                    my_db.cur.execute(sql, val)
                    my_db.conn.commit()

                    flash('Page has been Updated successfully!')
                    return redirect(url_for('page.page_list'))
                except mysql.connector.Error as err:
                    print(err)
                    my_db.conn.rollback()
                finally:
                    my_db.conn.close()

        return render_template('/page-manager/edit-page.html'
                                   , error=error, myresults=myresult, sec=session['username'])
    return render_template('/homepages/login.htm')


@page.route('/page-delete', methods=['POST', 'GET'])
def page_delete():
    id = request.args.get('id')
    try:

        my_db.connection()
        val = (id,)
        sql = "delete from page_tbl where id = %s"
        my_db.cur.execute(sql, val)
        my_db.conn.commit()
    except mysql.connector.Error as err:
        print(err)
        my_db.conn.rollback()

    finally:
        my_db.conn.close()
    return json.dumps({"type": "error"})


