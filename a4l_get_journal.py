from api42lib import IntraAPIClient
import os, sys, json, datetime, math
import my_common as my

var = {
    "reason": [
		"Earning after defense",
		"Defense plannification",
    ],
    "kickoff_lower": "2020-01-01T00:00:00Z",
    "kickoff_upper": "2028-12-31T23:59:59Z",
    "cursus_name": "42cursus",
    "campus_name": "Tokyo",
    "test_user": ""
}

def get_journal(reason = None):
    ic = IntraAPIClient(config_path="./config.yml")

    params = {
        "filter[name]": var['campus_name'],
    }
    campus_id = ic.get("campus", params=params).json()[0].get("id")

    params = {
        "sort": "created_at"
    }
    if reason != None:
        params["filter[reason]"] = reason
    journal = ic.get(f"campus/{campus_id}/journals", params=params).json()

    for j in journal:
        print(j)
        break
    return journal

def wrapper(args):
    if len(args) > 1:
        reason = int(args[1])
    else:
        reason = None
    return get_journal(reason)

if __name__ == "__main__":
    start_at = datetime.datetime.now()

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    data_dir = BASE_DIR + "/data/evals"
    my.mkdir(data_dir, True)
    datetime = my.get_datetime()
    filepath = "evals_" + datetime + ".json"
    filepath = data_dir + "/" + filepath

    ret = wrapper(sys.argv)
    my.save_json(ret, "./journal.json")

    finish_at = datetime.datetime.now()
    print(f"Elapsed time: {finish_at - start_at}")
