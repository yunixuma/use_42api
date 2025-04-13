#! /usr/bin/env python3

import sys, os, json
import urllib3, requests
import my_common as my
DEBUG = True
ftapi = my.import_module("ftapi_common", DEBUG)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_dir = BASE_DIR + "/data/userquest"
my.mkdir(data_dir, DEBUG)

my.debug_print(ftapi.ftapi_token.token, DEBUG, my.COLOR["DEBUG"])

if len(sys.argv) < 2:
    login = "ylinux"
else:
    login = sys.argv[1]
datetime = my.get_datetime()
filepath = login + "_quest_" + datetime + ".json"
filepath = data_dir + "/" + filepath
my.debug_print(filepath, DEBUG, my.COLOR["DEBUG"])

header = {
    'Authorization' : 'Bearer ' + ftapi.ftapi_token.token
}
    # 'Authorization' : 'Bearer ' + ftapi_common.ftapi_token.token
    # 'access_token': ftapi_common.ftapi_token.token
my.debug_print(str(header), DEBUG, my.COLOR["DEBUG"])
json_data_joined = []
for idx_page in range(1, 200):
    uri = f"/v2/users/{login}/quests_users?page[number]={idx_page}&page[size]=100"
    my.debug_print(uri, DEBUG, my.COLOR["DEBUG"])
    try:
        json_data = ftapi.get_method(uri, header)
        my.debug_print(str(json_data))
    except:
        my.debug_print("Exiting on failure", DEBUG, my.COLOR["FAILURE"])
        exit(1)
    if json_data == None or len(json_data) == 0:
        break
    json_data_joined += json_data
try:
    my.save_json(json_data_joined, filepath)
except:
    my.debug_print("Exiting on failure", DEBUG, my.COLOR["FAILURE"])
    sys.exit(1)
