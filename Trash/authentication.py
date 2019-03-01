import my_db
from functions import *
from flask import session, render_template, request, redirect, url_for, Blueprint, json

auth = Blueprint('auth', __name__)


@auth.route('/registration')
def registers():
    if 'username' in session:
        return redirect(url_for('auth.get'))

    myresult = "na"
    try:
        my_db.connection()

        my_db.cur.execute("SELECT * FROM countries")

        myresult = my_db.cur.fetchall()

        print(myresult)
    except:
        my_db.conn.rollback()

    finally:
        my_db.conn.close()

    return render_template('registration.htm',myresult=myresult)


@auth.route('/dashboard')
def get():
    if 'username' in session:
        return render_template('', sec=session['username'])
    return render_template("login.htm")


@auth.route('/registration_post', methods=['POST'])
def registration_post():
    if 'username' in session:
        return redirect(url_for('auth.get'))
    else:
        error = []
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

            if f_name == "":
                error.append("First name is Required")

            if l_name == "":

                error.append("Last name is Required")

            if u_name == "":

                error.append("User name is Required")

            if email == "":
                error.append("E-mail is required")
            else:
                if email_error(email) is None:
                    error.append("Enter a valid email")

            if len(passwd) < 6:
                error.append("Password must be at least 6 characters")
            else:
                pass
                if lower_error(passwd) is None:
                    error.append("Password must be at least one lower character")

                if upcase_error(passwd) is None:
                    error.append("Password must be at least one Upper character")

                if digit_error(passwd) is None:
                    error.append("Password must be at least one Numeric digits")

                if symbol_error(passwd) is None:
                    error.append("Password must be at least one Special Character" )

            if passwd != c_passwd or c_passwd is '':
                error.append("Password and Confirm Password does not Match")

            if contact.isdecimal()is False or contact == "":
                error.append("Numeric value Required! in Contact")
            else:
                if len(contact) != 10:
                    error.append("Enter 10 digits only in contact")

            if country == '0':
                error.append("please select a country")

            if state == '0':
                error.append("please select a state")

            if city == '0':
                error.append("please select a city")

            if pin == '':
                error.append("Pin code  is Required!")

            if address == "":
                error.append("Address is Required!")

            if len(error) != 0:
                return json.dumps({"type": "error", "result": error})

            else:
                hash_passwd = hash_password(passwd)
                try:
                    my_db.connection()

                    sql = "insert into reg_tbl(first_name,last_name,user_name,e_mail," \
                          "password,contact,country,state,city,pin,address )" \
                          " values (%s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s)"

                    val = (f_name, l_name, u_name, email, hash_passwd, contact, country, state, city, pin, address)
                    my_db.cur.execute(sql, val)
                    my_db.conn.commit()
                    my_db.cur.rowcount()

                except:
                    my_db.conn.rollback()
                finally:
                    my_db.conn.close()

                return json.dumps({"type": "success"})


@auth.route('/get_state', methods=['POST', 'GET'])
def get_state():

    myresult = "na"
    country=request.args.get('country')
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
    print(myresult)
    return json.dumps({"type": "get_city", "result":  myresult})


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


@auth.route('/login_post', methods=['POST', 'GET'])
def login_post():
    error = {}
    if request.method == 'POST':
        email = request.form['email']
        passwd = request.form['psw']

        if email == '':
            error['e'] = 'E-mail is required'

        if passwd == '':
            error['p'] = 'Enter Password'

        if len(error) != 0:
            return render_template('login.htm', error=error)
        else:
            hash_pass = hash_password(passwd)
            myresult = "na"
            val = (email, hash_pass, )
            try:
                my_db.connection()
                sql = "SELECT * FROM reg_tbl where e_mail=%s and  password=%s"
                my_db.cur.execute(sql, val)

                myresult = my_db.cur.fetchone()
            except:
                my_db.conn.rollback()
            finally:
                my_db.conn.close()
            if myresult is None:
                error['ep'] = "Email and password does not match"
                return render_template('login.htm', error=error)
            else:
                session['username'] = myresult
                return redirect(url_for('auth.get'))
    return render_template('login.htm')


@auth.route('/login')
def index():
    if 'username' in session:
        return redirect(url_for('auth.get'))
    return render_template("login.htm")


