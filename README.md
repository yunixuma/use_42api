# use_42api
Python scripts to use 42 API

## Preparation
1. Install git and Python (v3.10 or above).
2. Clone the repository into anywhere you like.
3. Rename the file `.env_sample` to `.env` and replace the values of `FT_UID` and `FT_SECRET` for yours.

## Usage
1. Run the python script with an argument if required.
2. Open the log file put out `data` directory by default.

## Script list
- ftapi_token.py .......... Get the access token
- ftapi_userinfo.py ....... Get the user information
- ftapi_userlist.py ....... Get the user list in Tokyo (campus_id: 26) (available to filter by piscine month & cursus)
- ftapi_events.py ......... Get the event list in Tokyo (campus_id: 26)
- ftapi_eventusers.py ..... Get users who subscribe the event
- ftapi_userevent.py ...... Get the event list the user subscribed
- ftapi_scales.py ......... Get the feedback history in Tokyo (campus_id: 26). You can also filter the user determined by user_id
- ftapi_scaled.py ......... Get the evaluated history of user determined by the argument as user_id
- ftapi_userlocation.py ... Get the host list the user logged in
- ftapi_slot.py ........... (implementaion not complete)
- ftapi_evals.py .......... (implementaion not complete)

## Example
- If you want to get the users who took Piscine on March 2021 and entered 42cursus
Run `ftapi_userlist.py` with `pool_year` and `pool_month`.
```
> python3 ftapi_userlist.py 2021 march
> ls -l ./data/userlist
total 24
-rw-r--r-- 1 bill bill 21057 Jan  2 01:14 users_2021-march_20250102T0114.json
```

- If you want to get the users who took Piscine on March 2021 (whether passed or failed)
Run `ftapi_userlist.py` with `pool_year`, `pool_month` and `cursus_id` of C Piscine.
```
> python3 ftapi_userlist.py 2021 march 9
> ls -l ./data/userlist
total 52
-rw-r--r-- 1 bill bill 21057 Jan  2 01:14 users_2021-march_20250102T0114.json
-rw-r--r-- 1 bill bill 26284 Jan  2 01:13 users_2021-march_cursus9_20250102T0113.json
```

- If you want to get the user list who subscribed the specified event
Run `ftapi_eventusers.py` with `event_id`.
```
> python3 ftapi_eventusers.py 7459
> ls -l ./data/eventusers
total 456
-rw-r--r-- 1 bill bill 462903 Jan  2 02:27 event_7459_20250102T0227.jsonjson
```
