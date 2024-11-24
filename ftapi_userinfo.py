#! /usr/bin/env python3

import sys, os, json
import urllib3, requests
import my_common as my
ftapi = my.import_module("ftapi_common", my.DEBUG)
DEBUG = True
PATH_DIR = os.path.dirname(os.path.abspath(__file__))
my.debug_print(ftapi.ftapi_token.token, DEBUG, my.COLOR["DEBUG"])

if len(sys.argv) < 2:
    login = "ylinux"
else:
    login = sys.argv[1]
datetime = my.get_datetime()
filepath = login + "_" + datetime + ".json"
filepath = PATH_DIR + "/" + filepath
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
    my.debug_print("Before requests.post", DEBUG, my.COLOR["INFO"])
    json_data = ftapi.get_method(endpoint, data)
    my.debug_print(str(json_data))
    my.debug_print("After  requests.post", DEBUG, my.COLOR["SUCCESS"])
except:
    my.debug_print("Error: Unable to connect to 42 API", DEBUG, my.COLOR["ERROR"])
try:
    my.debug_print("Before save JSON to file", DEBUG, my.COLOR["INFO"])
    my.save_json(json_data, filepath)
    my.debug_print("After  save JSON to file", DEBUG, my.COLOR["SUCCESS"])
except:
    my.debug_print("Error: Unable to save to file", DEBUG, my.COLOR["ERROR"])
