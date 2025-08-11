from api42lib import IntraAPIClient
import os, sys, json, datetime, math
import my_common as my

var = {
    "cursus_name": "42cursus",
    "campus_name": "Tokyo",
    "test_user": ""
}

def get_campususers(campus_id = None):
    ic = IntraAPIClient(config_path="./config.yml")

    params = {
        "filter[campus_id]": campus_id
    }
    campususers = ic.pages_threaded(f"campus_users/", params=params)

    return campususers

def wrapper(args):
    if len(args) > 1:
        campus_id = int(args[1])
    else:
        campus_id = None
    return get_campususers(campus_id)

if __name__ == "__main__":
    start_at = datetime.datetime.now()

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    data_dir = BASE_DIR + "/data/campususers"
    my.mkdir(data_dir, True)
    date = my.get_datetime()
    filepath = "campususers_"
    if len(sys.argv) > 1:
        filepath += sys.argv[1] + "_"
    filepath += date + ".json"
    filepath = data_dir + "/" + filepath

    ret = wrapper(sys.argv)
    my.save_json(ret, filepath)

    finish_at = datetime.datetime.now()
    print(f"Elapsed time: {finish_at - start_at}")
