import sys, os, json
import datetime
from dotenv import load_dotenv

DEBUG = True
ANSI = {
    "ESC"       : "\033[",
    "BLACK"     : "30m",
    "RED"       : "31m",
    "GREEN"     : "32m",
    "YELLOW"    : "33m",
    "BLUE"      : "34m",
    "MAGENTA"   : "35m",
    "CYAN"      : "36m",
    "WHITE"     : "37m",
    "BG_BLACK"  : "40m",
    "BG_RED"    : "41m",
    "BG_GREEN"  : "42m",
    "BG_YELLOW" : "43m",
    "BG_BLUE"   : "44m",
    "BG_MAGENTA": "45m",
    "BG_CYAN"   : "46m",
    "BG_WHITE"  : "47m",
    "RESET"     : "0;",
    "BOLD"      : "1;",
    "FAINT"     : "2;",
    "ITALIC"    : "3;",
    "UNDERLINE" : "4;",
    "BLINK"     : "5;",
    "RAPID"     : "6;",
    "REVERSE"   : "7;",
    "CONCEAL"   : "8;",
    "STRIKE"    : "9;"
}
COLOR = {
    "DEBUG"   : ANSI["ESC"] + ANSI["ITALIC"] + ANSI["FAINT"] + ANSI["WHITE"],
    "INFO"    : ANSI["ESC"] + ANSI["ITALIC"] + ANSI["CYAN"],
    "WARNING" : ANSI["ESC"] + ANSI["ITALIC"] + ANSI["YELLOW"],
    "ERROR"   : ANSI["ESC"] + ANSI["ITALIC"] + ANSI["MAGENTA"],
    "SUCCESS" : ANSI["ESC"] + ANSI["GREEN"],
    "FAILURE" : ANSI["ESC"] + ANSI["RED"],
    "RESET"   : ANSI["ESC"] + ANSI["RESET"] + ANSI["WHITE"]
}
N_INDENT = 2

load_dotenv()

def debug_print(msg, flag_debug = DEBUG, color = COLOR["DEBUG"]):
    if flag_debug:
        print(color + msg + COLOR["RESET"])
def import_module(mod, flag_debug):
    if not mod in sys.modules:
        # Dynamically import the module using __import__
        debug_print(mod + " is not imported yet", flag_debug, COLOR["INFO"])
        imported_mod = __import__(mod)
        debug_print(mod + " just has been imported", flag_debug, COLOR["SUCCESS"])
        return imported_mod
    else:
        # If already imported, return the module from sys.modules
        debug_print(mod + " is already imported", flag_debug, COLOR["FAILURE"])
        return sys.modules[mod]
def get_datetime():
    return datetime.datetime.now().strftime("%Y%m%dT%H%M")
def mkdir(path, flag_debug = DEBUG):
    if os.path.exists(path):
        debug_print("Directory already exists", flag_debug, COLOR["INFO"])
        return
    try:
        debug_print("Before creating directory", flag_debug, COLOR["INFO"])
        os.makedirs(path)
        debug_print("After  creating directory", flag_debug, COLOR["SUCCESS"])
    except:
        debug_print("Unable to create directory", DEBUG, COLOR["FAILURE"])
        exit(1)
def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)
def save_json(data, path, flag_debug = DEBUG):
    try:
        debug_print("Before save JSON to file", flag_debug, COLOR["INFO"])
        with open(path, 'w') as f:
            json.dump(data, f, indent=N_INDENT)
        debug_print("After  save JSON to file", flag_debug, COLOR["SUCCESS"])
    except:
        debug_print("Unable to save JSON to file", flag_debug, COLOR["INFO"])
