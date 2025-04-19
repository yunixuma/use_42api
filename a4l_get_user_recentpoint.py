from api42lib import IntraAPIClient
import datetime, math

ic = IntraAPIClient(config_path="./config.yml")
var = {
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
    "reason": [
		"Earning after defense",
		"Defense plannification",
    ],
    "campus_name": "Tokyo",
    "cursus_name": "42cursus",
    "kickoff_lower": "2020-01-01T00:00:00Z",
    "kickoff_upper": "2024-12-31T23:59:59Z",
    "test_user": "kanahash"
}
date_lower = datetime.datetime.now() + datetime.timedelta(days=-7)
date_upper = date_lower + datetime.timedelta(days=+8)
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

params = {
    "filter[campus_id]": campus_id,
    "range[begin_at]": f'{var["kickoff_lower"]},{var["kickoff_upper"]}',
    # "range[updated_at]": f'{date_lower},{date_upper}',
    "filter[end_at]": None,
    "sort": "-updated_at",
}
users = ic.pages_threaded("cursus/" + str(cursus_id) + "/cursus_users", params=params)
for user in users:
    if datetime.datetime.strptime(user["user"]["updated_at"], '%Y-%m-%dT%H:%M:%S.%fZ') < date_lower:
        continue
    user_id = user["user"]["id"]
    print(user["user"]["login"]) 
    cycle = 0
    try:
        params = {
            "sort": "-id"
            # "filter[quest_id]": quest_id,
            # "filter[validated]": "true",
        }
        recentpoints = ic.pages_threaded("users/" + str(user_id) + "/correction_point_historics")
        if recentpoints == None or len(recentpoints) == 0:
            cycle = 0
        else:
            for recentpoint in recentpoints:
                if datetime.datetime.strptime(recentpoint["updated_at"], '%Y-%m-%dT%H:%M:%S.%fZ') < date_lower:
                    continue
                if recentpoint["reason"] in var["reason"]:
                    continue
                cycle += 1
                if cycle > 5:
                    break
                print(recentpoint)
    except Exception as e:
        print("Error: " + str(e))
        continue
