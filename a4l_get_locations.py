
from api42lib import IntraAPIClient
import sys
import datetime
import my_common as my

campus_name = "Tokyo"
cursus_name = "42cursus"
quest_name = "CommonCoreValidation"
kickoff_lower = "2020-01-01T00:00:00Z"
kickoff_upper = "2028-09-30T23:59:59Z"

def get_locations(n_days = 1, begin_at_upper = None, hostname = None):
    if begin_at_upper == None:
        begin_at_upper = datetime.datetime.now().astimezone(datetime.timezone.utc)
    begin_at_lower = begin_at_upper - datetime.timedelta(days = n_days)
    ic = IntraAPIClient(config_path="./config.yml")

    params = {
        "filter[name]": campus_name
    }
    campus_id = ic.get("campus", params=params).json()[0].get("id")

    params = {
        "filter[campus_id]": campus_id,
        "range[begin_at]": f"{begin_at_lower},{begin_at_upper}"
    }
    if hostname:
        if "," in hostname:
            params["range[host]"] = hostname
        else:
            hostname_upper = hostname + "zz"
            params["range[host]"] = f"{hostname},{hostname_upper}"
    locations = ic.pages_threaded("locations", params=params)
    return locations

def wrapper(args) -> str:
    if len(args) > 1:
        n_days = int(args[1])
    else:
        n_days = 1
    if len(args) > 2:
        begin_at_upper = my.datetime_normalize(args[2])
    else:
        begin_at_upper = None
    if len(args) > 3:
        hostname = args[3]
    else:
        hostname = None
    return get_locations(n_days, begin_at_upper, hostname)

if __name__ == "__main__":
    start_at = datetime.datetime.now()
    print(wrapper(sys.argv))
    finish_at = datetime.datetime.now()
    print(f"Elapsed time: {finish_at - start_at}")
