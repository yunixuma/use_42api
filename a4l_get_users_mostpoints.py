from api42lib import IntraAPIClient
import sys
import datetime

campus_name = "Tokyo"
cursus_name = "42cursus"
initial_pts = 5

def get_users_hibernated(n_pts = 30):
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
        # "sort": "id"
    }
    users = ic.pages_threaded("cursus/" + str(cursus_id) + "/cursus_users", params=params)

    hit_users = []
    for user in users:
        if (n_pts > initial_pts and user['user'].get('correction_point') > n_pts) \
            or (n_pts <= initial_pts and user['user'].get('correction_point') < n_pts):
            hit_users.append({
                "login": user['user'].get('login'),
                "point": user['user'].get('correction_point'),
                "end_at": user['end_at']
            })
    if len(hit_users) == 0:
        return "No user found with more than " + str(n_pts) + " pts."
    if n_pts > initial_pts:
        hit_users.sort(key=lambda x: x['point'], reverse=True)
    else:
        hit_users.sort(key=lambda x: x['point'], reverse=False)
    ret = "login   \tpts\tend_at\n"
    for user in hit_users:
        ret += f"{user['login']:8s}\t{user['point']:-3d}\t{user['end_at']}\n"
    ret = "```\n" + ret + "```"
    return ret

def wrapper(args) -> str:
    if len(args) > 1:
        n_pts = int(args[1])
    else:
        n_pts = 30
    return get_users_hibernated(n_pts)

if __name__ == "__main__":
    start_at = datetime.datetime.now()
    print(wrapper(sys.argv))
    finish_at = datetime.datetime.now()
    print(f"Elapsed time: {finish_at - start_at}")
