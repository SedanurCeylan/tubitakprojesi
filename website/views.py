from mailbox import Message
from flask import Blueprint, render_template, request, jsonify, flash
from flask_login import login_required, current_user
import pytz
from .models import BeignDataset, GeneratedDataDataset, LearnedInfo, MaliciousDataset, User, AnalysisResult
from . import db
import random
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Result, func, text
import pandas as pd
import json
import mysql.connector
from flask import redirect, url_for
from flask import Flask, request, jsonify
from flask_login import current_user
from website import db
from website.models import User

views = Blueprint('views', __name__)


@views.route('/')

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if not note:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.context_processor
def inject_user():
    return {'user': current_user}

@views.route('/data')
def data_display():
    datasets = MaliciousDataset.query.all()  
    random_data1 = random.choice(datasets)
    random_data2 = random.choice(datasets)
    random_data3 = random.choice(datasets)

    return render_template('data_display.html', random_data1=random_data1, random_data2=random_data2, random_data3=random_data3)


@views.route('/start-test')
def start_test():
    return render_template('test_page.html')

@views.route('/test_page')
def test_page():
    return render_template('test_page.html')

@views.route('/malicious')
def malicious():
    malicious_data = MaliciousDataset.query.all()
    sample_data = random.sample(malicious_data, min(20, len(malicious_data)))
    title = "Details of Malicious Data"
    return render_template('data_display.html', data=sample_data, title=title)

@views.route('/benign')
def benign():
    benign_data = BeignDataset.query.all()
    sample_data = random.sample(benign_data, min(20, len(benign_data)))
    title = "Details of Benign Data"
    return render_template('data_display.html', data=sample_data, title=title)

@views.route('/next-page')
def next_page():
    malicious_data = MaliciousDataset.query.all()
    benign_data = BeignDataset.query.all()

    sample_malicious = random.sample(malicious_data, min(10, len(malicious_data)))
    sample_benign = random.sample(benign_data, min(10, len(benign_data)))

    mixed_samples = sample_malicious + sample_benign
    random.shuffle(mixed_samples)

    return render_template('next_page.html', data=mixed_samples)



@views.route('/sonuclar', methods=['GET', 'POST'])
@login_required
def sonuclar():
    if request.method == 'POST':
        data = request.get_json()
        score = data.get('score')

        user = User.query.get(current_user.id)
        if user:
            user.test_score += score
            db.session.commit()

        new_result = AnalysisResult(score=score, user_id=current_user.id)
        db.session.add(new_result)
        db.session.commit()

        return jsonify({"status": "success"})

    results = AnalysisResult.query.filter_by(user_id=current_user.id).order_by(AnalysisResult.timestamp.desc()).all()
    test_score = current_user.test_score 

    return render_template('sonuclar.html', results=results, test_score=test_score)


@views.route('/quiz')
@login_required
def quiz():
    return render_template('quiz.html')

@views.route('/hakkimda')
def hakkimda():
    return render_template('hakkimda.html')

@views.route('/senaryo1')
def senaryo1():
    Session = sessionmaker(bind=db.engine)
    session = Session()
    
    query = text("SELECT * FROM generated_data_dataset ORDER BY RAND() LIMIT 5")
    result = session.execute(query)
    data = result.fetchall()
    
    print(data)
    
    session.close()
    
    return render_template('senaryo1.html', data=data)

@views.route('/senaryo2')
def senaryo2():
    Session = sessionmaker(bind=db.engine)
    session = Session()
    
    query = text("SELECT * FROM generated_data_dataset ORDER BY RAND() LIMIT 5")
    result = session.execute(query)
    data = result.fetchall()
    
    print(data)
    
    session.close()
    
    return render_template('senaryo2.html', data=data)

@views.route('/senaryo3')
def senaryo3():
    Session = sessionmaker(bind=db.engine)
    session = Session()
    
    query = text("SELECT * FROM generated_data_dataset ORDER BY RAND() LIMIT 5")
    result = session.execute(query)
    data = result.fetchall()
    
    
    print(data)
    
    session.close()
    
    return render_template('senaryo3.html', data=data)


