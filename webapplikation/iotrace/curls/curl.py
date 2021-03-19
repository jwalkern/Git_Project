import os
import requests
import json
from flask import Blueprint

curls = Blueprint('curls', __name__)

def get_data(device_mac):
	url = 'https://cloud.moviot.dk/web/logs/' + device_mac
	myToken = os.environ.get('XTEL_TOKEN')
	head = {"Authorization":"Token {}".format(myToken)}
	r = requests.get(url, headers=head)
	return r

def curl_all_device_data(devices):
	device_pos = []
	for device in devices:
		mac_addr = str(device.device_mac)
		count = 0
		icon = "http://maps.google.com/mapfiles/ms/icons/green-dot.png"
		if device.devicetype != 'fire':

			obj = get_data(mac_addr)
			collect_byte = []
			for item in obj:    
				collect_byte.append(item.decode('utf-8'))
			single_sting="".join(collect_byte)
			res = json.loads(single_sting)
			for item in res:
				if item['data']['pos'] != '':
					Lat = item['data']['pos'].split(',')[1].translate({ord(i): None for i in 'NS'})
					LAT_DD = int(float(Lat)/100)
					LAT_SS = float(Lat) - LAT_DD * 100
					LatDec = LAT_DD + LAT_SS/60
					if item['data']['pos'].find("S") != -1:
						LatDec = LatDec * -1

					Lng = item['data']['pos'].split(',')[2].translate({ord(i): None for i in 'EW'})
					LNG_DD = int(float(Lng)/100)
					LNG_SS = float(Lng) - LNG_DD * 100
					LngDec = LNG_DD + LNG_SS/60
					if item['data']['pos'].find("W") != -1:
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
	GOOGLEMAPS_KEY = os.environ.get('GOOGLEMAPS_KEY')
	return device_pos, GOOGLEMAPS_KEY
