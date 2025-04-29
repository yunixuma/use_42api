from api42lib import IntraAPIClient
import sys, datetime

start_at = datetime.datetime.now()
campus_name = "Tokyo"
cursus_name = "42cursus"
kickoff_lower = "2024-10-01T00:00:00Z"
kickoff_upper = "2028-09-30T23:59:59Z"

def get_bhusers_paced():
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

    ret = "login   \tend_at\n"
    users = ic.pages_threaded("cursus/" + str(cursus_id) + "/cursus_users", params=params)
    for user in users:
        ret += f"{user['user']['login']}\t{user['end_at']}\n"
    return "```\n" + ret + "```"

def wrapper(args) -> str:
    return get_bhusers_paced()

if __name__ == "__main__":
    start_at = datetime.datetime.now()
    print(wrapper(sys.argv))
    finish_at = datetime.datetime.now()
    print(f"Elapsed time: {finish_at - start_at}")
