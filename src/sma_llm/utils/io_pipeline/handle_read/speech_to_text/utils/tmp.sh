#!/bin/bash
# for 50 MB: 50 * 1024 * 1024 / 512 = 102400
rawBlockAddr=$(hdiutil attach -nomount ram://102400)
sleep 1
diskutil erasevolume HFS+ "myRAM" $rawBlockAddr
echo "myRAM created"
echo "/Volumes/myRAM"
ln -s /Volumes/myRAM ./Output
echo "$rawBlockAddr" > ./Output/disk.txt