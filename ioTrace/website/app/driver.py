# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 11:04:16 2020

@author: JaMiBiCh
"""
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
import socket
import nmap3


def ipaddress():
    IP = "8.8.8.8"      
   
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((IP, 0))
    ipaddr = s.getsockname()[0]    
    s.close()
    
    return ipaddr

def nmap_scan():
    """
    funktionen laver et socket bind, for at få host ip adressen.
    Dette bruger nmap til at scanne hele netværket.
    Scaning resultat returneres i en xml fil.
    """
    ipaddr = ipaddress()
    
    print ("Target for scan:", ipaddr+"/24")
    print("nmap scan running")
    
    nmap = nmap3.Nmap()
    nmap_command = nmap.run_command(["nmap", "-O" ,"-Pn", "-sV", "-sS", "-oX", "/home/pi/vulnerScan/website/app/static/files/result.xml",
                                     "--script=nmap-vulners", "-p21,22,23,25,80,111,135,139,445,3389 ", str(ipaddr)+"/24"])    
    print("nmap scan complete")
    
    file = '/home/pi/vulnerScan/website/app/static/files/result.xml'
    
    return file

def xml_reader(file):
    """
    1. funktionen indlæser xml filen der returneres af nmap_scan()
    2. den bruger xml root tag for at ittere igennem host tagget.
    3. Her bearbejder den specifikke attributer f.eks. address, port, protocol, state og script.
    4. Deler script attributten op i exploit og aktive exploit.
    5. Attributterne samles i en dictonary som returneres.
    """
    ipaddr = ipaddress()    
#1
    with open(file, "r") as f:
        scan_result = f.read()
    
    try:
        xml_str = str(scan_result)
        root = ET.fromstring(xml_str)
    
    except ParseError as e:
        print(e)
#2
    tag = root.tag
    hosts = []

#3    
    for host in root.findall('host'):
        details = {'address':host.find('address').attrib.get('addr')}
        port_list = []
        ports = host.find("ports")
        
        if details['address'] == ipaddr:
            continue
        
        for port in ports:
            port_details={'port':port.attrib.get('portid'),
                          'protocol':port.attrib.get('protocol')}
            service = port.find('service')
            state = port.find('state')
            script = port.findall('script')
            
            if service is not None:
                port_details.update({'service':service.attrib.get('name'), 
                                     'product':service.attrib.get('product',''),
                                     'version':service.attrib.get('version',''),
                                     'extrainfo':service.attrib.get('extrainfo',''),
                                     'ostype':service.attrib.get('ostype','')})
            if state is not None:
                port_details.update({'state':state.attrib.get('state'),
                                     'reason':state.attrib.get('reason', '')})
#4
            if script is not None:
                for item in script:
                   port_details.update({'id':item.attrib.get('id', ''),
                                        'output':item.attrib.get('output', '')})   
                   
                   exploits = []
                   active_exploits = []
                   vulners = item.attrib.get('id')
                   
                   if vulners == 'vulners':
                       for elem in item.iter('elem'):
                           is_exploit = elem.text
                           if is_exploit == 'true':
                               active_exploits.append(1)
                           if is_exploit == 'false':
                               exploits.append(1)
                                                     
                   elif vulners != 'vulners':
                       elem = item.findall('elem')
                       table = item.findall('table')
                       for item in elem:
                           exploits.append(1)
                       for item in table:
                           exploits.append(1)
                           
                   port_details.update({'exploits:': sum(exploits),
                                        'active exploits:': sum(active_exploits)})
               
            if port_details['port'] is not None:
                port_list.append(port_details)
#5      
        details['ports']=port_list
        hosts.append(details)
        
    return hosts
    
    


