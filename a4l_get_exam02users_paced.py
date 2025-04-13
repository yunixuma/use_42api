from api42lib import IntraAPIClient
import datetime

ic = IntraAPIClient(config_path="./config.yml")

campuses = ic.pages_threaded("campus")
for campus in campuses:
    if campus["name"] == "Tokyo":
        campus_id = campus["id"]
        break

cursuses = ic.pages_threaded("cursus")
for cursus in cursuses:
    if cursus["name"] == "42cursus":
        cursus_id = cursus["id"]
        break

quests = ic.pages_threaded("quests")
for quest in quests:
    if quest["internal_name"] == "CommonCoreRank01":
        quest_id = quest["id"]
        break

projs = ic.pages_threaded("cursus/" + str(cursus_id) + "/projects")
for proj in projs:
    if proj["name"] == "Exam Rank 02":
        proj_id = proj["id"]
        break

bh_low = datetime.datetime.now() + datetime.timedelta(days=-1)
bh_high = bh_low + datetime.timedelta(days=+7)

params = {
    "filter[campus_id]": campus_id,
    "range[begin_at]": "2024-10-01T00:00:00Z,2028-09-30T23:59:59Z",
    "filter[end_at]": None,
    "sort": "blackholed_at",
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
                            examusers += user["user"]["login"] + "\t" + user["blackholed_at"] + "\t" + userproj["validated_at"] + "\n"
                    break
            break
    except Exception as e:
        print("Error: " + str(e))
        continue
print(examusers)
