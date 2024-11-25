#! /usr/bin/env python3

import sys, os, json
import urllib3, requests
import my_common as my
ftapi = my.import_module("ftapi_common", my.DEBUG)
DEBUG = True
PATH_DIR = os.path.dirname(os.path.abspath(__file__))

my.debug_print(ftapi.ftapi_token.token, DEBUG, my.COLOR["DEBUG"])

campus_no = 26
idx_page = 1

datetime = my.get_datetime()
filepath = "users_" + datetime + ".json"
filepath = PATH_DIR + "/" + filepath

endpoint = f"/v2/campus/{campus_no}/users?page[number]={idx_page}&page[size]=100"
data = {
    'Authorization' : 'Bearer ' + ftapi.ftapi_token.token
}
my.debug_print(endpoint, DEBUG, my.COLOR["DEBUG"])
my.debug_print(str(data), DEBUG, my.COLOR["DEBUG"])
try:
    json_data = ftapi.get_method(endpoint, data)
    my.debug_print(str(json_data))
except:
    ftapi.my.debug_print("Exiting on failure", DEBUG, ftapi.my.COLOR["FAILURE"])
    exit(EXIT_FAILURE)
try:
    my.debug_print("Before save JSON to file", DEBUG, my.COLOR["INFO"])
    my.save_json(json_data, filepath)
    my.debug_print("After  save JSON to file", DEBUG, my.COLOR["SUCCESS"])
except:
    ftapi.my.debug_print("Exiting on failure", DEBUG, ftapi.my.COLOR["FAILURE"])
    exit(EXIT_FAILURE)
