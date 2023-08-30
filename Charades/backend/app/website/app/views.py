from flask import Blueprint, render_template, redirect, url_for, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from website import mongo

views = Blueprint('views', __name__)


@views.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', logged_in=True)
    return render_template('home.html', logged_in=False)


@views.route('/choose-game')
def choose_game():
    if 'username' in session:
        return render_template('choose-game.html')
    else:
        error = "Please log in first"
        return render_template('home.html', error=error)



@views.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        existing_user = mongo.db.users.find_one({'name': request.form['username']})
        if existing_user is None:
            hashpass = generate_password_hash(request.form['password'], method='sha256')
            mongo.db.users.insert_one({
                'name': request.form['username'],
                'email': request.form['email'],
                'password': hashpass
            })
            return redirect(url_for('views.home'))
        error = 'That username already exists!'
        return render_template('register.html', error=error)
    return render_template('register.html')


@views.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        login_user = mongo.db.users.find_one({'name': request.form['username']})
        if login_user:
            if check_password_hash(login_user['password'], request.form['password']):
                session['username'] = request.form['username']
                return redirect(url_for('views.home'))
            else:
                error = 'Wrong password'
        else:
            error = 'Wrong user name'
    return render_template('login.html', error=error)


@views.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('views.home'))
