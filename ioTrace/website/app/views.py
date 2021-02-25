# -*- coding: utf-8 -*-

from flask import render_template, send_file, redirect, url_for
from app import app
import os
import glob
import matplotlib.pyplot as plt
from app import driver
import datetime


#Dette er vores startside og viser index.html 
@app.route('/')
def index():
    
    return render_template('index.html')

#Dette er /result, funktionen genere plots ud fra er xml fil. viser result.html og returner images
@app.route('/result')
def jquery():
    
    hosts = driver.xml_reader('/home/pi/vulnerScan/website/app/static/files/result.xml')
    counter = 0
    
    for host in hosts:
    
        counter += 1
        filePath = f"/home/pi/vulnerScan/website/app/static/images/plot{counter}.png"
        title = host['address']
        
        chartPorts = []
        verifiedExploits = []
        possibleExploits = []
        
        if 'ports' in host:
            for port in host['ports']:
                
                chartPorts.append(port['port'])
                if 'active exploits:' in port:
                    verifiedExploits.append(port['active exploits:'])
                else:
                    verifiedExploits.append(0)
                    
                if 'exploits:' in port:
                    possibleExploits.append(port['exploits:'])
                else:
                    possibleExploits.append(0)
             
        # Generate plot       
        fig, ax = plt.subplots()
        width = 0.35   
        ax.bar(chartPorts, verifiedExploits, width, label='Not confirmed exploits')
        ax.bar(chartPorts, possibleExploits, width, bottom=verifiedExploits,
               label='Exploits')
        
        ax.set_ylabel('Exploits')
        ax.set_title(title)
        
        ax.legend()

        plt.savefig(filePath)
        plt.clf()
    
    images = []
    
    for file in os.listdir('/home/pi/vulnerScan/website/app/static/images'):
        if file.endswith('.png'):
            images.append(os.path.join('/static/images', file))
        else:
            continue   
        
    return render_template('result.html', images=images)

#Dette er /upload, den viser vores download.html
@app.route('/upload')
def upload():
    
    return render_template('download.html')

#Vores download.html sender en fil.
@app.route('/download')
def download_file():
    
    path = '/home/pi/vulnerScan/website/app/static/files/result.xml'
    
    return send_file(path, as_attachment=True)

#Dette er /scan, den viser vores scan.html
@app.route("/scan")
def resultView():
    
    return render_template("scan.html")

#Vores scan.html, aktivere vores nmap_scan() via url_for(scanner) på scan.html siden.
@app.route("/scanner")
def scanner():
    
    files = glob.glob('/home/pi/vulnerScan/website/app/static/images/*.png')
    for i in files:
        os.remove(i)
    
    xmlFile = driver.nmap_scan()
    
    return redirect(url_for('jquery'))


@app.route("/text")
def text_file():
    
    hosts = driver.xml_reader('/home/pi/vulnerScan/website/app/static/files/result.xml')    
    file = '/home/pi/vulnerScan/website/app/static/files/result.txt'
    
    with open(file, "w") as f:	
        
        x = datetime.datetime.now()	
        f.write("The log file was created:\n\n" + str(x.strftime("%b %d %Y %H:%M:%S"))+'\n\n')	
        f.write('---------------------------------------------------------'+'\n')	
        for host in hosts:	
            f.write('IP: '+ str(host.get('address', ''))+'\n')	
            f.write('Services: '+'\n')	
            for port in host['ports']:	
                f.write('\t Service: '+'\n')	
                f.write('\t-----------------------------------'+'\n')	
                for k,v in port.items():	
                    f.write('\t\t'+str(k)+' : '+str(v)+'\n')	
            f.write('---------------------------------------------------------'+'\n') 
        f.close()
    return send_file(file, as_attachment=True)
        
    