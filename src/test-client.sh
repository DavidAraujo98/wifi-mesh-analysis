#!/bin/bash

# Usage example: ./test-client.sh <IP> <PORT> <RESULTS DIRECTORY NAME>

IP=$1
PORT=$2
TESTDIR=$3

mkdir $TESTDIR

iperf3 -c $IP -t 60 --timestamps -p $PORT -P 3 -bidir -J > "$TESTDIR/test.json"

python3 jsonDigest.py --csv "$TESTDIR/test.json" $TESTDIR/results.csv