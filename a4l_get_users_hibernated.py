from api42lib import IntraAPIClient
import sys
import datetime

campus_name = "Tokyo"
cursus_name = "42cursus"
quest_name = "CommonCoreValidation"

def get_users_hibernated(n_days = 15, paced = True):
    if paced:
        kickoff_lower = "2024-10-01T00:00:00Z"
        kickoff_upper = "2028-09-30T23:59:59Z"
    else:
        kickoff_lower = "2020-01-01T00:00:00Z"
        kickoff_upper = "2024-09-30T23:59:59Z"
    bh_lower = kickoff_lower
    bh_upper = "4242-12-31T23:59:59Z"
    updated_upper = datetime.datetime.now()
    updated_lower = updated_upper + datetime.timedelta(days=-n_days)
    ic = IntraAPIClient(config_path="./config.yml")

    params = {
        "filter[name]": campus_name
    }
    campus_id = ic.get("campus", params=params).json()[0].get("id")

    params = {
        "filter[name]": cursus_name
    }
    cursus_id = ic.get("cursus", params=params).json()[0].get("id")

    # params = {
    #     "filter[name]": quest_name
    # }
    # quest_id = ic.get("quests", params=params).json()[0].get("id")
    quest_id = 37

    params = {
        "filter[campus_id]": campus_id,
        "filter[quest_id]": quest_id,
        "filter[validated]": "true",
        "sort": "end_at",
    }
    quest_users = ic.pages_threaded("quests_users", params=params)
    quest_user_ids = []
    for quest_user in quest_users:
        quest_user_ids.append(quest_user['user']['id'])

    params = {
        "filter[campus_id]": campus_id,
        "range[begin_at]": f"{updated_lower},{updated_upper}"
    }
    user_locations = ic.pages_threaded("locations", params=params)

    params = {
        "filter[campus_id]": campus_id,
        "range[begin_at]": f"{kickoff_lower},{kickoff_upper}",
        "range[blackholed_at]": f"{bh_lower},{bh_upper}",
        "sort": "created_at",
    }
    users = ic.pages_threaded("cursus/" + str(cursus_id) + "/cursus_users", params=params)

    ret = "login   \tlevel\terase_at\n"
    # ret = "login   \tactive?\terase_at\n"
    for user in users:
        if user['user'].get('active?') != None and user['user'].get("active?") == False:
            continue
        if user['user'].get('end_at') != None and user['user'].get("end_at") < updated_upper:
            continue
        if user['user'].get("id") in quest_user_ids:
            continue
        is_hibernated = True
        for user_location in user_locations:
            if user_location['user']['id'] == user['user']['id']:
                is_hibernated = False
                break
        if is_hibernated and user['user'].get("staff?") == False:
            erase_at = datetime.datetime.strptime(user['user'].get("data_erasure_date"), '%Y-%m-%dT%H:%M:%S.%f%z').strftime("%Y-%m-%d")
            ret += f"{user['user']['login']:8s}\t{user.get('level'):.2f}\t{erase_at}\n"
            # ret += f"{user['user']['login']:8s}\t{user['user'].get('active?')}\t{erase_at}\n"
    ret = "```" + ret + "```"
    return ret

def wrapper(args) -> str:
    if len(args) > 1:
        n_days = int(args[1])
    else:
        n_days = 15
    if len(args) <= 2 or args[2] == "paced":
        paced = True
    else:
        paced = False
    return get_users_hibernated(n_days, paced)

if __name__ == "__main__":
    start_at = datetime.datetime.now()
    print(wrapper(sys.argv))
    finish_at = datetime.datetime.now()
    print(f"Elapsed time: {finish_at - start_at}")
