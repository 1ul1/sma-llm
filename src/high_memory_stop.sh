#!/bin/bash
while true
do
    sleep 1
    mem="$(ps aux | grep sma_llm.main.my_main | grep -v grep | awk '{print $4}')"
    echo "$mem"
    stop="$(echo "$mem >= 70" | bc)"
    if [ "$stop" -eq 1 ]
    then
        pid="$(ps aux | grep sma_llm.main.my_main | grep -v grep | awk '{print $2}')"
        kill "$pid"
    fi
done
