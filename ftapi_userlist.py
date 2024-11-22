#! /usr/bin/env python3

import sys, os, json
import urllib3, requests
import ftapi_common as ftapi
DEBUG = True

ftapi.my.debug_print(ftapi.ftapi_token.token, DEBUG, "35m")

FT_UID = os.environ['FT_UID']
FT_SECRET = os.environ['FT_SECRET']
campus_no = 26
idx_page = 1

endpoint = f"/v2/campus/{campus_no}/users?page[number]={idx_page}&page[size]=100"
data = {
    'Authorization' : 'Bearer ' + ftapi.ftapi_token.token
}
ftapi.my.debug_print(endpoint, DEBUG, "33m")
ftapi.my.debug_print(str(data), DEBUG, "33m")
try:
    ftapi.my.debug_print("Before requests.get", DEBUG, "36m")
    json_data = ftapi.get_method(endpoint, data)
    ftapi.my.debug_print(str(json_data))
    ftapi.my.debug_print("After  requests.get", DEBUG, "32m")
except:
    ftapi.my.debug_print("Error: Unable to connect to 42 API", DEBUG, "31m")
