from api42lib import IntraAPIClient
import os, sys, json, datetime, math
import my_common as my

var = {
    "cursus_name": "42cursus",
    "campus_name": "Tokyo",
    "test_user": ""
}

def get_questusers(quest_id = None):
    ic = IntraAPIClient(config_path="./config.yml")

    params = {
        "filter[name]": var['campus_name'],
    }
    campus_id = ic.get("campus", params=params).json()[0].get("id")

    params = {
        "filter[campus_id]": campus_id
    }
    if quest_id != None:
        params["filter[quest_id]"] = quest_id
    questusers = ic.pages_threaded(f"quests_users/", params=params)

    return questusers

def wrapper(args):
    if len(args) > 1:
        quest_id = int(args[1])
    else:
        quest_id = None
    return get_questusers(quest_id)

if __name__ == "__main__":
    start_at = datetime.datetime.now()

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    data_dir = BASE_DIR + "/data/questusers"
    my.mkdir(data_dir, True)
    date = my.get_datetime()
    filepath = "questusers_" + date + ".json"
    filepath = data_dir + "/" + filepath

    ret = wrapper(sys.argv)
    my.save_json(ret, filepath)

    finish_at = datetime.datetime.now()
    print(f"Elapsed time: {finish_at - start_at}")
