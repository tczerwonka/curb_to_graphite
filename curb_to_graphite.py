#!/usr/bin/python3

################################################################################
# curb_to_graphite.py
# https://github.com/tczerwonka/curb_to_graphite
#
# python script to grab data from curb energy thing and push to graphite
#
# T Czerwonka tczerwonka@gmail.com Jan 2021
################################################################################
# requires:
# python3 -m pip install bs4
# python3 -m pip install requests
# python3 -m pip install pandas
# python3 -m pip install lxml
# python3 -m pip install html5lib
################################################################################

import requests
from bs4 import BeautifulSoup
import re
import json
import sys
import time
import os
import platform
from array import array
from socket import socket

CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003
URL = "http://192.168.1.28"
carbondata = []

################################################################################
# graphite setup
################################################################################
sock = socket()
try:
    sock.connect( (CARBON_SERVER,CARBON_PORT) )
except:
    print("Couldn't connect to %(server)s on port %(port)d, is carbon-agent.py running?" % { 'server':CARBON_SERVER, 'port':CARBON_PORT })
    sys.exit(1)


################################################################################

################################################################################
################################################################################

#Tue Jan 19 18:21:18 2021 INFO Load control got aggregated sample {"t":1...
#{"t":1611081856,"g":[{"c":[{"w":7.95630067974},{"w":0.06374806566},{"w":-0.00161387508},{"w":1.50332463702},{"w":0.29695301472},{"w":4.71036340016}]},{"c":[{"w":3.68280907806},{"w":0.43628422996},{"w":0.00484162524},{"w":0.39782020722},{"w":0.13128643536},{"w":0.22755638628}]},{"c":[{"w":0.05191298174},{"w":0.01102814638},{"w":0.10409494266}]},{"c":[{"w":0.6173072181},{"w":0.10140515086},{"w":1.57433514054}]}]}



page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
text = soup.get_text()
for line in text.split('\n'):
    if re.search('INFO Load control got',line):
        wanted = re.findall(r'sample.([^\s]+)', line, re.I)
        #print(wanted[0])
        wrapper = json.loads(wanted[0])
        #print("now is:")
        #print(wrapper["t"])
        now = wrapper["t"]
        inner = wrapper["g"]

        value = str(inner[0]["c"][0]["w"])
        name = 'main-b'
        name = ''.join(('house.current.',name))
        carbondata.append("%s %s %d" % (name,value,now))

        name = "stove-ro"
        value = str(inner[0]["c"][1]["w"])
        name = ''.join(('house.current.',name))
        carbondata.append("%s %s %d" % (name,value,now))

        #double this one
        name = "well" 
        value = (inner[0]["c"][2]["w"] * 2)
        value = str(value)
        name = ''.join(('house.current.',name))
        carbondata.append("%s %s %d" % (name,value,now))

        name = "carrie-pc"
        value = str(inner[0]["c"][3]["w"])
        name = ''.join(('house.current.',name))
        carbondata.append("%s %s %d" % (name,value,now))

        name = "garage-a"
        value = str(inner[0]["c"][4]["w"])
        name = ''.join(('house.current.',name))
        carbondata.append("%s %s %d" % (name,value,now))

        name = "kitchen-dw-ll-server"
        value = str(inner[0]["c"][5]["w"])
        name = ''.join(('house.current.',name))
        carbondata.append("%s %s %d" % (name,value,now))

        name = "main-b"
        value = str(inner[1]["c"][0]["w"])
        name = ''.join(('house.current.',name))
        carbondata.append("%s %s %d" % (name,value,now))

        name = "refrigerator"
        value = str(inner[1]["c"][1]["w"])
        name = ''.join(('house.current.',name))
        carbondata.append("%s %s %d" % (name,value,now))

        name = "airconditioner"
        value = (inner[1]["c"][2]["w"] * 2)
        value = str(value)
        name = ''.join(('house.current.',name))
        carbondata.append("%s %s %d" % (name,value,now))

        name = "basement-sw"
        value = str(inner[1]["c"][3]["w"])
        name = ''.join(('house.current.',name))
        carbondata.append("%s %s %d" % (name,value,now))

        name = "garage-bj"
        value = str(inner[1]["c"][4]["w"])
        name = ''.join(('house.current.',name))
        carbondata.append("%s %s %d" % (name,value,now))

        name = "bath"
        value = str(inner[1]["c"][5]["w"])
        name = ''.join(('house.current.',name))
        carbondata.append("%s %s %d" % (name,value,now))

        name = "laundry"
        value = str(inner[2]["c"][0]["w"])
        name = ''.join(('house.current.',name))
        carbondata.append("%s %s %d" % (name,value,now))

        name = "kitchen-a"
        value = str(inner[2]["c"][1]["w"])
        name = ''.join(('house.current.',name))
        carbondata.append("%s %s %d" % (name,value,now))

        name = "furnace"
        value = str(inner[2]["c"][2]["w"])
        name = ''.join(('house.current.',name))
        carbondata.append("%s %s %d" % (name,value,now))

        name = "nw-house-corner"
        value = str(inner[3]["c"][0]["w"])
        name = ''.join(('house.current.',name))
        carbondata.append("%s %s %d" % (name,value,now))

        name = "kitchen-b"
        value = str(inner[3]["c"][1]["w"])
        name = ''.join(('house.current.',name))
        carbondata.append("%s %s %d" % (name,value,now))

        name = "ll-freezer-dehumidifier"
        value = str(inner[3]["c"][2]["w"])
        name = ''.join(('house.current.',name))
        carbondata.append("%s %s %d" % (name,value,now))



message = '\n'.join(carbondata) + '\n' #all lines must end in a newline
#print("sending message")
#print(message)
sock.sendall(message.encode('utf-8'))

sys.exit(0)
