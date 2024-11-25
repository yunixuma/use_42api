import sys, os
import my_common as my
import json, requests

DEBUG = True

URL_42API = "https://api.intra.42.fr"
HEADER = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

def post_method(endpoint, payload, flag_debug = DEBUG):
    url = URL_42API + endpoint
    headers = HEADER
    try:
        my.debug_print("Before POST request", flag_debug, my.COLOR["INFO"])
        res = requests.request("POST", url, headers=headers, data=payload)
        my.debug_print("After  POST request", flag_debug, my.COLOR["SUCCESS"])
        return res.json()
    except:
        my.debug_print("Error: Unable to connect to 42 API", flag_debug, my.COLOR["FAILURE"])
        return None

def get_method(endpoint, payload, flag_debug = DEBUG):
    url = URL_42API + endpoint
    headers = HEADER
    headers['Authorization'] = payload['Authorization']
    # my.debug_print(url)
    # my.debug_print(str(headers))
    # my.debug_print(str(payload))
    try:
        my.debug_print("Before GET request", flag_debug, my.COLOR["INFO"])
        # res = requests.request("GET", url, headers=headers, data=payload)
        # res = requests.request("GET", url, headers=headers)
        res = requests.get(url, headers=headers)
        my.debug_print("After  GET request", flag_debug, my.COLOR["SUCCESS"])
        # my.debug_print(str(res))
        res.raise_for_status()
        # my.debug_print(str(res.json()))
        return res.json()
    except:
        my.debug_print("Error: Unable to connect to 42 API", flag_debug, my.COLOR["FAILURE"])
        return None

ftapi_token = my.import_module("ftapi_token", DEBUG)
# if not "ftapi_token" in sys.modules:
#     my.debug_print("ftapi_token is not imported", flag_debug)
#     import ftapi_token
#     my.debug_print("ftapi_token just has been imported", flag_debug)
# else:
#     my.debug_print("ftapi_token is already imported", flag_debug)
#     ftapi_token = sys.modules["ftapi_token"]
