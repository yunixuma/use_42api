#! /usr/bin/env python3

import sys, os, json
import urllib3, requests
import my_common as my
DEBUG = True
ftapi = my.import_module("ftapi_common", DEBUG)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_dir = BASE_DIR + "/data/eventusers"
my.mkdir(data_dir, DEBUG)

my.debug_print(ftapi.ftapi_token.token, DEBUG, my.COLOR["DEBUG"])

if len(sys.argv) < 2:
    event_id = "28242"
else:
    event_id = sys.argv[1]
datetime = my.get_datetime()
filepath = "event_" + event_id + '_' + datetime + ".json"
filepath = data_dir + "/" + filepath
my.debug_print(filepath, DEBUG, my.COLOR["DEBUG"])

# uri = '/v2/me/slots'
uri = '/v2/events/' + event_id + '/events_users'
data = {
    'Authorization' : 'Bearer ' + ftapi.ftapi_token.token
}
    # 'Authorization' : 'Bearer ' + ftapi_common.ftapi_token.token
    # 'access_token': ftapi_common.ftapi_token.token
my.debug_print(uri, DEBUG, my.COLOR["DEBUG"])
my.debug_print(str(data), DEBUG, my.COLOR["DEBUG"])
try:
    json_data = ftapi.get_method(uri, data)
    my.debug_print(str(json_data))
except:
    my.debug_print("Exiting on failure", DEBUG, my.COLOR["FAILURE"])
    sys.exit(1)
if json_data == None:
    my.debug_print("Error: No data", DEBUG, my.COLOR["ERROR"])
    sys.exit(1)
try:
    my.save_json(json_data, filepath)
except:
    my.debug_print("Exiting on failure", DEBUG, my.COLOR["FAILURE"])
    sys.exit(1)
