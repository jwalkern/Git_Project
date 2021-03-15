from datetime import datetime
from flask import current_app
from flask_admin.contrib.sqla import ModelView
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from iotrace import db, login_manager
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
    devices = db.relationship('Device', cascade='all, delete-orphan', backref='owner', lazy=True)
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    devicename = db.Column(db.String(100), nullable=False)
    devicetype = db.Column(db.String(100), nullable=False)
    device_mac = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    data_trackingdevice = db.relationship('TrackingDeviceData', cascade='all, delete-orphan', backref='ref_trackingdevice', lazy=True)
    data_firedevice = db.relationship('FireDeviceData', cascade='all, delete-orphan', backref='ref_firedevice', lazy=True)
    
    
    def __repr__(self):
        return f"Device('{self.id}', '{self.devicetype}', '{self.device_mac}')"
    
class TrackingDeviceData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    pos = db.Column(db.String(100), nullable=True)
    temp = db.Column(db.Integer, nullable=True)
    humid = db.Column(db.Integer, nullable=True)
    hpa = db.Column(db.Integer, nullable=True)
    volt = db.Column(db.Integer, nullable=True)
    lte_rssi = db.Column(db.Integer, nullable=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    
    def __repr__(self):
        return f"TrackingDeviceData('{self.timestamp}', '{self.pos}', '{self.temp}', '{self.humid}', '{self.hpa}', '{self.volt}', '{self.lte_rssi}')"
   
class FireDeviceData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    alarm_1 = db.Column(db.Boolean, nullable=True)
    alarm_2 = db.Column(db.Boolean, nullable=True)
    volt = db.Column(db.Integer, nullable=True)
    lte_rssi = db.Column(db.Integer, nullable=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)

    def __repr__(self):
        return f"FireDeviceData('{self.timestamp}', '{self.alarm_1}', '{self.alarm_2}', '{self.volt}', '{self.lte_rssi}')"
