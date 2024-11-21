#! /usr/bin/env python3

import sys, os, json
import urllib3, requests
# var = globals()
DEBUG = True
import ftapi_common
# if not "ftapi_common" in sys.modules:
#     print("ftapi_common is not imported")
#     import ftapi_common
#     print("ftapi_common just has been imported")
# else:
#     print("ftapi_common is already imported")
#     ftapi_common = sys.modules["ftapi_common"]
# ftapi_vars = ftapi_common.import_module("ftapi_vars", DEBUG)

# ftapi_common.debug_print(ftapi_vars.FT_UID)
# ftapi_common.debug_print(ftapi_vars.FT_SECRET)
FT_UID = os.environ['FT_UID']
FT_SECRET = os.environ['FT_SECRET']

# url = 'https://api.intra.42.fr/oauth/token'
# data  = "grant_type=client_credentials&client_id=" + FT_UID + "&client_secret=" + FT_SECRET
endpoint = '/oauth/token'
payload = {
    'grant_type': 'client_credentials',
    'client_id': FT_UID,
    'client_secret': FT_SECRET
}

# try:
#     ftapi_common.debug_print("Before requests.post", DEBUG, "36m")
#     res = requests.post(url, data=data)
#     ftapi_common.debug_print("After  requests.post", DEBUG, "32m")
# except:
#     ftapi_common.debug_print("Error: Unable to connect to 42 API", DEBUG, "31m")

try:
    ftapi_common.debug_print("Before requests.post", DEBUG, "36m")
    # json_data = res.json()
    json_data = ftapi_common.post_method(endpoint, payload)
    ftapi_common.debug_print(json_data)
    ftapi_common.debug_print("After  requests.post", DEBUG, "32m")
except:
    ftapi_common.debug_print("Error: Unable to parse JSON response", DEBUG, "31m")

try:
    ftapi_common.debug_print("Before extract a token from JSON", DEBUG, "36m")
    token = json_data['access_token']
    ftapi_common.debug_print(token)
    ftapi_common.debug_print("After  extract a token from JSON", DEBUG, "32m")
except:
    ftapi_common.debug_print("Error: Unable to parse JSON response", DEBUG, "31m")
