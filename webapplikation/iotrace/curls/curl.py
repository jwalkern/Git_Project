import os
import requests
import json
import io
import base64
from flask import Blueprint, current_app
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from iotrace import googlemaps
from iotrace.models import DeviceData
from flask_googlemaps import Map

curls = Blueprint('curls', __name__)

def curl_device_temp(device_data, numbers_of_iteration=125):
	test = device_data
	loop = True
	while loop:
		try:
			time = []
			temp = []
			for i in range(len(device_data)):
				time.insert(0,device_data[i].timestamp.strftime('%Y-%d-%m'))
				temp.insert(0,device_data[i].temp)
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
			
			loop = False
		except:
			numbers_of_iteration = numbers_of_iteration - 1
			if numbers_of_iteration == -1:
				loop = False
	return PNG

def curl_device_humid(device_data, numbers_of_iteration=125):
	test = device_data
	loop = True
	while loop:
		try:
			time = []
			humid = []
			# Fetching data
			for i in range(len(device_data)):
				time.insert(0,device_data[i].timestamp.strftime('%d-%m'))
				humid.insert(0,device_data[i].humid)
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
			loop = False
		except:
			numbers_of_iteration = numbers_of_iteration - 1
			if numbers_of_iteration == -1:
				loop = False
	return PNG

def curl_device_hpa(device_data, numbers_of_iteration=125):
	test = device_data
	loop = True
	while loop:
		try:
			time = []
			hpa = []
			# Fetching data
			for i in range(len(device_data)):
				time.insert(0,device_data[i].timestamp.strftime('%d-%m'))
				hpa.insert(0,device_data[i].hpa)
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
			loop = False
		except:
			numbers_of_iteration = numbers_of_iteration - 1
			if numbers_of_iteration == -1:
				loop = False
	return PNG

def curl_device_volt(device_data, numbers_of_iteration=125):
	test = device_data
	loop = True
	while loop:
		try:
			time = []
			volt = []
			# Fetching data
			for i in range(len(device_data)):
				time.insert(0,device_data[i].timestamp.strftime('%d-%m'))
				volt.insert(0,device_data[i].volt)
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
			loop = False
		except:
			numbers_of_iteration = numbers_of_iteration - 1
			if numbers_of_iteration == -1:
				loop = False
	return PNG


def curl_device_lte_rssi(device_data, numbers_of_iteration=125):
	test = device_data
	loop = True
	while loop:
		try:
			time = []
			lte_rssi = []
			# Fetching data
			for i in range(len(device_data)):
				time.insert(0,device_data[i].timestamp.strftime('%d-%m'))
				lte_rssi.insert(0,device_data[i].lte_rssi)
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
			loop = False
		except:
			numbers_of_iteration = numbers_of_iteration - 1
			if numbers_of_iteration == -1:
				loop = False
	return PNG

def curl_device_alarm1(device_data, numbers_of_iteration=125):
	loop = True
	while loop:
		try:
			time = []
			alarm = []
			# Fetching data
			for i in range(len(device_data)):
				time.insert(0,device_data[i].timestamp.strftime('%d-%m'))
				alarm.insert(0,device_data[i].alarm_1)
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
			loop = False
		except:
			numbers_of_iteration = numbers_of_iteration - 1
			if numbers_of_iteration == -1:
				loop = False
	return PNG

def curl_device_alarm2(device_data, numbers_of_iteration=125):
	loop = True
	while loop:
		try:
			time = []
			alarm = []
			# Fetching data
			for i in range(len(device_data)):
				time.insert(0,device_data[i].timestamp.strftime('%d-%m'))
				alarm.insert(0,device_data[i].alarm_2)
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
			loop = False
		except:
			numbers_of_iteration = numbers_of_iteration - 1
			if numbers_of_iteration == -1:
				loop = False
	return PNG 	 

def curl_device_pos(device, device_data):
	NULL = None
	LatDec = ''
	LngDec = ''
	count = 0
	label = device.devicename
	icon = "http://maps.google.com/mapfiles/ms/icons/green-dot.png"
	for item in device_data:
		try:
			if item.geo != '':
				Lat = item.geo.split(',')[1].translate({ord(i): None for i in 'NS'})
				LAT_DD = int(float(Lat)/100)
				LAT_SS = float(Lat) - LAT_DD * 100
				LatDec = LAT_DD + LAT_SS/60
				if item.geo.find("S") != -1:
					LatDec = LatDec * -1

				Lng = item.geo.split(',')[2].translate({ord(i): None for i in 'EW'})
				LNG_DD = int(float(Lng)/100)
				LNG_SS = float(Lng) - LNG_DD * 100
				LngDec = LNG_DD + LNG_SS/60
				if item.geo.find("W") != -1:
					LngDec = LngDec * -1
				if count > 10:
					icon = "http://maps.google.com/mapfiles/ms/icons/red-dot.png"
					label = item.timestamp.strftime('%d-%m-%Y')

				break
			else:
				count = count + 1
		except:
			count = count + 1

	pos = f'lat:{LatDec}, lng:{LngDec}'
	GOOGLEMAPS_KEY =  current_app.config['GOOGLEMAPS_KEY']	
	return pos, label, icon, GOOGLEMAPS_KEY



def curl_all_device_pos(devices):
	device_pos = []
	device_data = {}
	for device in devices:
		device_data[str(device.device_mac)] = DeviceData.query.filter_by(device_mac=device.device_mac).order_by(DeviceData.timestamp.desc()).all()
		count = 0
		icon = "http://maps.google.com/mapfiles/ms/icons/green-dot.png"
		if device.devicetype != 'fire':
			for item in device_data[str(device.device_mac)]:
				try:
					if item.geo != '':
						Lat = item.geo.split(',')[1].translate({ord(i): None for i in 'NS'})
						LAT_DD = int(float(Lat)/100)
						LAT_SS = float(Lat) - LAT_DD * 100
						LatDec = LAT_DD + LAT_SS/60
						if item.geo.find("S") != -1:
							LatDec = LatDec * -1

						Lng = item.geo.split(',')[2].translate({ord(i): None for i in 'EW'})
						LNG_DD = int(float(Lng)/100)
						LNG_SS = float(Lng) - LNG_DD * 100
						LngDec = LNG_DD + LNG_SS/60
						if item.geo.find("W") != -1:
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
				except:
					count = count + 1
		else:
			continue
	GOOGLEMAPS_KEY = current_app.config['GOOGLEMAPS_KEY']
	return device_data, device_pos, GOOGLEMAPS_KEY