@views.route('/senaryo4')
@login_required
def senaryo4():
    return render_template('senaryo4.html')

@views.route('/senaryo5')
@login_required
def senaryo5():
    return render_template('senaryo5.html')


@views.route('/profil')
@login_required
def profil():
    users = User.query.order_by(User.total_score.desc()).all()  
    learned_info = LearnedInfo.query.filter_by(user_id=current_user.id).first()  
    return render_template('profil.html', user=current_user, users=users, learned_info=learned_info)

    
@views.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = User.query.get(current_user.id)  
    errors = {}

    if request.method == 'POST':
        new_username = request.form.get('username')
        new_photo = request.form.get('profile_picture')

        special_characters = ['<', '>', '#', '\'', '!', '@', '$', '%', '^', '&', '*', '(', ')', '+', '=', '{', '}', '[', ']', '|', '\\', ':', ';', '"', ',', '<', '>', '?', '/', '`', '~']
        if any(char in special_characters for char in new_username):
            errors['username'] = 'Kullanıcı adı özel karakterler içeremez, yalnızca harfler, rakamlar ve "." kullanılabilir.'

       
        existing_user = User.query.filter_by(username=new_username).first()
        if existing_user and existing_user.id != current_user.id:
            errors['username'] = 'Bu kullanıcı adı zaten kullanımda.'

        if errors:
            return render_template('edit_profile.html', user=user, photos=["default.png", "photo1.png", "photo2.png", "photo3.png", "photo4.png", "photo5.png", "photo6.png"], errors=errors)

        user.username = new_username
        user.profile_picture = new_photo

        try:
            db.session.commit()
            flash('Profil başarıyla güncellendi!', category='success')
        except Exception as e:
            db.session.rollback()  
            flash('Bir hata oluştu. Lütfen tekrar deneyin.', category='error')

        return redirect(url_for('views.profil'))


    photos = ["default.png", "photo1.png", "photo2.png", "photo3.png", "photo4.png", "photo5.png", "photo6.png"]

    return render_template('edit_profile.html', user=user, photos=photos)




app = Flask(__name__)

@views.route('/update_score', methods=['POST'])
def update_score():
    if request.method == 'POST':
        data = request.get_json()
        total_score = data.get('total_score')
        
        user = User.query.get(current_user.id)
        if user:
            user.total_score = total_score
            db.session.commit()
            return jsonify({"status": "success", "total_score": total_score})
        else:
            return jsonify({"status": "error", "message": "User not found"}), 404





from flask_login import current_user

@views.route('/save-learned-info', methods=['POST'])
@login_required
def save_learned_info():
    data = request.get_json()
    if not data or 'learnedText' not in data or 'scenario' not in data:
        return jsonify({'success': False, 'message': 'Geçersiz veri'}), 400

    learned_text = data['learnedText']
    scenario = data['scenario']

    
    user_id = current_user.id  
    existing_info = LearnedInfo.query.filter_by(user_id=user_id).first() 
    if not existing_info:
        existing_info = LearnedInfo(user_id=user_id)  

    if scenario == 'senaryo1':
        existing_info.senaryo1_learned_text = learned_text
    elif scenario == 'senaryo2':
        existing_info.senaryo2_learned_text = learned_text
    elif scenario == 'senaryo3':
        existing_info.senaryo3_learned_text = learned_text
    elif scenario == 'senaryo4':
        existing_info.senaryo4_learned_text = learned_text  
    elif scenario == 'senaryo5':
        existing_info.senaryo5_learned_text = learned_text


    try:
        db.session.add(existing_info)
        db.session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500



@views.route('/results')
@login_required
def results():
    results = AnalysisResult.query.filter_by(user_id=current_user.id).all()  
    return render_template('sonuclar.html', results=results)
