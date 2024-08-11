from mailbox import Message
from flask import Blueprint, render_template, request, jsonify, flash
from flask_login import login_required, current_user
import pytz
from .models import BeignDataset, GeneratedDataDataset, MaliciousDataset, User, AnalysisResult
from . import db
import random
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
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
    datasets = MaliciousDataset.query.all()  # Veritabanından verileri çekerken hangi tabloyu kullanacağını belirtiyoruz

    random_data1 = random.choice(datasets)
    random_data2 = random.choice(datasets)
    random_data3 = random.choice(datasets)

    return render_template('data_display.html', random_data1=random_data1, random_data2=random_data2, random_data3=random_data3)

@views.route('/submit-analysis', methods=['POST'])
def submit_analysis():
    selected_rows = request.json.get('selected_rows')
    total_samples = len(selected_rows)
    malicious_samples = len([row for row in selected_rows if row['source'] == 'malicious'])
    
    if total_samples > 0:
        accuracy = (malicious_samples / total_samples) * 100
    else:
        accuracy = 0

    return jsonify({'accuracy': accuracy})

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
    title = "Zararlı Verilerin Detayları"
    return render_template('data_display.html', data=sample_data, title=title)

@views.route('/benign')
def benign():
    benign_data = BeignDataset.query.all()
    sample_data = random.sample(benign_data, min(20, len(benign_data)))
    title = "Zararsız Verilerin Detayları"
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
def sonuclar():
    if request.method == 'POST':
        data = request.get_json()
        accuracy = data.get('accuracy')
        
        # Yeni bir analiz sonucu oluştur ve veritabanına ekle
        new_result = AnalysisResult(accuracy=accuracy)
        db.session.add(new_result)
        db.session.commit()
        return jsonify({"status": "success"})
    
    # Tüm analiz sonuçlarını al ve sonuclar.html sayfasına gönder
    results = AnalysisResult.query.order_by(AnalysisResult.timestamp.desc()).all()
    return render_template('sonuclar.html', results=results)


@views.route('/quiz')
@login_required
def quiz():
    return render_template('quiz.html')

@views.route('/hakkimda')
def hakkimda():
    return render_template('hakkimda.html')

@views.route('/senaryo1')
@login_required
def senaryo1():
    # Veritabanı oturumu oluştur
    Session = sessionmaker(bind=db.engine)
    session = Session()
    
    # generated_data_dataset tablosundan rastgele beş satır çek
    query1 = text("SELECT * FROM generated_data_dataset ORDER BY RAND() LIMIT 5")
    result1 = session.execute(query1)
    data_generated = result1.fetchall()
    
    # malicious_dataset tablosundan rastgele beş satır çek
    query2 = text("SELECT * FROM malicious_dataset ORDER BY RAND() LIMIT 5")
    result2 = session.execute(query2)
    data_malicious = result2.fetchall()
    
    # Verileri konsola yazdır
    print("Generated Data:", data_generated)
    print("Malicious Data:", data_malicious)
    
    session.close()
    
    return render_template('senaryo1.html', data_generated=data_generated, data_malicious=data_malicious)

@views.route('/senaryo2')
def senaryo2():
    # Veritabanı oturumu oluştur
    Session = sessionmaker(bind=db.engine)
    session = Session()
    
    # Veritabanından rastgele üç satır çek
    query = text("SELECT * FROM generated_data_dataset ORDER BY RAND() LIMIT 5")
    result = session.execute(query)
    data = result.fetchall()
    
    # Verileri konsola yazdır
    print(data)
    
    session.close()
    
    return render_template('senaryo2.html', data=data)

@views.route('/senaryo3')
@login_required
def senaryo3():
    return render_template('senaryo3.html')

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
    users = User.query.order_by(User.total_score.desc()).all()  # Tüm kullanıcıları puana göre sırala
    return render_template('profil.html', user=current_user, users=users)

@views.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = User.query.get(current_user.id)  # Mevcut kullanıcıyı al
    errors = {}

    if request.method == 'POST':
        new_username = request.form.get('username')
        new_photo = request.form.get('profile_picture')

        # Özel karakter kontrolü (noktali harfler hariç)
        special_characters = ['<', '>', '#', '\'', '!', '@', '$', '%', '^', '&', '*', '(', ')', '+', '=', '{', '}', '[', ']', '|', '\\', ':', ';', '"', ',', '<', '>', '?', '/', '`', '~']
        if any(char in special_characters for char in new_username):
            errors['username'] = 'Kullanıcı adı özel karakterler içeremez, yalnızca harfler, rakamlar ve "." kullanılabilir.'

        # Kullanıcı adının zaten kullanımda olup olmadığını kontrol et
        existing_user = User.query.filter_by(username=new_username).first()
        if existing_user and existing_user.id != current_user.id:
            errors['username'] = 'Bu kullanıcı adı zaten kullanımda.'

        if errors:
            return render_template('edit_profile.html', user=user, photos=["default.png", "photo1.png", "photo2.png", "photo3.png", "photo4.png", "photo5.png", "photo6.png"], errors=errors)

        # Kullanıcı adı ve profil fotoğrafını güncelle
        user.username = new_username
        user.profile_picture = new_photo

        try:
            # Veritabanında güncellemeleri kaydet
            db.session.commit()
            flash('Profil başarıyla güncellendi!', category='success')
        except Exception as e:
            db.session.rollback()  # Hata durumunda değişiklikleri geri al
            flash('Bir hata oluştu. Lütfen tekrar deneyin.', category='error')

        return redirect(url_for('views.profil'))

    # Fotoğraf seçenekleri
    photos = ["default.png", "photo1.png", "photo2.png", "photo3.png", "photo4.png", "photo5.png", "photo6.png"]

    return render_template('edit_profile.html', user=user, photos=photos)




app = Flask(__name__)

@views.route('/update_score', methods=['POST'])
def update_score():
    if request.method == 'POST':
        data = request.get_json()
        total_score = data.get('total_score')
        
        # Kullanıcının total_score değerini güncelle
        user = User.query.get(current_user.id)
        if user:
            user.total_score = total_score
            db.session.commit()
            return jsonify({"status": "success", "total_score": total_score})
        else:
            return jsonify({"status": "error", "message": "User not found"}), 404






