import my_db
from functions import *
from flask import session, render_template, request, redirect, url_for, Blueprint, json, flash, make_response
import mysql.connector

auth = Blueprint('auth', __name__)


@auth.route('/admin/user/add_user', methods=['GET', 'POST'])
def add_user():
    if 'username' in session:
        error = {}
        val={}
        if request.method == 'POST':
            f_name = request.form['fname']
            l_name = request.form['lname']
            u_name = request.form['uname']
            email = request.form['email']
            passwd = request.form['psw']
            c_passwd = request.form['c_psw']
            contact = request.form['p_no']
            country = request.form['country']
            state = request.form['state']
            city = request.form['city']
            pin = request.form['pin']
            address = request.form['address']

            val['f_name'] = f_name
            val['l_name'] = l_name
            val['u_name'] = u_name
            val['email'] = email
            val['passwd'] = passwd
            val['c_passwd'] = c_passwd
            val['contact'] = contact
            val['country'] = country
            val['state'] = state
            val['city'] = city
            val['pin'] = pin
            val['address'] = address

            if f_name == "":
                error['f_name'] = "First name is Required"

            if l_name == "":
                error['l_name'] = "Last name is Required"

            if u_name == "":
                error['u_name'] = "User name is Required"

            if email == "":
                error['email'] = "E-mail is required"
            else:
                if email_error(email) is None:
                    error['email'] = "Enter a valid email"

            if len(passwd) < 6:
                error['psw'] = "Password must be at least 6 characters"
            else:
                if lower_error(passwd) is None:
                    error['psw_l'] = "Password must be at least one lower character"

                if upcase_error(passwd) is None:
                    error['psw_u'] = "Password must be at least one Upper character"

                if digit_error(passwd) is None:
                    error['psw_d'] = "Password must be at least one Numaaric digits"

                if symbol_error(passwd) is None:
                    error['psw_s'] = "Password must be at least one Special Character"

            if passwd != c_passwd:
                error['c_psw'] = "Password and Confirm Password does not Match"

            if contact.isdecimal() is False or contact == "":
                error['p_no'] = "Numeric value Required! in Contact"
            else:
                if len(contact) != 10:
                    error['p_no'] = "Enter 10 digits only in contact"
            if country == '0':
                error['country'] = "please select a country"

            if state == '0':
                error['state'] = "please select a state"

            if city == '0':
                error['city'] = "please select a city"

            if pin == '':
                error['pin'] = "please select a pin code"

            if address == "":
                error['address'] = "Address is Required!"

            if len(error) == 0:

                hash_passwd = hash_password(passwd)

                try:
                    send_email('cms_login', 'http://127.0.0.1:5000/login \n user name:'+u_name+'\n Password :'+passwd,
                               email)
                    my_db.connection()

                    sql = "insert into reg_tbl(first_name,last_name,user_name,e_mail," \
                        "password,contact,country,state,city,pin,address )" \
                        " values (%s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s)"

                    val = (f_name, l_name, u_name, email, hash_passwd, contact, country, state, city, pin, address)
                    my_db.cur.execute(sql, val)
                    my_db.conn.commit()

                    flash('User has been added successfully!')
                    return redirect(url_for('auth.list_user'))
                except:

                    my_db.conn.rollback()
                finally:
                    my_db.conn.close()

        return render_template('/user-management/add-user.html', error=error, myresult=get_conutry(), sec=session['username'], val=val)
    return render_template('homepages/login.htm')


@auth.route('/get_city', methods=['POST', 'GET'])
def get_city():

    myresult = "na"
    state = request.args.get('state')
    val=(state , )
    try:
        my_db.connection()
        sql = "SELECT * FROM cities where state_id=%s"
        my_db.cur.execute(sql, val)

        myresult = my_db.cur.fetchall()
    except:
        my_db.conn.rollback()
    finally:
        my_db.conn.close()

    return json.dumps({"type": "get_city", "result":  myresult})


@auth.route('/check_email', methods=['POST', 'GET'])
def check_email():

    myresult = "na"
    email = request.args.get('email')
    val = (email,)
    try:
        my_db.connection()
        sql = "SELECT * FROM reg_tbl where e_mail=%s"
        my_db.cur.execute(sql, val)

        myresult = my_db.cur.fetchone()
    except:
        my_db.conn.rollback()
    finally:
        my_db.conn.close()

    return json.dumps({"type": "check_email", "result": myresult})


@auth.route('/get_state', methods=['POST', 'GET'])
def get_state():

    myresult = "na"
    country = request.args.get('country')
    val = (country, )
    try:
        my_db.connection()

        sql = "SELECT * FROM states where country_id=%s"
        my_db.cur.execute(sql, val)

        myresult = my_db.cur.fetchall()
    except:
        my_db.conn.rollback()
    finally:
        my_db.conn.close()
    return json.dumps({"type": "get_state", "result":  myresult})


