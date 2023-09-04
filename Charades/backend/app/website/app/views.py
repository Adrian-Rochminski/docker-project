import hashlib
from flask import Blueprint, render_template, redirect, url_for, request, session, flash, jsonify
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
            flash('Answers submitted successfully!', 'success')
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
        flash('Please log in first', 'danger')
        return render_template('home.html')


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
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('views.home'))
        flash('That username already exists. Please choose a different one.', 'danger')
    return render_template('register.html')


@views.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        login_user = mongo.db.users.find_one({'name': request.form['username']})
        if login_user:
            if check_password_hash(login_user['password'], request.form['password']):
                session['username'] = request.form['username']
                flash('Login successful!', 'success')
                return redirect(url_for('views.home'))
            else:
                error = 'Wrong password'
        else:
            error = 'Wrong username'
        flash(error, 'danger')
    return render_template('login.html')


@views.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('views.home'))


def get_category_number(category_name, categories_dict):
    if category_name in categories_dict:
        return categories_dict[category_name]
    else:
        return None


@views.route('/profile')
def profile():
    if session.get('username'):
        user_info = mongo.db.users.find_one({'name': session['username']})
        games = users_data.db.db_data.find({"username": session['username']})
        games_count = 0
        won = 0
        for game in games:
            if game['won']:
                won += 1
            games_count += 1
        email = user_info.get('email', '')
        hash = hashlib.md5(email.encode()).hexdigest()
        user_image_url = f"https://api.adorable.io/avatars/150/{hash}.png"
        return render_template('profile.html', user_info=user_info, won=won, games=games_count,
                               user_image=user_image_url)
    else:
        flash('You must log in to view your profile.', 'danger')
        return redirect(url_for('views.login'))


@views.route('/game/<category>')
def game(category: str):
    if session.get('username'):
        category_number = get_category_number(category, categories)
        url = f'https://opentdb.com/api.php?amount=2&category={category_number}&difficulty=medium&type=multiple'
        with urlrequ.urlopen(url) as response:
            data = response.read()
            decoded_data = data.decode('utf-8')
            json_data = json.loads(decoded_data)
        return render_template('game.html', data=json_data)
    flash('Please log in to play the game.', 'danger')
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
            flash('User not found.', 'danger')
            return redirect(url_for('views.home'))
    else:
        flash('Please log in to view your game history.', 'danger')
        return redirect(url_for('views.login'))
