from api42lib import IntraAPIClient
import datetime

campus_name = "Tokyo"
cursus_name = "42cursus"
bh_lower = datetime.datetime.now() + datetime.timedelta(days=-1)
bh_upper = bh_lower + datetime.timedelta(days=+8)
ic = IntraAPIClient(config_path="./config.yml")

params = {
    "filter[name]": campus_name
}
campus_id = ic.get("campus", params=params).json()[0].get("id")

params = {
    "filter[name]": cursus_name
}
cursus_id = ic.get("cursus", params=params).json()[0].get("id")

params = {
    "filter[campus_id]": campus_id,
    "range[begin_at]": "2019-10-01T00:00:00Z,2024-09-30T23:59:59Z",
    "range[blackholed_at]": f"{bh_lower},{bh_upper}",
    "filter[end_at]": None,
    "sort": "blackholed_at",
    # "filter[cursus_id]": cursus_id,
    # "page[size]": 100,
}

users = ic.pages_threaded("cursus/" + str(cursus_id) + "/cursus_users", params=params)
# users = ic.pages_threaded("users", params=params)
for user in users:
    # print(user)
    bh = datetime.datetime.strptime(user["blackholed_at"], '%Y-%m-%dT%H:%M:%S.%f%z')
    print(user["user"]["login"] + "\t" \
        + str(bh.astimezone(datetime.timezone(datetime.timedelta(hours=+9)))))
    # break

# freezes = ic.pages_threaded("freeze/v2/freezes")
# for freeze in freezes:
#     print(freeze["id"])
