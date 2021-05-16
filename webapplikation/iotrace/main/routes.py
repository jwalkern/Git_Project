import os
import datetime
import json
from flask import Blueprint, render_template, url_for, flash, redirect
from flask_login import login_required, current_user
from flask_admin.contrib.sqla import ModelView
from iotrace import db, admin
from iotrace.models import User, Device, DeviceData, TrackingDeviceTrigger, Xtel
from iotrace.main.forms import GenerateTrackingDeviceData

main = Blueprint('main', __name__)


class Admin_Model_View(ModelView):
    def is_accessible(self):
        if current_user.id == 1:
            return True
        else:
            return False
admin.add_view(Admin_Model_View(User, db.session))
admin.add_view(Admin_Model_View(Device, db.session))
admin.add_view(Admin_Model_View(DeviceData, db.session))
admin.add_view(Admin_Model_View(TrackingDeviceTrigger, db.session))
admin.add_view(Admin_Model_View(Xtel, db.session))

#Dette er vores startside og viser index.html 
@main.route('/')
@main.route(('/home'))
def home(methods=['GET', 'POST']):    
    if current_user.is_authenticated:
        return redirect(url_for('devices.curl_dashboard'))
    return redirect(url_for('accounts.login'))




