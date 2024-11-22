#! /usr/bin/env python3

import sys, os, json
import urllib3, requests
import my_common as my
ftapi = my.import_module("ftapi_common", my.DEBUG)
DEBUG = True

my.debug_print(ftapi.ftapi_token.token, DEBUG, my.COLOR["DEBUG"])

FT_UID = os.environ['FT_UID']
FT_SECRET = os.environ['FT_SECRET']
campus_no = 26
idx_page = 1

endpoint = f"/v2/campus/{campus_no}/users?page[number]={idx_page}&page[size]=100"
data = {
    'Authorization' : 'Bearer ' + ftapi.ftapi_token.token
}
my.debug_print(endpoint, DEBUG, my.COLOR["DEBUG"])
my.debug_print(str(data), DEBUG, my.COLOR["DEBUG"])
try:
    my.debug_print("Before requests.get", DEBUG, my.COLOR["INFO"])
    json_data = ftapi.get_method(endpoint, data)
    my.debug_print(str(json_data))
    my.debug_print("After  requests.get", DEBUG, my.COLOR["SUCCESS"])
except:
    my.debug_print("Error: Unable to connect to 42 API", DEBUG, my.COLOR["FAILURE"])
