from api42lib import IntraAPIClient
import sys, datetime

campus_name = "Tokyo"
cursus_name = "42cursus"

def get_criticalusers_bhv2(n_days = 14):
    bh_lower = datetime.datetime.now() + datetime.timedelta(days=-2)
    bh_upper = bh_lower + datetime.timedelta(days= 2 + n_days)

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

    ret = "login   \tlevel\tBH date\n"
    users = ic.pages_threaded("cursus/" + str(cursus_id) + "/cursus_users", params=params)
    # users = ic.pages_threaded("users", params=params)
    for user in users:
        # print(user)
        bh = datetime.datetime.strptime(user['blackholed_at'], '%Y-%m-%dT%H:%M:%S.%f%z')
        ret += f"{user['user']['login']:8s}\t{user['level']:.2f}\t" \
            + bh.strftime('%Y-%m-%d') \
            + f"\t{user['user']['wallet']:-4d}\n"
        # break

    ret = "```\n" + ret + "```" 
    return ret

if __name__ == "__main__":
    start_at = datetime.datetime.now()
    if len(sys.argv) > 1:
        n_days = int(sys.argv[1])
    else:
        n_days = 14
    print(get_criticalusers_bhv2(n_days))
    finish_at = datetime.datetime.now()
    print(f"Elapsed time: {finish_at - start_at}")
