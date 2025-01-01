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
- ftapi_token.py ...... Get the access token
- ftapi_userinfo.py ... Get the user information
- ftapi_userlist.py ... Get the user list in Tokyo (campus_id: 26) (available to filter by piscine month & cursus)
- ftapi_events.py ..... Get the event list in Tokyo (campus_id: 26)
- ftapi_eventusers.py . Get users who subscribe the event
- ftapi_userevent.py .. Get the event list the user subscribed
- ftapi_scales.py ..... Get the feedback history in Tokyo (campus_id: 26). You can also filter the user determined by user_id
- ftapi_scaled.py ..... Get the evaluated history of user determined by the argument as user_id
- ftapi_slot.py ....... (implementaion not complete)
- ftapi_evals.py ...... (implementaion not complete)
