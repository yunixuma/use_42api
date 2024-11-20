#!/bin/bash

cd `dirname $0`
python3 ./`basename $0 .sh`.py
# curl -X POST --data "grant_type=client_credentials&client_id=$FT_UID&client_secret=$FT_SECRET" $URL_TOKEN
