# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 11:04:16 2020

@author: JaMiBiCh
"""

import socket


def ipaddress():
    IP = "8.8.8.8"      
   
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((IP, 0))
    ipaddr = s.getsockname()[0]    
    s.close()
    
    return ipaddr


    


