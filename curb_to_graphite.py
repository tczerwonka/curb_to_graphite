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

URL = "http://192.168.1.28"

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
        #print("wrapper is:")
        #print(wrapper)
        print("wrapper t is:")
        print(wrapper["t"])
        #print("wrapper g is:")
        #print(wrapper["g"])
        inner = wrapper["g"]
        #main-b
        print(inner[0]["c"][0])
        #stove-ro
        print(inner[0]["c"][1])
        #well --double
        print(inner[0]["c"][2])
        #carrie-pc
        print(inner[0]["c"][3])
        #garage-a
        print(inner[0]["c"][4])
        #kitchen-dw-ll-server
        print(inner[0]["c"][5])
        #main-b
        print(inner[1]["c"][0])
        #refrigerator
        print(inner[1]["c"][1])
        #AC -- double
        print(inner[1]["c"][2])
        #basement-sw
        print(inner[1]["c"][3])
        #garage-bj
        print(inner[1]["c"][4])
        #bath
        print(inner[1]["c"][5])
        #laundry
        print(inner[2]["c"][0])
        #kitchen-a
        print(inner[2]["c"][1])
        #furnace
        print(inner[2]["c"][2])
        #nw-house-corner
        print(inner[3]["c"][0])
        #kitchen-b
        print(inner[3]["c"][1])
        #ll-freezer-dehumidifier
        print(inner[3]["c"][2])
        print("---")

