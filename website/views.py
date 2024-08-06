from flask import Blueprint, render_template, request, jsonify, flash
from flask_login import login_required, current_user
from .models import BeignDataset, GeneratedDataDataset, MaliciousDataset
from . import db
import random
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import pandas as pd
import json
import mysql.connector



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

@views.route('/final-step')
def final_step():
    return render_template('final_step.html')

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

