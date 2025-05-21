from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User


app = Flask(__name__)
app.secret_key = '123'

# Configure SQLite DB
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "users.db")}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered!')
            return redirect(url_for('signup'))

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created! Please login.')
        return redirect(url_for('login'))

    return render_template('signup.html')

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
            return redirect(url_for('login'))

    return render_template('login.html')

#dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)
#logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
#   contact
@app.route('/contact')
def contact():
    return render_template('contact.html')
#  menu
@app.route('/menu')
def menu():
    return render_template('menu.html')
#SHOP
@app.route('/shop')
def shop():
    return render_template('shop.html')

#  gallery
@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


#home
@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


