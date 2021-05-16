import os
from flask import Blueprint, render_template, redirect, request, abort, flash, url_for
from flask_login import login_required, current_user
from iotrace import db
from iotrace.models import Device, DeviceData, TrackingDeviceTrigger, Xtel
from iotrace.devices.forms import CreateDeviceForm, EditDeviceForm
from iotrace.plots.plot import device_temp, device_humid, device_hpa, device_volt, device_lte_rssi, device_pos, all_device_pos, device_alarm1, device_alarm2
from iotrace.curls.curl import curl_all_device_pos, curl_device_temp, curl_device_humid, curl_device_hpa, curl_device_volt, curl_device_lte_rssi, curl_device_pos, curl_device_alarm1, curl_device_alarm2

devices = Blueprint('devices', __name__)

@devices.route('/dashboard')
@login_required
def curl_dashboard():
    devices = Device.query.filter_by(user_id=current_user.id).order_by(Device.devicetype.desc())
    device_data, all_device, GOOGLEMAPS_KEY = curl_all_device_pos(devices)
    return render_template('devices/NEWdashboard.html',  title='Dashboard', devices=devices, GOOGLEMAPS_KEY=GOOGLEMAPS_KEY, all_device=all_device, device_data=device_data)

@devices.route('/dashboard/device/data/<device_id>')
@login_required
def curl_device(device_id):
    device = Device.query.get_or_404(device_id)
    if current_user != device.owner:
        abort(403)
    data = DeviceData.query.filter_by(device_mac=device.device_mac).order_by(DeviceData.timestamp.desc()).all()
    if device.devicetype != 'fire':
        temp = curl_device_temp(data)
        humid = curl_device_humid(data)
        hpa = curl_device_hpa(data)
        volt = curl_device_volt(data)
        lte_rssi = curl_device_lte_rssi(data)
        pos, label, icon, GOOGLEMAPS_KEY= curl_device_pos(device, data)
        return render_template('devices/NEWdevice.html', title=device.devicename, device=device, data=data, device_data=device.data_device, temp=temp, humid=humid, hpa=hpa, volt=volt, lte_rssi=lte_rssi, pos=pos, icon=icon, label=label, GOOGLEMAPS_KEY=GOOGLEMAPS_KEY)

    elif device.devicetype == 'fire':
        alarm_1 = curl_device_alarm1(data)
        alarm_2 = curl_device_alarm2(data)
        volt = curl_device_volt(data)
        lte_rssi = curl_device_lte_rssi(data)       
        return render_template('devices/NEWdevice.html', title=device.devicename, device=device, data=data, device_data=device.data_device, alarm_1=alarm_1, alarm_2=alarm_2, volt=volt, lte_rssi=lte_rssi)

@devices.route('/dashboard/device/new', methods=['GET', 'POST'])
@login_required
def add_device():
    form = CreateDeviceForm()
    if form.validate_on_submit():
        dev = Xtel.query.filter_by(device_mac=form.device_mac.data).first()
        device = Device(device_mac=form.device_mac.data ,devicename=form.devicename.data, devicetype=dev.devicetype, owner=current_user)
        db.session.add(device)
        db.session.commit()
        flash('The device have been added!', 'success')
        return redirect(url_for('devices.curl_dashboard'))
    return render_template('devices/add_device.html', title='Add Device', form=form)

@devices.route('/dashboard/device/edit/<device_id>', methods=['GET', 'POST'])
@login_required
def edit_device(device_id):
    device = Device.query.get_or_404(device_id)
    if device.owner != current_user:
        abort(403)
    value = TrackingDeviceTrigger.query.filter_by(device_id=device.id).first()
    form = EditDeviceForm()
    if value:       
        if form.validate_on_submit():
            device.devicename = form.devicename.data
            value.mintemp = form.mintemp.data
            value.maxtemp = form.maxtemp.data
            value.minhumid = form.minhumid.data
            value.maxhumid = form.maxhumid.data
            value.minhpa = form.minhpa.data
            value.maxhpa = form.maxhpa.data
            db.session.commit()
            flash('Your device has been updated', 'success')
            return redirect(url_for('devices.curl_device', device_id=device.id))
        elif request.method == 'GET':
            form.devicename.data = device.devicename
            form.mintemp.data = value.mintemp
            form.maxtemp.data = value.maxtemp
            form.minhumid.data = value.minhumid
            form.maxhumid.data = value.maxhumid
            form.minhpa.data = value.minhpa
            form.maxhpa.data = value.maxhpa
        return render_template('devices/edit_device.html', title='Update Device', form=form, device=device)
    else:    
        if form.validate_on_submit():
            device.devicename = form.devicename.data
            value = TrackingDeviceTrigger(device_id=device.id ,mintemp=form.mintemp.data, maxtemp=form.maxtemp.data, minhumid=form.minhumid.data, maxhumid=form.maxhumid.data, minhpa=form.minhpa.data, maxhpa=form.maxhpa.data)
            db.session.add(value)
            db.session.commit()
            flash('The values have been added', 'success')
            return redirect(url_for('devices.curl_device', device_id=device.id))
        elif request.method == 'GET':
            form.devicename.data = device.devicename
        return render_template('devices/edit_device.html', title='Update Device', form=form, device=device)



@devices.route('/dashboard/device/delete/<device_id>', methods=['POST'])
@login_required
def delete_device(device_id):
    device = Device.query.get_or_404(device_id)
    if device.owner != current_user:
        abort(403)
    db.session.delete(device)
    db.session.commit()
    flash('Your device has been deleted!', 'success')
    return redirect(url_for('devices.curl_dashboard'))
