import sys, os, json, csv
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
def strptime(s_ts):
    try:
        ts = datetime.datetime.strptime(s_ts, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        ts = datetime.datetime.strptime(s_ts, "%Y-%m-%dT%H:%M:%SZ")
    return ts.astimezone(datetime.timezone(datetime.timedelta(hours=+9)))
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

def load_csv(path, flag_debug=DEBUG):
    """
    Reads a CSV file and returns its contents as a list of dictionaries (JSON-like).
    """
    data = []
    try:
        debug_print(f"Opening CSV file: {path}", flag_debug, COLOR["INFO"])
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        debug_print("CSV file successfully converted to JSON object", flag_debug, COLOR["SUCCESS"])
    except Exception as e:
        debug_print(f"Failed to convert CSV to JSON: {e}", flag_debug, COLOR["FAILURE"])
    return data

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
def str_filter(value, condition):
    # print(value, condition)
    conds = condition.split(',')
    for cond in conds:
        if cond in value:
            return cond
    return None
def calc_overlap_duration(periods_1, periods_2):
    periods_1.sort(key=lambda x: x['begin_at'], reverse=False)
    periods_2.sort(key=lambda x: x['begin_at'], reverse=False)
    duration = datetime.timedelta(0)
    i, j = 0, 0
    while i < len(periods_1) and j < len(periods_2):
        if periods_1[i]['end_at'] < periods_2[j]['begin_at']:
            i += 1
            continue
        if periods_2[j]['end_at'] < periods_1[i]['begin_at']:
            j += 1
            continue
        begin_at = max(periods_1[i]['begin_at'], periods_2[j]['begin_at'])
        end_at = min(periods_1[i]['end_at'], periods_2[j]['end_at'])
        duration += end_at - begin_at
        if periods_1[i]['end_at'] < periods_2[j]['end_at']:
            i += 1
        else:
            j += 1
    return duration
def datetime_normalize(ts):
    try:
        dt = datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%f%z")
    except ValueError as e:
        debug_print(f"Error: {e}", True, COLOR["FAILURE"])
        try:
            dt = datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S%z")
        except ValueError as e:
            debug_print(f"Error: {e}", True, COLOR["FAILURE"])
            dt = datetime.datetime.strptime(ts, "%Y-%m-%d")
    except Exception as e:
            debug_print(f"Error: {e}", True, COLOR["FAILURE"])
            dt = ts
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    else:
        dt = dt.astimezone(datetime.timezone.utc)
    return dt

if __name__ == "__main__":
    ts = "2023-10-01T12:34:56.0+0900"
    dt = {"ts": datetime_normalize(ts)}
    print(ts)
    print(dt)
    dt2 = {"ts": datetime_normalize(dt["ts"])}
    dt2["ts"] = dt2["ts"].replace(tzinfo=datetime.timezone.utc)
    print(dt2)
    print(dt2["ts"] > dt["ts"])