#!/bin/bash
i=0
echo -e "time,used_ram"
while true
do
    # time intervals for measure in seconds
    delta_t=0.1
    sleep $delta_t
    i=$(echo "$i+$delta_t" | bc)
    
    #calculate free Mem
    
    # Gather data
    free_pages="$(memory_pressure | grep 'Pages free' | awk '{print $3}')"
    purged_pages="$(memory_pressure | grep 'Pages purged' | awk '{print $3}')"
    inactive_pages="$(memory_pressure | grep 'Pages inactive' | awk '{print $3}')"
    purgeable_pages="$(memory_pressure | grep 'Pages purgeable' | awk '{print $3}')"
    compressed_pages="$(memory_pressure | grep 'Pages compressed' | awk '{print $3}')"
    size_of_page="$(memory_pressure | head -1 | awk '{print $NF}' | tr -d ').')"
    
    # Calculate
    free_pages_total="$(echo "$(($free_pages+$inactive_pages))")"
    free_mem_bytes="$(echo "$(($free_pages_total*$size_of_page))")"
    # bc here so it doesnt approximate result, also scale to select precision
    free_mem="$(echo "scale=3; $free_mem_bytes/1000000000" | bc)"
    used_mem="$(echo "24-$free_mem-3" | bc)"

    # CVS format
    echo -e "$i,$used_mem"
done
