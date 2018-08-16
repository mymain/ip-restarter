#!/bin/bash
#cronjob setup
#* * * * * ~/ip-restarter/cron.sh > /dev/null 2>&1
if ! screen -list | grep -q "restarter"; then
    # run python script in screen
    echo "off"
    cd ~/ip-restarter && screen -dmS restarter python restarter.py

else
   echo "on"
fi