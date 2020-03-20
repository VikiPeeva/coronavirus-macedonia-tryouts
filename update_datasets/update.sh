#!/bin/bash

BASEDIR=$(dirname "$0")
cd $BASEDIR
cwd=$(pwd)
OPENDATA_ROOT=$1

python ./update.py
cd $OPENDATA_ROOT
git add .
git status
message="update covid19 $(date)"
git commit -m "$message"
git push
cd $cwd

interval=1800
while [[ ! -f /home/22/job_stop.txt ]] ; do
    now=$(date +%s) # timestamp in seconds
    sleep $((interval - now % interval))
    python ./update.py
    cd $OPENDATA_ROOT
    git add .
    git status
    message="update covid19 $(date)"
    git commit -m "$message"
    git push
    cd $cwd
done