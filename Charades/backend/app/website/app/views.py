from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from website import mongo, users_data
from urllib import request as urlrequ
import json

views = Blueprint('views', __name__)

categories = {
    "Animals": 27,
    "Celebrities": 26,
    "Art": 25,
    "Politics": 24,
    "History": 23,
    "Geography": 22,
    "Sports": 21,
    "Mythology": 20,
    "Mathematics": 19,
}


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
            users_data.insert_one({
                'name': request.form['username'],
                'points': 0,
                'wins': 0
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


def get_category_number(category_name, categories_dict):
    if category_name in categories_dict:
        return categories_dict[category_name]
    else:
        return None


@views.route('/profile')
def profile():
    print("siema")
    if session['username']:
        user_info = mongo.find_one({'name': session['username']})
        user_stats = users_data.find_one({'name': session['username']})
        print(user_info)
        return render_template('profile.html', user_info=user_info, user_stats=user_stats)
    else:
        return 'Musisz się zalogować, aby zobaczyć swój profil.'


@views.route('/game/<category>')
def game(category: str):
    if session['username']:
        category_number = get_category_number(category, categories)
        url = f'https://opentdb.com/api.php?amount=10&category={category_number}&difficulty=medium&type=multiple'
        with urlrequ.urlopen(url) as response:
            data = response.read()
            decoded_data = data.decode('utf-8')
            json_data = json.loads(decoded_data)
        return render_template('game.html', data=json_data)
    return render_template("choose-game.html")


@views.route('/history')
def history():
    if session['username']:
        user = mongo.find_one({"name": session['username']})
        if user:
            games = users_data.find({"user_id": user["_id"]})
            return render_template('history.html', user=user, games=games)
        else:
            return "Nie znaleziono użytkownika o podanej nazwie."
    else:
        return "Zaloguj się"
