#!/bin/bash
ps aux | grep argus > file.txt
NVDAEMON=$(awk '/usr/{print $2}' file.txt)
sudo kill -9 $NVDAEMON
rm file.txt
