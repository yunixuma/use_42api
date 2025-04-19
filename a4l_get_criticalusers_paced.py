from api42lib import IntraAPIClient
import datetime, math

ic = IntraAPIClient(config_path="./config.yml")
var = {
    "kickoff_lower": "2024-10-01T00:00:00Z",
    "kickoff_upper": "2024-12-31T23:59:59Z",
    "campus_name": "Tokyo",
    "cursus_name": "42cursus",
    "test_user": "ylinux",
    "xp": [
        {"required":     0, "total":      0},
        {"required":   462, "total":    462},
        {"required":  2226, "total":   2688},
        {"required":  3197, "total":   5885},
        {"required":  5892, "total":  11777},
        {"required": 17440, "total":  29217},
        {"required": 17038, "total":  46255},
        {"required": 17304, "total":  63559},
        {"required": 10781, "total":  74340},
        {"required": 11143, "total":  85483},
        {"required":  9517, "total":  95000},
        {"required": 10577, "total": 105577},
        {"required": 18775, "total": 124352},
        {"required": 21324, "total": 145676},
        {"required": 24136, "total": 169812},
        {"required": 27368, "total": 197180},
        {"required": 31019, "total": 228199},
        {"required": 35134, "total": 263333},
        {"required": 39834, "total": 303167},
        {"required": 45124, "total": 348291},
        {"required": 51126, "total": 399417},
        {"required": 57926, "total": 457343}
    ],
    "pace": [
		{"8":   8, "12":  13, "15":  18, "18":  24,  "22":  30, "24":  45},
		{"8":  32, "12":  48, "15":  60, "18":  72,  "22":  88, "24": 118},
		{"8":  54, "12":  81, "15": 101, "18": 121,  "22": 148, "24": 178},
		{"8":  90, "12": 134, "15": 168, "18": 201,  "22": 246, "24": 306},
		{"8": 141, "12": 211, "15": 264, "18": 316,  "22": 387, "24": 447},
		{"8": 212, "12": 318, "15": 398, "18": 478,  "22": 584, "24": 644},
		{"8": 244, "12": 365, "15": 457, "18": 548,  "22": 670, "24": 730}
   ],
    "quest": [
		"CommonCoreRank00",
		"CommonCoreRank01",
		"CommonCoreRank02",
		"CommonCoreRank03",
		"CommonCoreRank04",
		"CommonCoreRank05",
        "CommonCoreValidation"
    ]
}
bh_lower = datetime.datetime.now() + datetime.timedelta(days=-1)
bh_upper = bh_lower + datetime.timedelta(days=+15)
quest_ids = [44,45,46,47,48,49.37]

# quest_ids = []
# quests = ic.pages_threaded("quests")
# for quest_name in var["quest"]:
#     for quest in quests:
#         # print(quest["internal_name"])
#         if quest["internal_name"] == quest_name:
#             quest_ids += [quest["id"]]
#             print(quest["internal_name"] + "\t" + str(quest["id"]))
#             break

# campuses = ic.pages_threaded("campus")
# for campus in campuses:
#     if campus["name"] == "Tokyo":
#         campus_id = campus["id"]
#         break
params = {
    "filter[name]": var["campus_name"],
}
campus_id = ic.get("campus", params=params).json()[0].get("id")

# cursuses = ic.pages_threaded("cursus")
# for cursus in cursuses:
#     if cursus["name"] == cursus_name:
#         cursus_id = cursus["id"]
#         break
params = {
    "filter[name]": var["cursus_name"],
}
cursus_id = ic.get("cursus", params=params).json()[0].get("id")


user_id = ic.get("users/" + var["test_user"]).json()["id"]
params = {
    # "filter[campus_id]": campus_id,
    # "filter[cursus_id]": cursus_id,
    "filter[user_id]": user_id,
    # "range[begin_at]": f'{var["kickoff_lower"]},{var["kickoff_upper"]}',
    # "filter[end_at]": None,
    # "sort": "blackholed_at",
}
user = ic.get("cursus/" + str(cursus_id) + "/cursus_users", params=params).json()[0]
print(user["user"]["login"] + "\t" + str(user["level"]) + "\t" + str(user["blackholed_at"]))
milestone = 0
params = {
    # "filter[quest_id]": quest_id,
    "filter[validated]": "true",
}
userquests = ic.pages_threaded("users/" + str(user_id) + "/quests_users")
if userquests == None or len(userquests) == 0:
    milestone = 0
else:
    for userquest in userquests:
        # print(userquest)
        print(userquest["quest"]["name"] + "\t" + str(userquest.get("validated_at")))
        if userquest["quest"]["id"] in quest_ids:
            if userquest.get("validated_at") != None:
                milestone += 1
# user["user"]["level"] = 
xp = var["xp"][math.floor(user["level"])]["total"] + (user["level"] - math.floor(user["level"])) * var["xp"][math.ceil(user["level"])]["required"]
bh = datetime.datetime.strptime(user["blackholed_at"], '%Y-%m-%dT%H:%M:%S.000Z') + datetime.timedelta(days = -math.floor((xp/49980) ** 0.45 * 483) - 77 + var["pace"][milestone]["24"])
print(user["user"]["login"] + "\t" \
    + str(milestone) + "\t" \
    + str(user["level"]) + "\t" \
    + str(bh) + "\t" \
    + str(xp))


criticalusers = ""
params = {
    "filter[campus_id]": campus_id,
    "range[begin_at]": f'{var["kickoff_lower"]},{var["kickoff_upper"]}',
    "filter[end_at]": None,
    "sort": "blackholed_at",
}
users = ic.pages_threaded("cursus/" + str(cursus_id) + "/cursus_users", params=params)
for user in users:
    user_id = user["user"]["id"]
    # print(user["user"]["login"] + "\t" + str(user["level"]) + "\t" + str(user["blackholed_at"]))
    milestone = 0
    xp = 0
    bh = "1970-01-01T00:00:00Z"
    try:
        params = {
            # "filter[quest_id]": quest_id,
            "filter[validated]": "true",
        }
        userquests = ic.pages_threaded("users/" + str(user_id) + "/quests_users")
        if userquests == None or len(userquests) == 0:
            milestone = 0
        else:
            for userquest in userquests:
                if userquest["quest"]["id"] in quest_ids:
                    if userquest.get("validated_at") != None:
                        milestone += 1
        # user["user"]["level"] = 
        xp = var["xp"][math.floor(user["level"])]["total"] + (user["level"] - math.floor(user["level"])) * var["xp"][math.ceil(user["level"])]["required"]
        bh = datetime.datetime.strptime(user["blackholed_at"], '%Y-%m-%dT%H:%M:%S.000Z') + datetime.timedelta(days = -math.floor((xp/49980) ** 0.45 * 483) - 77 + var["pace"][milestone]["24"])
        if bh_lower < bh < bh_upper:
            criticalusers += user["user"]["login"] + "\t" + str(milestone) + "\t" \
                + str(user["level"]) + "\t" + str(bh) + "\n"
    except Exception as e:
        print("Error: " + str(e))
        continue
print(criticalusers)
