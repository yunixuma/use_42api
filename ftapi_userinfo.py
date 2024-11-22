#! /usr/bin/env python3

import sys, os, json
import urllib3, requests
import ftapi_common as ftapi
DEBUG = True

ftapi.my.debug_print(ftapi.ftapi_token.token, DEBUG, "35m")

FT_UID = os.environ['FT_UID']
FT_SECRET = os.environ['FT_SECRET']
if len(sys.argv) < 2:
    login = "ylinux"
else:
    login = sys.argv[1]

endpoint = '/v2/users/' + login
data = {
    'Authorization' : 'Bearer ' + ftapi.ftapi_token.token
}
    # 'Authorization' : 'Bearer ' + ftapi_common.ftapi_token.token
    # 'access_token': ftapi_common.ftapi_token.token
ftapi.my.debug_print(endpoint, DEBUG, "33m")
ftapi.my.debug_print(str(data), DEBUG, "33m")
try:
    ftapi.my.debug_print("Before requests.post", DEBUG, "36m")
    json_data = ftapi.get_method(endpoint, data)
    ftapi.my.debug_print(str(json_data))
    ftapi.my.debug_print("After  requests.post", DEBUG, "32m")
except:
    ftapi.my.debug_print("Error: Unable to connect to 42 API", DEBUG, "31m")
