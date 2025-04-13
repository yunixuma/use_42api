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

bh_high = datetime.datetime.now()

params = {
    "filter[campus_id]": campus_id,
    "range[begin_at]": "2024-10-01T00:00:00Z,2028-09-30T23:59:59Z",
    "range[end_at]": f"2024-10-01T00:00:00Z,{bh_high}",
    "sort": "end_at",
}

users = ic.pages_threaded("cursus/" + str(cursus_id) + "/cursus_users", params=params)
for user in users:
    print(user["user"]["login"] + "\t" + str(user["end_at"]))
