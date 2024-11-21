#! /usr/bin/env python3

import sys, os, json
import urllib3, requests
import ftapi_common
DEBUG = True

ftapi_common.debug_print(ftapi_common.ftapi_token.token, DEBUG, "35m")

FT_UID = os.environ['FT_UID']
FT_SECRET = os.environ['FT_SECRET']
if len(sys.argv) < 2:
    login = "ylinux"
else:
    login = sys.argv[1]

endpoint = '/v2/users/' + login
data = {
    'access_token': ftapi_common.ftapi_token.token
}
    # 'Authorization' : 'Bearer ' + ftapi_common.ftapi_token.token

try:
    ftapi_common.debug_print("Before requests.post", DEBUG, "36m")
    json_data = ftapi_common.get_method(endpoint, data)
    ftapi_common.debug_print(json_data)
    ftapi_common.debug_print("After  requests.post", DEBUG, "32m")
except:
    ftapi_common.debug_print("Error: Unable to connect to 42 API", DEBUG, "31m")
