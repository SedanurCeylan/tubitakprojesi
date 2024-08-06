from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        # Kullanıcı adı, email ve şifrelerin dolu olduğunu kontrol et
        if not username or not email or not password or not confirm_password:
            flash('All fields are required.', category='error')
            return render_template("sign_up.html")

        # Şifrelerin eşleştiğini kontrol et
        if password != confirm_password:
            flash('Passwords must match.', category='error')
            return render_template("sign_up.html")

        # E-posta adresinin zaten kullanımda olup olmadığını kontrol et
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already in use.', category='error')
            return render_template("sign_up.html")

        # Şifreyi hashle ve yeni kullanıcıyı oluştur
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)

        try:
            db.session.commit()
            flash('Account created successfully!', category='success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            print(f"Failed to create user: {e}")
            flash('Failed to create account.', category='error')

    return render_template("sign_up.html")

@auth.route('/test_page')
def test_page():
    return render_template('test_page.html')
