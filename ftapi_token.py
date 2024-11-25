#! /usr/bin/env python3

import sys, os, json
import urllib3, requests
# var = globals()
DEBUG = True
import ftapi_common as ftapi
# if not "ftapi_common" in sys.modules:
#     print("ftapi_common is not imported")
#     import ftapi_common
#     print("ftapi_common just has been imported")
# else:
#     print("ftapi_common is already imported")
#     ftapi_common = sys.modules["ftapi_common"]
# ftapi_vars = ftapi_common.import_module("ftapi_vars", DEBUG)

# ftapi.my.debug_print(ftapi_vars.FT_UID)
# ftapi.my.debug_print(ftapi_vars.FT_SECRET)
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
#     ftapi.my.debug_print("Before requests.post", DEBUG, ftapi.my.COLOR["INFO"])
#     res = requests.post(url, data=data)
#     ftapi.my.debug_print("After  requests.post", DEBUG, ftapi.my.COLOR["SUCCESS"])
# except:
#     ftapi.my.debug_print("Error: Unable to connect to 42 API", DEBUG, ftapi.my.COLOR["FAILURE"])

try:
    # json_data = res.json()
    json_data = ftapi.post_method(endpoint, payload)
    ftapi.my.debug_print(str(json_data))
except:
    ftapi.my.debug_print("Exiting on failure", DEBUG, ftapi.my.COLOR["FAILURE"])
    sys.exit(1)

try:
    token = json_data['access_token']
    ftapi.my.debug_print(token)
except:
    ftapi.my.debug_print("Exiting on failure", DEBUG, ftapi.my.COLOR["FAILURE"])
    sys.exit(1)
