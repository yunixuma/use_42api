#! /usr/bin/env python3

import sys, os, json
import urllib3, requests
import ftapi_common
DEBUG = True

ftapi_common.debug_print(ftapi_common.ftapi_token.token, DEBUG, "35m")

FT_UID = os.environ['FT_UID']
FT_SECRET = os.environ['FT_SECRET']
campus_no = 26
idx_page = 1

endpoint = '/v2/campus/' + str(campus_no) + '/users?page[number]=' + str(idx_page) + '&page[size]=100'
data = {
    "access_token": ftapi_common.ftapi_token.token
}

try:
    ftapi_common.debug_print("Before requests.get", DEBUG, "36m")
    json_data = ftapi_common.get_method(endpoint, data)
    ftapi_common.debug_print(json_data)
    ftapi_common.debug_print("After  requests.get", DEBUG, "32m")
except:
    ftapi_common.debug_print("Error: Unable to connect to 42 API", DEBUG, "31m")
