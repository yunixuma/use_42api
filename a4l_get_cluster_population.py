
from api42lib import IntraAPIClient
import sys
import datetime
import a4l_get_locations
from collections import namedtuple
import my_common as my

campus_name = "Tokyo"
cursus_name = "42cursus"
quest_name = "CommonCoreValidation"
kickoff_lower = "2020-01-01T00:00:00Z"
kickoff_upper = "2028-09-30T23:59:59Z"

ClusterEvents = namedtuple('ClusterEvents', ['timestamp', 'is_begin', 'host'])

def get_cluster_population(hostname = "c", n_days = 1, begin_at_upper = None, m_days = 1):
    if begin_at_upper == None:
        begin_at_upper = datetime.datetime.now().astimezone(datetime.timezone.utc)
    locations = a4l_get_locations.get_locations(n_days + m_days, begin_at_upper, hostname)
    begin_at_lower = begin_at_upper - datetime.timedelta(days = n_days)

    clus_events = []
    for location in locations:
        end_at = my.datetime_normalize(location['end_at'])
        if end_at == None:
            end_at = begin_at_upper
        elif end_at <= begin_at_lower:
            continue
        clus_events.append(ClusterEvents(end_at, False, location['host']))
        begin_at = my.datetime_normalize(location['begin_at'])
        if begin_at < begin_at_lower:
            begin_at = begin_at_lower
        clus_events.append(ClusterEvents(begin_at, True, location['host']))
        
    clus_events.sort(key=lambda x: x.timestamp, reverse=False)

    pop_hist = [{"timestamp": begin_at_lower, "count": 0}]
    idx = 0
    for clus_event in clus_events:
        print(clus_event)
        if clus_event.timestamp > pop_hist[idx]["timestamp"]:
            pop_hist.append({"timestamp": clus_event.timestamp, "count": pop_hist[idx]["count"]})
            idx += 1
        if clus_event.is_begin:
            pop_hist[idx]["count"] += 1
        else:
            pop_hist[idx]["count"] -= 1
    return pop_hist

def wrapper(args) -> str:
    if len(args) > 1:
        hostname = args[1]
    else:
        hostname = "c"
    if len(args) > 2:
        n_days = int(args[2])
    else:
        n_days = 1
    if len(args) > 3:
        begin_at_upper = datetime.datetime.strptime(args[3], "%Y-%m-%dT%H:%M:%S.%f%z")
    else:
        begin_at_upper = datetime.datetime.now().astimezone(datetime.timezone.utc)
    if len(args) > 4:
        m_days = int(args[4])
    else:
        m_days = 1
    pop_hist = get_cluster_population(hostname, n_days, begin_at_upper, m_days)
    my.save_csv(f"cluster_population_{hostname}_{begin_at_upper}.csv", pop_hist)

if __name__ == "__main__":
    start_at = datetime.datetime.now()
    wrapper(sys.argv)
    finish_at = datetime.datetime.now()
    print(f"Elapsed time: {finish_at - start_at}")
