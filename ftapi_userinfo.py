#! /usr/bin/env python3

import sys, os, json
import urllib3, requests
import my_common as my
ftapi = my.import_module("ftapi_common", my.DEBUG)
DEBUG = True
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_dir = BASE_DIR + "/data/userinfo"
my.mkdir(data_dir, DEBUG)

my.debug_print(ftapi.ftapi_token.token, DEBUG, my.COLOR["DEBUG"])

if len(sys.argv) < 2:
    login = "ylinux"
else:
    login = sys.argv[1]
datetime = my.get_datetime()
filepath = login + "_" + datetime + ".json"
filepath = data_dir + "/" + filepath
my.debug_print(filepath, DEBUG, my.COLOR["DEBUG"])

endpoint = '/v2/users/' + login
data = {
    'Authorization' : 'Bearer ' + ftapi.ftapi_token.token
}
    # 'Authorization' : 'Bearer ' + ftapi_common.ftapi_token.token
    # 'access_token': ftapi_common.ftapi_token.token
my.debug_print(endpoint, DEBUG, my.COLOR["DEBUG"])
my.debug_print(str(data), DEBUG, my.COLOR["DEBUG"])
try:
    json_data = ftapi.get_method(endpoint, data)
    my.debug_print(str(json_data))
except:
    ftapi.my.debug_print("Exiting on failure", DEBUG, ftapi.my.COLOR["FAILURE"])
    sys.exit(1)
try:
    my.save_json(json_data, filepath)
except:
    ftapi.my.debug_print("Exiting on failure", DEBUG, ftapi.my.COLOR["FAILURE"])
    sys.exit(1)
