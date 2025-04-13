from api42lib import IntraAPIClient

ic = IntraAPIClient(config_path="./config.yml")

campuses = ic.pages_threaded("campus")
for campus in campuses:
    print(campus)
    print('Campus name: ' + campus['name'])
    print('Campus ID: ' + str(campus['id']))
    break

cursuses = ic.pages_threaded("cursus")
for cursus in cursuses:
    print(cursus)
    print('Cursus name: ' + cursus['name'])
    print('Cursus ID: ' + str(cursus['id']))
    break

cursus_id = 21

params = {
    "filter[campus_id]": 26,
    "range[begin_at]": "2024-10-01T00:00:00Z,2025-03-31T23:59:59Z",
    "range[blackholed_at]": "2025-04-15T00:00:00Z,2025-04-24T23:59:59Z"
    # "filter[cursus_id]": 21,
    # "page[size]": 100,
}

users = ic.pages_threaded("cursus/" + str(cursus_id) + "/cursus_users", params=params)
# users = ic.pages_threaded("users", params=params)
for user in users:
    # print(user)
    print(user["user"]["login"])
    # break

# freezes = ic.pages_threaded("freeze/v2/freezes")
# for freeze in freezes:
#     print(freeze["id"])
