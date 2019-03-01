from flask import Flask, render_template
from user_management import auth
from category_manager import cat_manager
from article_manager import art_manager
from login import log
from page_manager import page
from slider_manager import sld_manager
import os
app = Flask(__name__)

app.register_blueprint(auth)
app.register_blueprint(cat_manager)
app.register_blueprint(art_manager)
app.register_blueprint(log)
app.register_blueprint(page)
app.register_blueprint(sld_manager)

'''app.secret_key = os.urandom(12)'''
app.secret_key = "b'\x95\x12Y\x97\xcd\x07>\x00J\xcc\x91\x17'"


@app.route('/')
def home():
    return render_template('homepages/home.html')


@app.route('/about')
def about():
    return render_template('homepages/about.html')


@app.route('/contact')
def contact():
    return render_template('homepages/contact.html')


if __name__ == "__main__":

    print(os.urandom(12))
    app.run(debug=True)
