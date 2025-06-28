from api42lib import IntraAPIClient
import os, sys, json, datetime, math
import my_common as my

var = {
    "cursus_name": "42cursus",
    "campus_name": "Tokyo",
    "test_user": ""
}

def get_projectusers(project_id = None):
    ic = IntraAPIClient(config_path="./config.yml")

    params = {
        "filter[name]": var['campus_name'],
    }
    campus_id = ic.get("campus", params=params).json()[0].get("id")

    params = {
        "filter[campus]": campus_id
    }
    if project_id != None:
        params["filter[project_id]"] = project_id
    projectusers = ic.pages_threaded(f"projects_users/", params=params)

    return projectusers

def wrapper(args):
    if len(args) > 1:
        project_id = int(args[1])
    else:
        project_id = None
    return get_projectusers(project_id)

if __name__ == "__main__":
    start_at = datetime.datetime.now()

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    data_dir = BASE_DIR + "/data/projectusers"
    my.mkdir(data_dir, True)
    date = my.get_datetime()
    filepath = "projectusers_"
    if len(sys.argv) > 1:
        filepath += sys.argv[1] + "_"
    filepath += date + ".json"
    filepath = data_dir + "/" + filepath

    ret = wrapper(sys.argv)
    my.save_json(ret, filepath)

    finish_at = datetime.datetime.now()
    print(f"Elapsed time: {finish_at - start_at}")
