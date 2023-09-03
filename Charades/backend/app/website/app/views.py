from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify, flash
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


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and 'username' in session:
        user_responses = json.loads(request.form.get('userResponses'))
        if user_responses:
            username = session['username']
            total_points = sum([1 for response in user_responses if response['isCorrect']])
            won = total_points / len(user_responses) >= 0.8
            flash(user_responses)
            users_data.db.db_data.insert_one({
                'username': username,
                'total_points': total_points,
                'won': won,
                'responses': user_responses
            })
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


def get_category_number(category_name, categories_dict):
    if category_name in categories_dict:
        return categories_dict[category_name]
    else:
        return None


@views.route('/profile')
def profile():
    if session['username']:
        user_info = mongo.db.users.find_one({'name': session['username']})
        games = users_data.db.db_data.find({"username": session['username']})
        games_count = 0
        won = 0
        for game in games:
            if game['won']:
                won += 1
            games_count += 1
        return render_template('profile.html', user_info=user_info, won=won, games=games_count)
    else:
        return 'Musisz się zalogować, aby zobaczyć swój profil.'


@views.route('/game/<category>')
def game(category: str):
    if session['username']:
        category_number = get_category_number(category, categories)
        url = f'https://opentdb.com/api.php?amount=2&category={category_number}&difficulty=medium&type=multiple'
        with urlrequ.urlopen(url) as response:
            data = response.read()
            decoded_data = data.decode('utf-8')
            json_data = json.loads(decoded_data)
        return render_template('game.html', data=json_data)
    return render_template("choose-game.html")


@views.route('/history')
def history():
    if 'username' in session:
        user = mongo.db.users.find_one({"name": session['username']})
        if user:
            games = users_data.db.db_data.find({"username": session['username']})
            total_points = 0
            games_count = 0
            game_data = []
            for game in games:
                game_info = {
                    'points': game['total_points'],
                    'category': game['responses'][0]['category'],
                    'other_fields': {
                        'won': game['won'],
                        'user_responses': game['responses']
                    }
                }
                total_points += game['total_points']
                games_count += 1
                game_data.append(game_info)
            user['total_points'] = total_points
            user['games_count'] = games_count
            return render_template('history.html', user=user, games=game_data)
        else:
            return redirect(url_for('views.home'))
    else:
        return redirect(url_for('views.login'))
