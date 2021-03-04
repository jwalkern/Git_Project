from datetime import datetime
from webapp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    devices = db.relationship('Device', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    datadumps = db.relationship('Dummydata', backref='devicedata', lazy=True)
    
    
    def __repr__(self):
        return f"Device('{self.device_name}')"
    
class Dummydata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    pos = db.Column(db.String(100), nullable=False)
    temp = db.Column(db.Integer, nullable=False)
    humid = db.Column(db.Integer, nullable=False)
    hpa = db.Column(db.Integer, nullable=False)
    volt = db.Column(db.Integer, nullable=False)
    lte_rssi = db.Column(db.Integer, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    
    def __repr__(self):
        return f"Dummydata('{self.timestamp}', '{self.pos}', '{self.temp}', '{self.humid}', '{self.hpa}', '{self.volt}', '{self.lte_rssi}')"
    