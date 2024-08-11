import re
from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    errors = {}

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Özel karakter kontrolü
        special_characters = ['<', '>', '#', '\'', '!', '$', '%', '^', '&', '*', '(', ')', '+', '=', '{', '}', '[', ']', '|', '\\', ':', ';', '"', ',', '<', '>', '?', '/', '`', '~']
        if any(char in special_characters for char in email):
            errors['email'] = 'Special characters are not allowed in email.'
        if any(char in special_characters for char in password):
            errors['password'] = 'Special characters are not allowed in password.'

        if errors:
            return render_template("login.html", errors=errors)

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            errors['login'] = 'Kullanıcı adı veya şifre yanlış.'

        if errors:
            
            return render_template("login.html", errors=errors)


        if errors:
            return render_template("login.html", errors=errors)
        else:
            login_user(user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("login.html")





@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    errors = {}  # Hata mesajlarını depolamak için bir sözlük oluşturuyoruz.

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        # Özel karakterleri kontrol et
        special_characters = ['<', '>', '#', '\'', '!', '$', '%', '^', '&', '*', '(', ')', '+', '=', '{', '}', '[', ']', '|', '\\', ':', ';', '"', ',', '<', '>', '?', '/', '`', '~']
        if any(char in special_characters for char in username):
            errors['username'] = 'Special characters are not allowed in username.'
        if any(char in special_characters for char in email):
            errors['email'] = 'Special characters  are not allowed in email.'

        # Kullanıcı adı, email ve şifrelerin dolu olduğunu kontrol et
        if not username:
            errors['username'] = 'Username is required.'
        if not email:
            errors['email'] = 'Email is required.'
        if not password:
            errors['password'] = 'Password is required.'
        if not confirm_password:
            errors['confirm_password'] = 'Confirm Password is required.'

      

        if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'[0-9]', password) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors['password'] = 'Password must be at least 8 characters long and include an uppercase letter, a lowercase letter, a number, and a special character.'

        # Şifrelerin eşleştiğini kontrol et
        if password != confirm_password:
            errors['confirm_password'] = 'Passwords must match.'

        # Kullanıcı adı veya e-posta adresinin zaten kullanımda olup olmadığını kontrol et
        existing_user_email = User.query.filter_by(email=email).first()
        existing_user_username = User.query.filter_by(username=username).first()
        if existing_user_email:
            errors['email'] = 'Email already in use.'
        if existing_user_username:
            errors['username'] = 'Username already in use.'

        # Hatalar varsa, sayfayı yeniden render et ve hataları göster
        if errors:
            return render_template("sign_up.html", errors=errors, username=username, email=email)

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





@auth.route('/sonuclar')
def sonuclar():
    return render_template('sonuclar.html')

