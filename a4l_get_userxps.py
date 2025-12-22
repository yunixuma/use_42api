
from api42lib import IntraAPIClient
import sys
import datetime
import my_common as my

campus_name = "Tokyo"
cursus_name = "42cursus"
quest_name = "CommonCoreValidation"
kickoff_lower = "2020-01-01T00:00:00Z"
kickoff_upper = "2028-09-30T23:59:59Z"

def get_xps(n_days = 1, created_at_upper = None):
    if created_at_upper == None:
        created_at_upper = datetime.datetime.now().astimezone(datetime.timezone.utc)
    created_at_lower = created_at_upper - datetime.timedelta(days = n_days)
    ic = IntraAPIClient(config_path="./config.yml")

    params = {
        "filter[name]": campus_name
    }
    campus_id = ic.get("campus", params=params).json()[0].get("id")

    params = {
        "filter[name]": cursus_name
    }
    cursus_id = ic.get("cursus", params=params).json()[0].get("id")

    params = {
        "filter[campus_id]": campus_id,
        "filter[cursus_id]": cursus_id,
        "range[created_at]": f"{created_at_lower},{created_at_upper}"
    }
    xps = ic.pages_threaded("experiences", params=params)
    return xps

def get_cursus_users(n_days = 1, created_at_upper = None):
    if created_at_upper == None:
        created_at_upper = datetime.datetime.now().astimezone(datetime.timezone.utc)
    created_at_lower = created_at_upper - datetime.timedelta(days = n_days)
    ic = IntraAPIClient(config_path="./config.yml")

    params = {
        "filter[name]": campus_name
    }
    campus_id = ic.get("campus", params=params).json()[0].get("id")

    params = {
        "filter[name]": cursus_name
    }
    cursus_id = ic.get("cursus", params=params).json()[0].get("id")

    params = {
        "filter[campus_id]": campus_id,
        "filter[cursus_id]": cursus_id,
        "range[begin_at]": f"{created_at_lower},{created_at_upper}",
    }
    cus = ic.pages_threaded("cursus_users", params=params)
    return cus

def get_userxps(n_days, created_at_upper, user_lst = None):
    cus = get_cursus_users(n_days, created_at_upper)
    print(len(cus))
    xps = get_xps(n_days, created_at_upper)
    print(len(xps))
    xps_history = {}

    for cu in cus:
        # print(xp)
        if cu['user'] and cu['user'].get("login"):
            login = cu['user']['login']
            if user_lst is not None and login not in user_lst:
                continue
            xps_history[login] = [
                {
                    # 'login': login,
                    'xp': 0,
                    'project': None,
                    'created_at': my.datetime_normalize(cu['begin_at'])
                }
            ]

    for xp in xps:
        # print(xp)
        if xp['user'] and xp['user'].get("login"):
            login = xp['user']['login']
            if user_lst is not None and login not in user_lst:
                continue
            if login not in xps_history:
                xps_history[login] = []
            xps_history[login].append( {
                # 'login': login,
                'xp': xp['experience'],
                'project': xp['experiancable']['project'].get('slug') if xp['experiancable'].get('project') else None,
                'created_at': my.datetime_normalize(xp['created_at'])
            } )
    for login in xps_history:
        xps_history[login].sort(key=lambda x: x['created_at'])
    return xps_history

def wrapper(args) -> str:
    if len(args) > 1:
        n_days = int(args[1])
    else:
        n_days = 1
    if len(args) > 2:
        created_at_upper = my.datetime_normalize(args[2])
    else:
        created_at_upper = None
    if len(args) > 3:
        with open(args[3], 'r') as f:
            user_lst = [f.strip() for f in f.readlines()]
    else:
        user_lst = None

    userxps = get_userxps(n_days, created_at_upper, user_lst)
    if len(args) > 4:
        my.save_json(userxps, args[4])
        return len(userxps)
    else:
        return userxps

if __name__ == "__main__":
    start_at = datetime.datetime.now()
    print(wrapper(sys.argv))
    finish_at = datetime.datetime.now()
    print(f"Elapsed time: {finish_at - start_at}")
