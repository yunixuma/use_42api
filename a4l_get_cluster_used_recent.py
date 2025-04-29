
from api42lib import IntraAPIClient
import sys
import datetime

campus_name = "Tokyo"
cursus_name = "42cursus"
quest_name = "CommonCoreValidation"
kickoff_lower = "2020-01-01T00:00:00Z"
kickoff_upper = "2028-09-30T23:59:59Z"

def get_login_cluster_recent(hostname = "c", n_days = 1):
    updated_upper = datetime.datetime.now()
    updated_lower = updated_upper + datetime.timedelta(days=-n_days)
    ic = IntraAPIClient(config_path="./config.yml")

    params = {
        "filter[name]": campus_name
    }
    campus_id = ic.get("campus", params=params).json()[0].get("id")

    params = {
        "filter[campus_id]": campus_id,
        "range[begin_at]": f"{updated_lower},{updated_upper}"
    }
    locations = ic.pages_threaded("locations", params=params)

    ret = ""
    for location in locations:
        if hostname in location['host']:
            ret += f"{location['host']:8s}\t{location['user'].get('login'):8s}\t{location['begin_at']}\t{location['end_at']}\n"
            # ret += f"{location['host']:8s}\t{location['user'].get('login'):8s}\t{location['begin_at']}\t{location['end_at']}\n"
    ret = "```\n" + ret + "```"
    return ret

def wrapper(args) -> str:
    if len(args) > 1:
        host = args[1]
    else:
        host = "c"
    if len(args) > 2:
        n_days = int(args[2])
    else:
        n_days = 1
    return get_login_cluster_recent(host, n_days)

if __name__ == "__main__":
    start_at = datetime.datetime.now()
    print(wrapper(sys.argv))
    finish_at = datetime.datetime.now()
    print(f"Elapsed time: {finish_at - start_at}")
