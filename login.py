from flask import session, render_template, request, redirect, url_for, Blueprint
from functions import hash_password
import my_db

log = Blueprint('log', __name__)


@log.route('/login')
def login():
    user_id = request.cookies.get('userID')
    if 'username' in session:
        '''logs.secret_key = os.urandom(12)
        session['username'] = user_id'''
        return redirect(url_for('log.dashboard'))
    return render_template('homepages/login.htm')


@log.route('/login-post', methods=['GET','POST'])
def login_post():
    error = {}

    if request.method == 'POST':

        username = request.form['email']
        passwd = request.form['psw']

        if username == '':
            error['e'] = 'E-mail is required'

        if passwd == '':
            error['p'] = 'Enter Password'

        if len(error) == 0:
            hash_pass = hash_password(passwd)
            myresult = ""
            val = (username, hash_pass, )
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

            else:
                session['username'] = myresult

                '''resp = make_response(redirect('/admin/dashboard'))
                resp.set_cookie('userID', myresult)
                return resp'''
                return redirect(url_for('log.dashboard'))
        return render_template('homepages/login.htm', error=error)
    return redirect(url_for('log.login'))


'''@log.route('/do-that')
def do_that():
    user_id = request.cookies.get('userID')
    if user_id:
        user = get(user_id)
        if user:
            session['username'] = user
            return render_template('dashboard.html',sec=session['username'])
    return redirect(url_for('login'))'''


@log.route('/admin/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', sec=session['username'])
    return render_template('homepages/login.htm')


@log.route('/logout')
def logout():
    session.pop('username')
    '''s=request.session
    s.cookies.clear()'''
    return redirect(url_for('log.login'))
