#! /usr/bin/env python3

import sys, os, json
import urllib3, requests
import my_common as my
DEBUG = True
ftapi = my.import_module("ftapi_common", DEBUG)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_dir = BASE_DIR + "/data/userlist"
my.mkdir(data_dir, DEBUG)

my.debug_print(ftapi.ftapi_token.token, DEBUG, my.COLOR["DEBUG"])

campus_no = 26
idx_page = 1

datetime = my.get_datetime()
filepath = "users_" + datetime + ".json"
filepath = data_dir + "/" + filepath

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
    my.debug_print("Exiting on failure", DEBUG, my.COLOR["FAILURE"])
    exit(1)
try:
    my.save_json(json_data, filepath)
except:
    my.debug_print("Exiting on failure", DEBUG, my.COLOR["FAILURE"])
    exit(1)
