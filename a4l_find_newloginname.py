
from api42lib import IntraAPIClient
import sys
import datetime
import a4l_get_locations
from collections import namedtuple
import my_common as my

LENGTH = 8

def find_newloginname(first, last):
    ic = IntraAPIClient(config_path="./config.yml")

    num = 1
    length = LENGTH
    i = 1
    while True:
        if len(first) < i or length == i:
            i = 1
            if num == 1:
                length -= 1
            num += 1
        login = first[:i] + last[:(length - i)]
        if num > 1:
            login += str(num)
        print(f"Try login: {login}")
        try:
            data = ic.get("users/" + login).json()
            if len(data) == 0:
                break
        except:
            break
        i += 1
    return login

def wrapper(args) -> str:
    if len(args) > 1:
        first = args[1]
    else:
        first = ""
    if len(args) > 2:
        last = args[2]
    else:
        last = ""
    return find_newloginname(first, last)

if __name__ == "__main__":
    start_at = datetime.datetime.now()
    print(wrapper(sys.argv))
    finish_at = datetime.datetime.now()
    print(f"Elapsed time: {finish_at - start_at}")
