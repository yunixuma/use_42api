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
    "test_user": "ykosaka"
}

def get_transcenders():
    ic = IntraAPIClient(config_path="./config.yml")

    params = {
        "filter[name]": var['campus_name'],
    }
    campus_id = ic.get("campus", params=params).json()[0].get("id")

    params = {
        "filter[campus]": campus_id,
    }
    projectusers_tracen = ic.pages_threaded("projects/1337/projects_users", params=params)
    projectusers_exam06 = ic.pages_threaded("projects/1324/projects_users", params=params)
    projectusers_cpc04 = ic.pages_threaded("projects/1261/projects_users", params=params)

    users = {}
    for user in projectusers_exam06:
        # if user['user']['login'] == var['test_user']:
        #     print(user)
        if user.get('validated?') == True:
            validated_at = datetime.datetime.strptime(user.get('marked_at'), "%Y-%m-%dT%H:%M:%S.%fZ")
            validated_at = validated_at.astimezone((datetime.timezone(datetime.timedelta(hours=+9))))
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
                validated_at = datetime.datetime.strptime(user.get('marked_at'), "%Y-%m-%dT%H:%M:%S.%fZ")
                validated_at = validated_at.astimezone((datetime.timezone(datetime.timedelta(hours=+9))))
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

    userlist = list(users.values())
    userlist.sort(key=lambda x: x['validated_at'], reverse=False)
    ret = "login   \tvalidated_at\n" 
    for user in userlist:
        if user['login'] == var['test_user']:
            print(user)
        if user['flag'] == var['flag_cpc04'] | var['flag_exam06'] | var['flag_tracen']:
            ret += f"{user['login']:8s}\t" \
                + f"{datetime.datetime.strftime(userlist[id]['validated_at'], '%Y-%m-%d')}\n"
    return "```\n" + ret + "```"

def wrapper(args):
    return get_transcenders()

if __name__ == "__main__":
    start_at = datetime.datetime.now()
    print(wrapper(sys.argv))
    finish_at = datetime.datetime.now()
    print(f"Elapsed time: {finish_at - start_at}")
