
from api42lib import IntraAPIClient
import sys
import datetime
import my_common as my

campus_name = "Tokyo"
cursus_name = "42cursus"
quest_name = "CommonCoreValidation"
kickoff_lower = "2020-01-01T00:00:00Z"
kickoff_upper = "2028-09-30T23:59:59Z"

def get_scaleteams(n_days = 1, begin_at_upper = None):
    if begin_at_upper == None:
        begin_at_upper = datetime.datetime.now().astimezone(datetime.timezone.utc)
    begin_at_lower = begin_at_upper - datetime.timedelta(days = n_days)
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
        "filter[cursus_id]": cursus_id,
        "range[begin_at]": f"{begin_at_lower},{begin_at_upper}"
    }
    scaleteams = ic.pages_threaded("scale_teams", params=params)
    return scaleteams

def get_most_reviewers(n_days, begin_at_upper, user_lst = None):
    scaleteams = get_scaleteams(n_days, begin_at_upper)
    print(len(scaleteams))
    reviewer_count = {}
    for scaleteam in scaleteams:
        # print(scaleteam)
        if 'corrector' in scaleteam and scaleteam['corrector'].get("login"):
            reviewer = scaleteam['corrector']['login']
            if user_lst is not None and reviewer not in user_lst:
                continue
            if reviewer not in reviewer_count:
                reviewer_count[reviewer] = 0
            reviewer_count[reviewer] += 1
    sorted_reviewers = sorted(reviewer_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_reviewers

def wrapper(args) -> str:
    if len(args) > 1:
        n_days = int(args[1])
    else:
        n_days = 1
    if len(args) > 2:
        begin_at_upper = my.datetime_normalize(args[2])
    else:
        begin_at_upper = None
    if len(args) > 3:
        with open(args[3], 'r') as f:
            user_lst = [f.strip() for f in f.readlines()]
    else:
        user_lst = None

    reviewers_tuples = get_most_reviewers(n_days, begin_at_upper, user_lst)
    if len(args) > 4:
        reviewers_dicts = [
            {'login': r[0], 'count': r[1]} for r in reviewers_tuples
        ]
        my.save_csv(reviewers_dicts, args[4])
        return len(reviewers_dicts)
    else:
        return reviewers_tuples

if __name__ == "__main__":
    start_at = datetime.datetime.now()
    print(wrapper(sys.argv))
    finish_at = datetime.datetime.now()
    print(f"Elapsed time: {finish_at - start_at}")
