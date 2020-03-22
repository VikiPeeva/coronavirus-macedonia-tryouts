#!/bin/bash

BASEDIR=$(dirname "$0")
cd $BASEDIR
cwd=$(pwd)


while getopts ":o:i:" opt; do
  case $opt in
    o) OPENDATA_ROOT="$OPTARG"
    ;;
    i) interval="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done


if [ -z "$OPENDATA_ROOT" ]
then
      OPENDATA_ROOT='../../opendata/'
fi
echo The data will be published here: $OPENDATA_ROOT. If you want to change the destination please send the directory as \-o argument.

if [ -z "$interval" ]
then
      interval=1800
fi
echo Starting work cycle every $interval seconds. If you want to change the loop cycle length please send as \-i argument the length \in seconds.

cd $OPENDATA_ROOT
git pull
cd $cwd
python ./update.py $OPENDATA_ROOT
cd $OPENDATA_ROOT
git add .
git status
message="update covid19 $(date)"
git commit -m "$message"
git push
cd $cwd

while [[ ! -f /home/22/job_stop.txt ]] ; do
    now=$(date +%s) # timestamp in seconds
    sleep $((interval - now % interval))
    cd $OPENDATA_ROOT
    git pull
    cd $cwd
    python ./update.py $OPENDATA_ROOT
    cd $OPENDATA_ROOT
    git add .
    git status
    message="update covid19 $(date)"
    git commit -m "$message"
    git push
    cd $cwd
done
