from api42lib import IntraAPIClient
import datetime

ic = IntraAPIClient(config_path="./config.yml")

campuses = ic.pages_threaded("campus")
for campus in campuses:
    # print(campus)
    # print('Campus name: ' + campus['name'])
    # print('Campus ID: ' + str(campus['id']))
    if campus["name"] == "Tokyo":
        campus_id = campus["id"]
        break

cursuses = ic.pages_threaded("cursus")
for cursus in cursuses:
    # print(cursus)
    # print('Cursus name: ' + cursus['name'])
    # print('Cursus ID: ' + str(cursus['id']))
    if cursus["name"] == "42cursus":
        cursus_id = cursus["id"]
        break
# cursus_id = 21

bh_low = datetime.datetime.now() + datetime.timedelta(days=-1)
bh_high = bh_low + datetime.timedelta(days=+7)

params = {
    "filter[campus_id]": campus_id,
    "range[begin_at]": "2019-10-01T00:00:00Z,2024-09-30T23:59:59Z",
    "range[blackholed_at]": f"{bh_low},{bh_high}",
    "filter[end_at]": None,
    "sort": "blackholed_at",
    # "filter[cursus_id]": cursus_id,
    # "page[size]": 100,
}

users = ic.pages_threaded("cursus/" + str(cursus_id) + "/cursus_users", params=params)
# users = ic.pages_threaded("users", params=params)
for user in users:
    # print(user)
    print(user["user"]["login"] + "\t" + str(user["blackholed_at"]))
    # break

# freezes = ic.pages_threaded("freeze/v2/freezes")
# for freeze in freezes:
#     print(freeze["id"])
