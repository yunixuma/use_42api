
from api42lib import IntraAPIClient
import sys
import datetime
import my_common as my

campus_name = "Tokyo"
cursus_name = "42cursus"
quest_name = "CommonCoreValidation"
kickoff_lower = "2020-01-01T00:00:00Z"
kickoff_upper = "2028-09-30T23:59:59Z"

def get_logintime(userlist = None, n_days = 1, begin_at_upper = None, m_days = 1):
    if begin_at_upper == None:
        begin_at_upper = datetime.datetime.now()
    begin_at_lower = begin_at_upper - datetime.timedelta(days = n_days + m_days)
    ic = IntraAPIClient(config_path="./config.yml")

    params = {
        "filter[name]": campus_name
    }
    campus_id = ic.get("campus", params=params).json()[0].get("id")

    params = {
        "filter[campus_id]": campus_id,
        "range[begin_at]": f"{begin_at_lower},{begin_at_upper}"
    }
    locations = ic.pages_threaded("locations", params=params)
    begin_at_lower += datetime.timedelta(days=m_days)

    logintime = {}
    for location in locations:
        if userlist == None or location['user'].get('login') in userlist:
            login = location['user']['login']
            end_at = location['end_at']
            if end_at is None:
                end_at = begin_at_upper
            else:
                end_at = datetime.datetime.strptime(location['end_at'], "%Y-%m-%dT%H:%M:%S.%f%z")
            begin_at = datetime.datetime.strptime(location['begin_at'], "%Y-%m-%dT%H:%M:%S.%f%z")
            if begin_at < begin_at_lower:
                begin_at = begin_at_lower
            if end_at < begin_at:
                continue
            if login not in logintime:
                logintime[login] = []
            logintime[login].append({
                "begin_at": begin_at,
                "end_at": end_at
                })
    return logintime

def wrapper(args) -> str:
    if len(args) > 1 and args[1] != "all":
        userlist = []
        users = my.load_csv(args[1])
        for user in users:
            if user.get('login'):
                userlist.append(user['login'])
        print(f"Num of users: {len(userlist)}")
    else:
        userlist = None
    if len(args) > 2:
        n_days = int(args[2])
    else:
        n_days = 1
    if len(args) > 3:
        begin_at_upper = datetime.datetime.strptime(args[3], "%Y-%m-%dT%H:%M:%S.%f%z")
    else:
        begin_at_upper = None
    if len(args) > 4:
        m_days = int(args[4])
    else:
        m_days = 1
    return get_logintime(userlist, n_days, begin_at_upper, m_days)

if __name__ == "__main__":
    start_at = datetime.datetime.now()
    logintimes = wrapper(sys.argv)
    print(logintimes)
    # print(my.calc_overlap_duration(logintimes['login1'], logintimes['login2']))
    finish_at = datetime.datetime.now()
    print(f"Elapsed time: {finish_at - start_at}")