@auth.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('auth.index'))


@auth.route('/data_list')
def list_user():
    if 'username' in session:
        myresult = "na"
        try:
            my_db.connection()
            my_db.cur.execute("SELECT * FROM reg_tbl")
            myresult = my_db.cur.fetchall()

        except:
            my_db.conn.rollback()

        finally:
            my_db.conn.close()
        return render_template('list_user.html', sec=session['username'], myresult=myresult)
    return render_template("login.htm")


@auth.route('/add_user')
def add_user():
    if 'username' in session:
        myresult = "na"
        try:
            my_db.connection()

            my_db.cur.execute("SELECT * FROM countries")

            myresult = my_db.cur.fetchall()

        except:
            my_db.conn.rollback()

        finally:
            my_db.conn.close()

        return render_template('registration.html', myresult=myresult, sec=session['username'])

    return render_template("login.htm")


@auth.route('/delete', methods=['POST', 'GET'])
def delete():
    user1 = request.args.get('user')
    try:
        my_db.connection()
        sql="delete from reg_tbl where user_name = %s"
        val=(user1, )
        my_db.cur.execute(sql, val)
        
        my_db.conn.commit()
    except:

        my_db.conn.rollback()

    finally:
        my_db.conn.close()
    return json.dumps({"type": "error"})


@auth.route('/add_user_post', methods=['POST', 'GET'])
def add_user_reg():
    error = []
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

            if f_name == "":
                error.append("First name is Required")

            if l_name == "":

                error.append("Last name is Required")

            if u_name == "":

                error.append("User name is Required")

            if email == "":
                error.append("E-mail is required")
            else:
                if email_error(email) is None:
                    error.append("Enter a valid email")

            if len(passwd) < 6:
                error.append("Password must be at least 6 characters")
            else:
                pass
                if lower_error(passwd) is None:
                    error.append("Password must be at least one lower character")

                if upcase_error(passwd) is None:
                    error.append("Password must be at least one Upper character")

                if digit_error(passwd) is None:
                    error.append("Password must be at least one Numeric digits")

                if symbol_error(passwd) is None:
                    error.append("Password must be at least one Special Character" )

            if passwd != c_passwd or c_passwd is '':
                error.append("Password and Confirm Password does not Match")

            if contact.isdecimal()is False or contact == "":
                error.append("Numeric value Required! in Contact")
            else:
                if len(contact) != 10:
                    error.append("Enter 10 digits only in contact")

            if country == '0':
                error.append("please select a country")

            if state == '0':
                error.append("please select a state")

            if city == '0':
                error.append("please select a city")

            if pin == '':
                error.append("Pin code  is Required!")

            if address == "":
                error.append("Address is Required!")

            if len(error) != 0:
                return json.dumps({"type": "error", "result": error})

            else:
                hash_passwd = hash_password(passwd)
                try:
                   ''' my_db.connection()

                    sql = "insert into reg_tbl(first_name,last_name,user_name,e_mail," \
                          "password,contact,country,state,city,pin,address )" \
                          " values (%s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s)"

                    val = (f_name, l_name, u_name, email, hash_passwd, contact, country, state, city, pin, address)
                    my_db.cur.execute(sql, val)
                    my_db.conn.commit()
                    my_db.cur.rowcount()'''

                except:
                    my_db.conn.rollback()
                finally:
                    my_db.conn.close()

            return json.dumps({"type": "success"})


@auth.route('/edit', methods=['POST', 'GET'])
def edit():
    if 'username' in session:
        myresult = "na"
        user1 = request.args.get('user')
        try:
            my_db.connection()
            sql = "delete from reg_tbl where user_name = %s"
            val = (user1,)
            my_db.cur.execute(sql, val)

            my_db.conn.commit()
        except:

            my_db.conn.rollback()

        finally:
            my_db.conn.close()
        return render_template('edit.html', myresult=myresult, sec=session['username'])

    return render_template("login.htm")


{{url_for('about')}}
 #               {% include 'template-parts/left.html' %}

#         delete(art.config['UPLOAD_FOLDER'], myresult['image'])

''''
{{url_for('page.edit',id=sece.id)}}
'''








