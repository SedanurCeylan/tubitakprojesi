from datetime import datetime
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
'''from .main import db'''

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    profile_picture = db.Column(db.String(150), default='default.png')
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    notes = db.relationship('Note')
    total_score = db.Column(db.Integer, default=0)



from . import db

class BeignDataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_orig_h = db.Column(db.String(50))
    id_resp_h = db.Column(db.String(50))
    id_resp_p = db.Column(db.String(50))
    proto = db.Column(db.String(50))
    duration = db.Column(db.Float)
    orig_bytes = db.Column(db.Float)
    resp_bytes = db.Column(db.String(50))
    history = db.Column(db.String(50))
    orig_pkts = db.Column(db.Float)
    orig_ip_bytes = db.Column(db.Float)
    resp_pkts = db.Column(db.Float)
    malware_status = db.Column(db.String(50))

class GeneratedDataDataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_orig_h = db.Column(db.String(50))
    id_resp_h = db.Column(db.String(50))
    id_resp_p = db.Column(db.String(50))
    proto = db.Column(db.String(50))
    duration = db.Column(db.Float)
    orig_bytes = db.Column(db.Float)
    resp_bytes = db.Column(db.String(50))
    history = db.Column(db.String(50))
    orig_pkts = db.Column(db.Float)
    orig_ip_bytes = db.Column(db.Float)
    resp_pkts = db.Column(db.Float)
    malware_status = db.Column(db.String(50))

class MaliciousDataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_orig_h = db.Column(db.String(50))
    id_resp_h = db.Column(db.String(50))
    id_resp_p = db.Column(db.String(50))
    proto = db.Column(db.String(50))
    duration = db.Column(db.Float)
    orig_bytes = db.Column(db.Float)
    resp_bytes = db.Column(db.String(50))
    history = db.Column(db.String(50))
    orig_pkts = db.Column(db.Float)
    orig_ip_bytes = db.Column(db.Float)
    resp_pkts = db.Column(db.Float)
    malware_status = db.Column(db.String(50))

class AnalysisResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accuracy = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Dataset {self.id}>'
