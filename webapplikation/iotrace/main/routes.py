import os
import datetime
import json
from flask import Blueprint, render_template, url_for, flash, redirect
from flask_login import login_required, current_user
from flask_admin.contrib.sqla import ModelView
from iotrace import db, admin
from iotrace.models import User, Device, TrackingDeviceData, FireDeviceData
from iotrace.main.forms import GenerateTrackingDeviceData

main = Blueprint('main', __name__)


class Admin_Model_View(ModelView):
    def is_accessible(self):
        return True
admin.add_view(Admin_Model_View(User, db.session))
admin.add_view(Admin_Model_View(Device, db.session))
admin.add_view(Admin_Model_View(TrackingDeviceData, db.session))

#Dette er vores startside og viser index.html 
@main.route('/')
@main.route(('/home'))
def home(methods=['GET', 'POST']):    
    if current_user.is_authenticated:
        return redirect(url_for('devices.dashboard'))
    return redirect(url_for('accounts.login'))


@main.route('/generate/data', methods=['GET', 'POST'])
def dummy():
    
    form = GenerateTrackingDeviceData()
    if form.validate_on_submit():
        device = Device.query.filter_by(device_mac=form.device_mac.data).first()
        if form.devicetype.data != 'fire':
            with open("D:/Git_projects/iotrace/datadump/Xtel16.txt") as obj:
                file = obj.read()
            js = json.loads(file)
            for item in js:
                timestamp = datetime.datetime.strptime(item['ts'].translate({ord(i): None for i in 'TZ'}), '%Y-%m-%d%H:%M:%S.%f')
                pos = item['data']['pos']
                temp = item['data']['temp']
                humid = item['data']['humid']
                hpa = item['data']['hpa']
                volt = item['data']['volt']
                lte_rssi = item['data']['lte_rssi']
                pos = item['data']['pos']
                device_id = device.id
                data = TrackingDeviceData(device_id=device_id, timestamp=timestamp, pos=pos, temp=temp, humid=humid, hpa=hpa, volt=volt, lte_rssi=lte_rssi)
                db.session.add(data)
            db.session.commit()
            flash('Data generated!', 'success')
        elif form.devicetype.data == 'fire':
            with open("D:/Git_projects/iotrace/datadump/brandalarm1.txt") as obj:
                file = obj.read()
            js = json.loads(file)
            for item in js:
                timestamp = datetime.datetime.strptime(item['ts'].translate({ord(i): None for i in 'TZ'}), '%Y-%m-%d%H:%M:%S.%f')
                volt = item['data']['volt']
                alarm_1 = item['data']['alarm_1']
                alarm_2 = item['data']['alarm_2']
                lte_rssi = item['data']['lte_rssi']                
                device_id = device.id
                data = FireDeviceData(device_id=device_id, timestamp=timestamp, alarm_1=alarm_1, alarm_2=alarm_2, volt=volt, lte_rssi=lte_rssi)
                db.session.add(data)
            db.session.commit()
            flash('Data generated!', 'success')
        else:
            pass  
    return render_template('dummy_data.html', title='GDD', form=form) 

