from api42lib import IntraAPIClient
import sys, datetime

var = {
    "kickoff_lower": "2021-07-01T00:00:00Z",
    "kickoff_upper": "2028-09-30T23:59:59Z",
    "cursus_name": "42cursus",
    "campus_name": "Tokyo",
    "quest": [
		"CommonCoreRank00",
		"CommonCoreRank01",
		"CommonCoreRank02",
		"CommonCoreRank03",
		"CommonCoreRank04",
		"CommonCoreRank05",
        "CommonCoreValidation"
    ],
    "exam": [
        "Exam Rank 02",
        "Exam Rank 03",
        "Exam Rank 04",
        "Exam Rank 05",
        "Exam Rank 06"
    ]
}

def get_examusers(rank = 2) -> str:
    if rank < 2 or rank > 1 + len(var['exam']):
        print("Rank must be between 2 and 6")
        return

    quest_ids = [44,45,46,47,48,49,37]
    quest_lookup = {}
    for i in range(len(quest_ids)):
        quest_lookup[quest_ids[i]] = i + 1

    ic = IntraAPIClient(config_path="./config.yml")

    # quests = ic.pages_threaded("quests")
    # for quest in quests:
    #     if quest['internal_name'] == quest_name:
    #         quest_id = quest['id']
    #         break
    quest_id = quest_ids[rank - 1]

    params = {
        "filter[name]": var['campus_name']
    }
    campus_id = ic.get("campus", params=params).json()[0].get("id")

    params = {
        "filter[name]": var['cursus_name']
    }
    cursus_id = ic.get("cursus", params=params).json()[0].get("id")

    params = {
        "filter[name]": var['exam'][rank - 2]
    }
    proj_id = ic.get("cursus/" + str(cursus_id) + "/projects", params=params).json()[0].get("id")
    # projs = ic.pages_threaded("cursus/" + str(cursus_id) + "/projects")
    # for proj in projs:
    #     if proj['name'] == exam_name:
    #         proj_id = proj['id']
    #         break

    exam_passed_users = []
    params = {
        "filter[project_id]": proj_id,
        "filter[campus]": campus_id,
        "filter[cursus]": cursus_id
    }
    proj_users = ic.pages_threaded("projects_users", params=params)
    for proj_user in proj_users:
        if proj_user['validated?'] == True:
            exam_passed_users.append(proj_user['user']['id'])

    ms_users = []
    params = {
        "filter[campus_id]": campus_id,
    }
    quests_users = ic.pages_threaded("quests/" + str(quest_id) + "/quests_users", params=params)
    for quest_user in quests_users:
        if quest_user.get("validated_at") != None:
            ms_users.append(quest_user['user']['id'])

    # bh_low = datetime.datetime.now() + datetime.timedelta(days=-1)
    # bh_high = bh_low + datetime.timedelta(days=+7)

    ret = "login   \tlevel\n"

    params = {
        "filter[campus_id]": campus_id,
        "range[begin_at]": f"{var['kickoff_lower']},{var['kickoff_upper']}",
        "filter[end_at]": None,
        "filter[active]": "true",
        "sort": "-level"
    }
    users = ic.pages_threaded("cursus/" + str(cursus_id) + "/cursus_users", params=params)
    for user in users:
        user_id = user['user']['id']
        # if user['user']['end_at'] != None:
        #     continue
        try:
            # userquests = ic.pages_threaded("users/" + str(user_id) + "/quests_users")
            # if userquests == None or len(userquests) == 0:
            #     continue
            # for userquest in userquests:
            #     if userquest['quest']['id'] == quest_id:
            #         userprojs = ic.pages_threaded("users/" + str(user_id) + "/projects_users")
            #         for userproj in userprojs:
            #             if userproj['project']['id'] == proj_id:
            #                 # print(userproj)
            #                 if userproj["validated?"] == False:
            #                     ret += f"{user['user']['login']:8s}\t{user['level']:.2f}\n"
            #             break
            #     break
            if "3b3-" in user['user']['login'] or user_id not in ms_users:
                continue
            if user_id not in exam_passed_users:
                ret += f"{user['user']['login']:8s}\t{user['level']:.2f}\n"
        except Exception as e:
            print("Error: " + str(e))
            continue
    return "```\n" + ret + "```"

def wrapper(args) -> str:
    if len(args) > 1:
        rank = int(args[1])
    else:
        rank = 2
    return get_examusers(rank)

if __name__ == "__main__":
    start_at = datetime.datetime.now()
    print(wrapper())
    finish_at = datetime.datetime.now()
    print(f"Elapsed time: {finish_at - start_at}")
