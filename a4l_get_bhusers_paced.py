from api42lib import IntraAPIClient
import datetime

campus_name = "Tokyo"
cursus_name = "42cursus"
kickoff_lower = "2024-10-01T00:00:00Z"
kickoff_upper = "2028-09-30T23:59:59Z"

ic = IntraAPIClient(config_path="./config.yml")

params = {
    "filter[name]": campus_name
}
campus_id = ic.get("campus", params=params).json()[0].get("id")

params = {
    "filter[name]": cursus_name
}
cursus_id = ic.get("cursus", params=params).json()[0].get("id")

bh_upper = datetime.datetime.now()
params = {
    "filter[campus_id]": campus_id,
    "range[begin_at]": f"{kickoff_lower},{kickoff_upper}",
    "range[end_at]": f"{kickoff_lower},{bh_upper}",
    "sort": "end_at",
}

users = ic.pages_threaded("cursus/" + str(cursus_id) + "/cursus_users", params=params)
for user in users:
    print(user["user"]["login"] + "\t" + str(user["end_at"]))
