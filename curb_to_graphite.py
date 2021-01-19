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
# python3 -m pip install requests
################################################################################

import requests

URL = "http://192.168.1.28"


page = requests.get(URL)
page

