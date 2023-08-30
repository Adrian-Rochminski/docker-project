from flask import Blueprint, render_template, redirect, url_for, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from website import mongo

views = Blueprint('views', __name__)


@views.route('/')
def index():
    if 'username' in session:
        return render_template('home.html', logged_in=True)
    return render_template('home.html', logged_in=False)


@views.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        existing_user = mongo.db.users.find_one({'name': request.form['username']})
        if existing_user is None:
            hashpass = generate_password_hash(request.form['pass'], method='sha256')
            mongo.db.users.insert({'name': request.form['username'], 'password': hashpass})
            return redirect(url_for('index'))
        return 'That username already exists!'
    return render_template('register.html')


@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_user = mongo.db.users.find_one({'name': request.form['username']})
        if login_user:
            if check_password_hash(login_user['password'], request.form['pass']):
                session['username'] = request.form['username']
                return redirect(url_for('index'))
        return 'Invalid username or password'
    return render_template('login.html')


@views.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
