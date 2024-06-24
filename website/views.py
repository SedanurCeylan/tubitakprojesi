from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import pandas as pd
import random

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

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

@views.route('/start-test')
def start_test():
    return render_template('test_page.html')

@views.context_processor
def inject_user():
    return {'user': current_user}

# CSV dosyalarını yükle
df_malicious = pd.read_csv(r"C:\Users\sdnrc\Desktop\csvler\zararli.csv", delimiter=';')
df_benign = pd.read_csv(r"C:\Users\sdnrc\Desktop\csvler\zararsiz.csv", delimiter=';')

@views.route('/malicious')
def malicious():
    sample_data = df_malicious.sample(20)
    title = "Zararlı Verilerin Detayları"
    return render_template('data_display.html', data=sample_data.to_html(classes='data-table', index=False, escape=False), title=title)

@views.route('/benign')
def benign():
    sample_data = df_benign.sample(20)
    title = "Zararsız Verilerin Detayları"
    return render_template('data_display.html', data=sample_data.to_html(classes='data-table', index=False, escape=False), title=title)

@views.route('/next-page')
def next_page():
    sample_malicious = df_malicious.sample(10).to_dict(orient='records')
    sample_benign = df_benign.sample(10).to_dict(orient='records')

    for row in sample_malicious:
        row['source'] = 'malicious'
    for row in sample_benign:
        row['source'] = 'benign'
    
    mixed_samples = sample_malicious + sample_benign
    random.shuffle(mixed_samples)

    return render_template('next_page.html', data=mixed_samples)

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

@views.route('/final-step')
def final_step():
    return render_template('final_step.html')

@views.route('/quiz')
@login_required
def quiz():
    return render_template('quiz.html')

@views.route('/senaryo1')
@login_required
def senaryo1():
    return render_template('senaryo1.html')  # Senaryo 1'e özel içerik

@views.route('/senaryo2')
@login_required
def senaryo2():
    return render_template('senaryo2.html')  # Senaryo 2'ye özel içerik

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