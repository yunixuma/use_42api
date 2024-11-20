import sys, os
from dotenv import load_dotenv

DEBUG = True
load_dotenv()

def debug_print(msg, flag = DEBUG, color = "\033[0m"):
    if flag:
        print(color + msg + "\033[0m")
def import_module(mod, flag_debug):
    if not mod in sys.modules:
        # Dynamically import the module using __import__
        debug_print(mod + " is not imported", flag_debug, "\033[31m")
        imported_mod = __import__(mod)
        debug_print(mod + " just has been imported", flag_debug, "\033[32m")
        return imported_mod
    else:
        # If already imported, return the module from sys.modules
        debug_print(mod + " is already imported", flag_debug, "\033[32m")
        return sys.modules[mod]

ftapi_token = import_module("ftapi_token", DEBUG)
# if not "ftapi_token" in sys.modules:
#     debug_print("ftapi_token is not imported", DEBUG)
#     import ftapi_token
#     debug_print("ftapi_token just has been imported", DEBUG)
# else:
#     debug_print("ftapi_token is already imported", DEBUG)
#     ftapi_token = sys.modules["ftapi_token"]
