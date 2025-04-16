from api42lib import IntraAPIClient
import datetime

ic = IntraAPIClient(config_path="./config.yml")
var = {
    "xp": [
        {"required":     0, "total":      0},
        {"required":   462, "total":    462},
        {"required":  2226, "total":   2688},
        {"required":   462, "total":    462},
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
        "CommonCoreRank06"
    ]
}

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

quest_ids = []
quests = ic.pages_threaded("quests")
for quest_name in var["quest"]:
    for quest in quests:
        if quest["internal_name"] == quest_name:
            quest_ids += quest["id"]
            break

bh_low = datetime.datetime.now() + datetime.timedelta(days=-1)
bh_high = bh_low + datetime.timedelta(days=+7)

params = {
    "filter[campus_id]": campus_id,
    "range[begin_at]": "2024-10-01T00:00:00Z,2028-09-30T23:59:59Z",
    "filter[end_at]": None,
    "sort": "blackholed_at",
}

criticalusers = ""
users = ic.pages_threaded("cursus/" + str(cursus_id) + "/cursus_users", params=params)
for user in users:
    user_id = user["user"]["id"]
    print(user["user"]["login"] + "\t" + str(user["level"]) + "\t" + str(user["blackholed_at"]))
    milestone = 0
    try:
        userquests = ic.pages_threaded("users/" + str(user_id) + "/quests_users")
        if userquests == None or len(userquests) == 0:
            milestone = 0
        else:
            for userquest in userquests:
                if userquest["quest"]["id"] in quest_ids:
                    milestone += 1
        user["user"]["level"] = 
    except Exception as e:
        print("Error: " + str(e))
        continue
print(criticalusers)
