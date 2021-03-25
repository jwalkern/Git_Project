import os
import io
import base64
from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from iotrace import googlemaps
from flask_googlemaps import Map
from iotrace.models import Device, TrackingDeviceData 

plots = Blueprint('plots', __name__)

def device_temp(data_trackingdevice):
	time = []
	temp = []
	for item in data_trackingdevice:
		time.insert(0,item.timestamp.strftime('%d-%m-%Y'))
		temp.insert(0,item.temp)
	# Generate plot
	fig = Figure()
	axis = fig.add_subplot(1,1,1)
	axis.set_title("Device Temperatur")
	axis.set_ylabel("Temperatur")
	axis.plot(time, temp)
	# Convert plot to PNG image
	pngImage = io.BytesIO()
	FigureCanvas(fig).print_png(pngImage)
	# Encode PNG image to base64 string
	PNG = "data:image/png;base64,"
	PNG += base64.b64encode(pngImage.getvalue()).decode('utf8')
	return PNG

def device_humid(data_trackingdevice):
	time = []
	humid = []
	# Fetching data
	for item in data_trackingdevice:
		time.insert(0,item.timestamp.strftime('%d-%m-%Y'))
		humid.insert(0,item.humid)
	# Generate plot
	fig = Figure()
	axis = fig.add_subplot(1,1,1)
	axis.set_title("Device Humidity")
	axis.set_ylabel("Humidity")
	axis.plot(time, humid)
	# Convert plot to PNG image
	pngImage = io.BytesIO()
	FigureCanvas(fig).print_png(pngImage)
	# Encode PNG image to base64 string
	PNG = "data:image/png;base64,"
	PNG += base64.b64encode(pngImage.getvalue()).decode('utf8')
	return PNG

def device_hpa(data_trackingdevice):
	time = []
	hpa = []
	# Fetching data
	for item in data_trackingdevice:
		time.insert(0,item.timestamp.strftime('%d-%m-%Y'))
		hpa.insert(0,item.hpa)
	# Generate plot
	fig = Figure()
	axis = fig.add_subplot(1,1,1)
	axis.set_title("Device Air pressure")
	axis.set_ylabel("hPa")
	axis.plot(time, hpa)
	# Convert plot to PNG image
	pngImage = io.BytesIO()
	FigureCanvas(fig).print_png(pngImage)
	# Encode PNG image to base64 string
	PNG = "data:image/png;base64,"
	PNG += base64.b64encode(pngImage.getvalue()).decode('utf8')
	return PNG

def device_volt(data_trackingdevice):
	time = []
	volt = []
	# Fetching data
	for item in data_trackingdevice:
		time.insert(0,item.timestamp.strftime('%d-%m-%Y'))
		volt.insert(0,item.volt)
	# Generate plot
	fig = Figure()
	axis = fig.add_subplot(1,1,1)
	axis.set_title("Device Voltage")
	axis.set_ylabel("Voltage")
	axis.plot(time, volt)
	# Convert plot to PNG image
	pngImage = io.BytesIO()
	FigureCanvas(fig).print_png(pngImage)
	# Encode PNG image to base64 string
	PNG = "data:image/png;base64,"
	PNG += base64.b64encode(pngImage.getvalue()).decode('utf8')
	return PNG


def device_lte_rssi(data_trackingdevice):
	time = []
	lte_rssi = []
	# Fetching data
	for item in data_trackingdevice:
		time.insert(0,item.timestamp.strftime('%d-%m-%Y'))
		lte_rssi.insert(0,item.lte_rssi)
	# Generate plot
	fig = Figure()
	axis = fig.add_subplot(1,1,1)
	axis.set_title("Device Signal Strength")
	axis.set_ylabel("LTE RSSI")
	axis.plot(time, lte_rssi)
	# Convert plot to PNG image
	pngImage = io.BytesIO()
	FigureCanvas(fig).print_png(pngImage)
	# Encode PNG image to base64 string
	PNG = "data:image/png;base64,"
	PNG += base64.b64encode(pngImage.getvalue()).decode('utf8')
	return PNG

