#!/bin/sh

# WARNING: This kills first python process it finds, pidof should be adjusted to find this exact script

PROCESS='python'
CMDPATH='.' # set path to hyperion-audio-effects
CMD='python main.py'
HYPERION_ADDR='localhost:20444'

if pidof -s -x $PROCESS > /dev/null
then
    # Killing process
    kill $(pgrep $PROCESS)
    hyperion-remote -c black > /dev/null
    sleep 3;
    hyperion-remote -a $HYPERION_ADDR -c black > /dev/null
    echo "$PROCESS was running. Killed it."
else
    # Starting process
    cd $CMDPATH &&
    $CMD  > /dev/null 2>&1 &
    echo "$PROCESS was not running. Starting $CMD in $CMDPATH."
fi