@auth.route('/check_user', methods=['POST', 'GET'])
def check_user():

    myresult = "na"
    uname = request.args.get('uname')
    val = (uname,)
    try:
        my_db.connection()
        sql = "SELECT * FROM reg_tbl where user_name=%s"
        my_db.cur.execute(sql, val)

        myresult = my_db.cur.fetchone()
    except:
        my_db.conn.rollback()
    finally:
        my_db.conn.close()

    return json.dumps({"type": "check_user", "result": myresult})


@auth.route('/admin/user/list_user')
def list_user():
    if 'username' in session:
        myresult = "na"
        try:
            my_db.connection()
            my_db.cur.execute("SELECT * FROM reg_tbl")
            myresult = my_db.cur.fetchall()
            print(type(myresult))
        except:
            my_db.conn.rollback()

        finally:
            my_db.conn.close()
        return render_template('/user-management/user-list.html', myresult=myresult, sec=session['username'])
    return render_template('homepages/login.htm')


@auth.route('/delete', methods=['POST', 'GET'])
def delete():
    id = request.args.get('user')
    try:
        my_db.connection()
        sql = "delete from reg_tbl where id = %s"
        val = (id,)
        my_db.cur.execute(sql, val)

        my_db.conn.commit()
    except:

        my_db.conn.rollback()

    finally:
        my_db.conn.close()
    return json.dumps({"type": "error"})


@auth.route('/admin/user/edit', methods=['POST', 'GET'])
def edit():
    if 'username' in session:
        flag = False
        if request.method == 'GET':
            id = request.args.get('id')
            try:
                my_db.connection()
                sql = "SELECT * FROM reg_tbl where id=%s"
                val = (id,)
                my_db.cur.execute(sql, val)
                myresult = my_db.cur.fetchone()
               
                
                return render_template('user-management/edit-user.html', sec=session['username'], myresults=myresult, country=get_conutry())
            except mysql.connector.Error as err:
                my_db.conn.rollback()

            finally:
                my_db.conn.close()
        error = {}

        if request.method == 'POST':

            id = request.form['id']
            f_name = request.form['fname']
            l_name = request.form['lname']
            u_name = request.form['uname']
            email = request.form['email']
            passwd = request.form['psw']
            c_passwd = request.form['c_psw']
            contact = request.form['p_no']
            country = request.form['country']
            state = request.form['state']
            city = request.form['city']
            pin = request.form['pin']
            address = request.form['address']

            if f_name == "":
                error['f_name'] = "First name is Required"

            if l_name == "":
                error['l_name'] = "Last name is Required"

            if u_name == "":
                error['u_name'] = "User name is Required"

            if email == "":
                error['email'] = "E-mail is required"
            else:
                if email_error(email) is None:
                    error['email'] = "Enter a valid email"
            if passwd is not "":
                if len(passwd) < 6:
                    error['psw'] = "Password must be at least 6 characters"
                else:
                    if lower_error(passwd) is None:
                        error['psw_l'] = "Password must be at least one lower character"

                    if upcase_error(passwd) is None:
                        error['psw_u'] = "Password must be at least one Upper character"

                    if digit_error(passwd) is None:
                        error['psw_d'] = "Password must be at least one Numeric digits"

                    if symbol_error(passwd) is None:
                        error['psw_s'] = "Password must be at least one Special Character"
                    flag = True

            if passwd != c_passwd:
                error['c_psw'] = "Password and Confirm Password does not Match"

            if contact.isdecimal() is False or contact == "":
                error['p_no'] = "Numeric value Required! in Contact"
            else:
                if len(contact) != 10:
                    error['p_no'] = "Enter 10 digits only in contact"
            if country == '0':
                error['country'] = "please select a country"

            if state == '0':
                error['state'] = "please select a state"

            if city == '0':
                error['city'] = "please select a city"

            if pin == '':
                error['pin'] = "please select a pin code"

            if address == "":
                error['address'] = "Address is Required!"

            if len(error) == 0:

                hash_passwd = hash_password(passwd)
                try:
                    my_db.connection()
                    if flag:
                        sql = "update reg_tbl set first_name=%s,last_name=%s,user_name=%s,e_mail=%s," \
                              "password=%s,contact=%s,country=%s,state=%s,city=%s,pin=%s,address =%s where id = %s"
                        val = (f_name, l_name, u_name, email, hash_passwd, contact, country, state, city, pin, address, id)
                    else:

                        sql = "update reg_tbl set first_name=%s,last_name=%s,user_name=%s,e_mail=%s," \
                              "contact=%s,country=%s,state=%s,city=%s,pin=%s,address =%s where id = %s"

                        val = (f_name, l_name, u_name, email, contact, country, state, city, pin, address, id)

                    my_db.cur.execute(sql, val)
                    my_db.conn.commit()

                    flash('User has been updated successfully!')
                    return redirect(url_for('auth.list_user'))
                except:
                    my_db.conn.rollback()
                finally:
                    my_db.conn.close()
        return render_template('user-management/edit-user.html', sec=session['username'],error=error, myresults=myresult, country=get_conutry())

    return render_template('homepages/login.htm')

