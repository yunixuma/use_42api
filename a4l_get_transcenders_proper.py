from api42lib import IntraAPIClient
import os, sys, json, datetime, math
import my_common as my

var = {
    "cursus_name": "42cursus",
    "campus_name": "Tokyo",
    "domain_name": "42tokyo.jp",
    "flag_tracen": 0x01,
    "flag_exam06": 0x02,
    "flag_cpc04": 0x04,
    "test_user": ""
}

def get_transcenders():
    ic = IntraAPIClient(config_path="./config.yml")

    params = {
        "filter[name]": var['campus_name'],
    }
    campus_id = ic.get("campus", params=params).json()[0].get("id")

    params = {
        "filter[name]": var['cursus_name']
    }
    cursus_id = ic.get("cursus", params=params).json()[0].get("id")

    params = {
        "filter[campus]": campus_id,
    }
    projectusers_tracen = ic.pages_threaded("projects/1337/projects_users", params=params)
    projectusers_exam06 = ic.pages_threaded("projects/1324/projects_users", params=params)
    projectusers_cpc04 = ic.pages_threaded("projects/1261/projects_users", params=params)

    params = {
        "filter[campus_id]": campus_id,
        "filter[end_at]": None
    }
    cursususers = ic.pages_threaded("cursus/" + str(cursus_id) + "/cursus_users", params=params)

    users = {}
    for user in projectusers_exam06:
        # if user['user']['login'] == var['test_user']:
        #     print(user)
        if user.get('validated?') == True:
            # validated_at = datetime.datetime.strptime(user.get('marked_at'), "%Y-%m-%dT%H:%M:%S.%fZ")
            # validated_at = validated_at.astimezone((datetime.timezone(datetime.timedelta(hours=+9))))
            validated_at = my.strptime(user.get('marked_at'))
            users[user['user']['id']] = {
                'login': user['user']['login'],
                'validated_at': validated_at,
                'flag': var['flag_exam06']
            }
            # if user['user']['login'] == var['test_user']:
            #     print(users[user['user']['id']])
    for user in projectusers_tracen:
        # if user['user']['login'] == var['test_user']:
        #     print(user)
        if user.get('validated?') == True and user['user']['id'] in users:
            if user['teams'][0].get('repo_url') != None \
                and var['domain_name'] in user['teams'][0].get('repo_url'):
                # validated_at = datetime.datetime.strptime(user.get('marked_at'), "%Y-%m-%dT%H:%M:%S.%fZ")
                # validated_at = validated_at.astimezone((datetime.timezone(datetime.timedelta(hours=+9))))
                validated_at = my.strptime(user.get('marked_at'))
                if users[user['user']['id']]['validated_at'] < validated_at:
                    users[user['user']['id']]['validated_at'] = validated_at
                users[user['user']['id']]['flag'] |= var['flag_tracen']
                # if user['user']['login'] == var['test_user']:
                #     print(users[user['user']['id']])
    for user in projectusers_cpc04:
        # if user['user']['login'] == var['test_user']:
        #     print(user)
        if user['user']['id'] in users:
            if user['teams'][0].get('repo_url') != None \
                and var['domain_name'] in user['teams'][0].get('repo_url'):
                users[user['user']['id']]['flag'] |= var['flag_cpc04']
                # if user['user']['login'] == var['test_user']:
                #     print(users[user['user']['id']])
    for user in cursususers:
        # print(user)
        if user['user']['id'] in users and user.get('begin_at') is not None:
            # begin_at = datetime.datetime.strptime(user.get('begin_at'), "%Y-%m-%dT%H:%M:%S.%fZ")
            # begin_at = begin_at.astimezone((datetime.timezone(datetime.timedelta(hours=+9))))
            users[user['user']['id']]['begin_at'] = my.strptime(user.get('begin_at'))
            # print(users[user['user']['id']])

    userlist = list(users.values())
    userlist.sort(key=lambda x: x['validated_at'], reverse=False)
    ret = "login       date        speedrun\n" 
    for user in userlist:
        # if user['login'] == var['test_user']:
        #     print(user)
        if user['flag'] == var['flag_exam06'] | var['flag_tracen'] | var['flag_cpc04']:
            if user.get('begin_at') is None:
                params = {
                    "filter[cursus_id]": cursus_id,
                }
                begin_at = ic.get(f"users/{user['login']}/cursus_users", params=params).json()[0].get('begin_at')
                # begin_at = begin_at.astimezone((datetime.timezone(datetime.timedelta(hours=+9))))
                user['begin_at'] = my.strptime(begin_at)
            n_days = user['validated_at'] - user['begin_at']
            n_days = math.ceil(n_days.days + n_days.seconds / 86400)
            ret += f"{user['login']:10s}  " \
                + f"{datetime.datetime.strftime(user['validated_at'], '%Y-%m-%d')}  " \
                + f"{n_days:-4d} days\n"
    return "```\n" + ret + "```"

def wrapper(args):
    return get_transcenders()

if __name__ == "__main__":
    start_at = datetime.datetime.now()
    print(wrapper(sys.argv))
    finish_at = datetime.datetime.now()
    print(f"Elapsed time: {finish_at - start_at}")