def device_alarm1(data_firedevice):
	time = []
	alarm = []
	# Fetching data
	for item in data_firedevice:
		time.insert(0,item.timestamp.strftime('%d-%m-%Y'))
		alarm.insert(0,item.alarm_1)
	# Generate plot
	fig = Figure()
	axis = fig.add_subplot(1,1,1)
	axis.set_title("Alarm 1")
	axis.set_ylabel("True/False")
	axis.plot(time, alarm)
	# Convert plot to PNG image
	pngImage = io.BytesIO()
	FigureCanvas(fig).print_png(pngImage)
	# Encode PNG image to base64 string
	PNG = "data:image/png;base64,"
	PNG += base64.b64encode(pngImage.getvalue()).decode('utf8')
	return PNG

def device_alarm2(data_firedevice):
	time = []
	alarm = []
	# Fetching data
	for item in data_firedevice:
		time.insert(0,item.timestamp.strftime('%d-%m-%Y'))
		alarm.insert(0,item.alarm_2)
	# Generate plot
	fig = Figure()
	axis = fig.add_subplot(1,1,1)
	axis.set_title("Alarm 2")
	axis.set_ylabel("True/False")
	axis.plot(time, alarm)
	# Convert plot to PNG image
	pngImage = io.BytesIO()
	FigureCanvas(fig).print_png(pngImage)
	# Encode PNG image to base64 string
	PNG = "data:image/png;base64,"
	PNG += base64.b64encode(pngImage.getvalue()).decode('utf8')
	return PNG 	 

def device_pos(device):
	LatDec = ''
	LngDec = ''
	count = 0
	label = device.devicename
	icon = "http://maps.google.com/mapfiles/ms/icons/green-dot.png"
	for item in device.data_trackingdevice:
		if item.pos != '':
			Lat = item.pos.split(',')[1].translate({ord(i): None for i in 'NS'})
			LAT_DD = int(float(Lat)/100)
			LAT_SS = float(Lat) - LAT_DD * 100
			LatDec = LAT_DD + LAT_SS/60
			if item.pos.find("S") != -1:
				LatDec = LatDec * -1

			Lng = item.pos.split(',')[2].translate({ord(i): None for i in 'EW'})
			LNG_DD = int(float(Lng)/100)
			LNG_SS = float(Lng) - LNG_DD * 100
			LngDec = LNG_DD + LNG_SS/60
			if item.pos.find("W") != -1:
				LngDec = LngDec * -1
			if count > 10:
				icon = "http://maps.google.com/mapfiles/ms/icons/red-dot.png"
				label = item.timestamp.strftime('%d-%m-%Y')

			break
		else:
			count = count + 1

	pos = f'lat:{LatDec}, lng:{LngDec}'
	GOOGLEMAPS_KEY =  current_app.config['GOOGLEMAPS_KEY']	
	return pos, label, icon, GOOGLEMAPS_KEY

def all_device_pos(devices):
	device_pos = []
	for device in devices:
		count = 0
		icon = "http://maps.google.com/mapfiles/ms/icons/green-dot.png"
		if device.devicetype != 'fire':
			for item in device.data_trackingdevice:
				if item.pos != '':
					Lat = item.pos.split(',')[1].translate({ord(i): None for i in 'NS'})
					LAT_DD = int(float(Lat)/100)
					LAT_SS = float(Lat) - LAT_DD * 100
					LatDec = LAT_DD + LAT_SS/60
					if item.pos.find("S") != -1:
						LatDec = LatDec * -1

					Lng = item.pos.split(',')[2].translate({ord(i): None for i in 'EW'})
					LNG_DD = int(float(Lng)/100)
					LNG_SS = float(Lng) - LNG_DD * 100
					LngDec = LNG_DD + LNG_SS/60
					if item.pos.find("W") != -1:
						LngDec = LngDec * -1

					pos = f'lat:{LatDec}, lng:{LngDec}'
					label = device.devicename
					if count > 10:
						icon = "http://maps.google.com/mapfiles/ms/icons/red-dot.png"
						label = item.timestamp.strftime('%d-%m-%Y')

					device_pos.append([pos, label, icon])
					break
				else:
					count = count + 1
		else:
			continue
	GOOGLEMAPS_KEY = current_app.config['GOOGLEMAPS_KEY']
	return device_pos, GOOGLEMAPS_KEY

