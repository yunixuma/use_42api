from api42lib import IntraAPIClient
import sys, datetime, math

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

def get_user_recentpoint(n_days = 1):
    date_lower = datetime.datetime.now() + datetime.timedelta(days = -n_days)
    date_upper = date_lower + datetime.timedelta(days = n_days + 7)
    max_rows = 10
    ic = IntraAPIClient(config_path="./config.yml")

    params = {
        "filter[name]": var['campus_name'],
    }
    campus_id = ic.get("campus", params=params).json()[0].get("id")

    # cursuses = ic.pages_threaded("cursus")
    # for cursus in cursuses:
    #     if cursus['name'] == cursus_name:
    #         cursus_id = cursus['id']
    #         break
    params = {
        "filter[name]": var['cursus_name'],
    }
    cursus_id = ic.get("cursus", params=params).json()[0].get("id")

    params = {
        "filter[campus_id]": campus_id,
        "range[begin_at]": f"{var['kickoff_lower']},{var['kickoff_upper']}",
        # "range[updated_at]": f'{date_lower},{date_upper}',
        "filter[end_at]": None,
        "sort": "-updated_at",
    }
    users = ic.pages_threaded("cursus/" + str(cursus_id) + "/cursus_users", params=params)
    ret = "login   \tupdated_at\treason\n"
    for user in users:
        if "3b3-" in user['user']['login']:
            continue
        if var.get("test_user") != None and var.get("test_user") != "" \
            and user['user']['login'] != var['test_user']:
            continue
        if datetime.datetime.strptime(user['user']['updated_at'], '%Y-%m-%dT%H:%M:%S.%fZ') < date_lower:
            continue
        user_id = user['user']['id']
        print(user['user']['login']) 
        try:
            params = {
                "range[updated_at]": f"{date_lower},{date_upper}",
                "sort": "-id"
                # "filter[quest_id]": quest_id,
                # "filter[validated]": "true",
            }
            recentpoints = ic.pages_threaded("users/" + str(user_id) + "/correction_point_historics")
            if recentpoints != None and len(recentpoints) > 0:
                continue
            else:
                rows = 0
                for recentpoint in recentpoints:
                    if datetime.datetime.strptime(recentpoint['updated_at'], '%Y-%m-%dT%H:%M:%S.%fZ') < date_lower:
                        continue
                    if recentpoint['reason'] in var['reason']:
                        continue
                    rows += 1
                    if rows > max_rows:
                        break
                    ret += f"{user['user']['login']:8s}\t{recentpoint['updated_at']}\t{recentpoint['reason']}\n"
        except Exception as e:
            print("Error: " + str(e))
            continue
    ret = "```\n" + ret + "```"

def wrapper(args) -> str:
    if len(args) > 1:
        n_days = int(args[1])
    else:
        n_days = 15
    return get_user_recentpoint(n_days)

if __name__ == "__main__":
    start_at = datetime.datetime.now()
    print(wrapper(sys.argv))
    finish_at = datetime.datetime.now()
    print(f"Elapsed time: {finish_at - start_at}")
