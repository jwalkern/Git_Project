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
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    logo_file = db.Column(db.String(20), nullable=False, default='ioTrace.jpg')
    role = db.Column(db.String(6), nullable=False, default='user')
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
    device_mac = db.Column(db.String(20), unique=True, nullable=False)
    devicetype = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    data_device = db.relationship('DeviceData', cascade='all, delete-orphan', backref='ref_data_device', lazy=True)
    trigger_trackingdevice = db.relationship('TrackingDeviceTrigger', cascade='all, delete-orphan', backref='ref_trig_track', lazy=True)
  
    
    def __repr__(self):
        return f"Device('{self.id}', '{self.devicetype}', '{self.device_mac}')"
    
class DeviceData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=True)
    geo = db.Column(db.String(100), nullable=True)
    temp = db.Column(db.Integer, nullable=True)
    humid = db.Column(db.Integer, nullable=True)
    hpa = db.Column(db.Integer, nullable=True)
    volt = db.Column(db.Integer, nullable=True)
    lte_rssi = db.Column(db.Integer, nullable=True)
    alarm_1 = db.Column(db.Boolean, nullable=True)
    alarm_2 = db.Column(db.Boolean, nullable=True)
    device_mac = db.Column(db.String(20), db.ForeignKey('device.device_mac'), nullable=False)
     
    
    def __repr__(self):
        return f"'{self.timestamp}', '{self.geo}', '{self.temp}', '{self.humid}', '{self.hpa}', '{self.volt}', '{self.lte_rssi}','{self.alarm_1}','{self.alarm_2}'"


class TrackingDeviceTrigger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mintemp = db.Column(db.Integer, nullable=True)
    maxtemp = db.Column(db.Integer, nullable=True)
    minhumid = db.Column(db.Integer, nullable=True)
    maxhumid = db.Column(db.Integer, nullable=True)
    minhpa = db.Column(db.Integer, nullable=True)
    maxhpa = db.Column(db.Integer, nullable=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)

    def __repr__(self):
        return f"Trigger('{self.device_id}', '{self.mintemp}', '{self.maxtemp}', '{self.minhumid}', '{self.maxhumid}', '{self.minhpa}', '{self.maxhpa}')"


class Xtel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_mac = db.Column(db.String(20), unique=True, nullable=False)
    devicetype = db.Column(db.String(50), nullable=False)
    
    

    def __repr__(self):
        return f"Info('{self.id}', '{self.device_mac}')"
   

