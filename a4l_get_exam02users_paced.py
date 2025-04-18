from api42lib import IntraAPIClient
import datetime

quest_name = "CommonCoreRank01"
exam_name = "Exam Rank 02"
kickoff_lower = "2024-10-01T00:00:00Z"
kickoff_upper = "2028-09-30T23:59:59Z"
campus_name = "Tokyo"
cursus_name = "42cursus"
ic = IntraAPIClient(config_path="./config.yml")
quest_id = 45

# quests = ic.pages_threaded("quests")
# for quest in quests:
#     if quest["internal_name"] == quest_name:
#         quest_id = quest["id"]
#         break

params = {
    "filter[name]": campus_name
}
campus_id = ic.get("campus", params=params).json()[0].get("id")

params = {
    "filter[name]": cursus_name
}
cursus_id = ic.get("cursus", params=params).json()[0].get("id")

params = {
    "filter[name]": exam_name
}
proj_id = ic.get("cursus/" + str(cursus_id) + "/projects", params=params).json()[0].get("id")
# projs = ic.pages_threaded("cursus/" + str(cursus_id) + "/projects")
# for proj in projs:
#     if proj["name"] == exam_name:
#         proj_id = proj["id"]
#         break

bh_low = datetime.datetime.now() + datetime.timedelta(days=-1)
bh_high = bh_low + datetime.timedelta(days=+7)

params = {
    "filter[campus_id]": campus_id,
    "range[begin_at]": f"{kickoff_lower},{kickoff_upper}",
    "filter[end_at]": None,
    "sort": "-level",
}

examusers = ""
users = ic.pages_threaded("cursus/" + str(cursus_id) + "/cursus_users", params=params)
for user in users:
    user_id = user["user"]["id"]
    # if user["user"]["end_at"] != None:
    #     continue
    try:
        userquests = ic.pages_threaded("users/" + str(user_id) + "/quests_users")
        if userquests == None or len(userquests) == 0:
            continue
        for userquest in userquests:
            if userquest["quest"]["id"] == quest_id:
                userprojs = ic.pages_threaded("users/" + str(user_id) + "/projects_users")
                for userproj in userprojs:
                    if userproj["project"]["id"] == proj_id:
                        # print(userproj)
                        if userproj["validated?"] == False:
                            examusers += user["user"]["login"] + "\t" + str(user["level"]) + "\t" + user["blackholed_at"] + "\n"
                    break
            break
    except Exception as e:
        print("Error: " + str(e))
        continue
print(examusers)
