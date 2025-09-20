#!/bin/bash
# to remove the disk image
rawBlockAddr="$(cat ./Output/disk.txt)"
diskutil unmount force $rawBlockAddr
hdiutil detach $rawBlockAddr
unlink ./Output