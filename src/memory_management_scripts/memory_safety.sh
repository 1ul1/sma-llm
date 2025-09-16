#!/bin/bash

Red='\033[0;31m'
Green='\033[0;32m'
Yellow='\033[0;33m'
NC='\033[0m'

i=0
while true
do
    sleep 0.1
    i=$(($i+1))
    
    #calculate free Mem
    
    # Gather data
    free_pages="$(memory_pressure | grep 'Pages free' | awk '{print $3}')"
    purged_pages="$(memory_pressure | grep 'Pages purged' | awk '{print $3}')"
    inactive_pages="$(memory_pressure | grep 'Pages inactive' | awk '{print $3}')"
    purgeable_pages="$(memory_pressure | grep 'Pages purgeable' | awk '{print $3}')"
    compressed_pages="$(memory_pressure | grep 'Pages compressed' | awk '{print $3}')"
    size_of_page="$(memory_pressure | head -1 | awk '{print $NF}' | tr -d ').')"
    
    # Calculate
    free_pages_total="$(($free_pages+$purgeable_pages+$inactive_pages))"
    free_mem_bytes="$(($free_pages_total*$size_of_page))"
    free_mem="$(($free_mem_bytes/1000000000))"
    quit="$(echo "$free_mem<=6" | bc)"
    if [ "$quit" -eq 1 ]
    then
        echo -e "${Red}$free_mem   ${NC}time:$i"
        ./terminate_model.sh
    else
        echo -e "${Green}$free_mem   ${NC}time:$i"
    fi
done
