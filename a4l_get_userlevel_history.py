
from api42lib import IntraAPIClient
import sys
import datetime
import my_common as my
import a4l_get_userxps

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
    ]
}

def calc_lv(xp):
    for i in range( len(var['xp']) ):
        if xp <= var['xp'][i]['total']:
            break
    return ( xp - var['xp'][i - 1]['total'] ) / (var['xp'][i]['required']) + (i - 1)

def get_userlevel_history(n_days, created_at_upper, user_lst = None):
    userxps = a4l_get_userxps.get_userxps(n_days, created_at_upper, user_lst)
    print(len(userxps))
    userlv_history = {}

    for ux in userxps.items():
        login = ux[0]
        # print(login)
        if user_lst is not None and login not in user_lst:
            continue
        if login not in userlv_history:
            userlv_history[login] = []
        current_xp = 0
        for xp in ux[1]:
            current_xp += xp['xp']
            userlv_history[login].append( {
                'date': xp['created_at'],
                'level': calc_lv(current_xp)
            } )
    return userlv_history

def wrapper(args) -> str:
    if len(args) > 1:
        n_days = int(args[1])
    else:
        n_days = 1
    if len(args) > 2:
        created_at_upper = my.datetime_normalize(args[2])
    else:
        created_at_upper = None
    if len(args) > 3:
        with open(args[3], 'r') as f:
            user_lst = [f.strip() for f in f.readlines()]
        print(len(user_lst))
    else:
        user_lst = None

    userlv_history = get_userlevel_history(n_days, created_at_upper, user_lst)
    if len(args) > 4:
        print(userlv_history)
        my.save_json(userlv_history, args[4])
        return len(userlv_history)
    else:
        return userlv_history

if __name__ == "__main__":
    start_at = datetime.datetime.now()
    print(wrapper(sys.argv))
    finish_at = datetime.datetime.now()
    print(f"Elapsed time: {finish_at - start_at}")
