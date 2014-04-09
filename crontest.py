#! /usr/bin/python

# to edit cron processes
# crontab -e

from time import strftime

with open("crontest.out",'a') as out:
    out.write("[success] @ "+ strftime("%Y-%m-%d %H:%M:%S") + "\n")

