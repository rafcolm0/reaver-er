# reaver-er
Automates reaver+pixie-dust attacks on surrounding WPS-capable routers.

Required Argument:
	-i, --interface=<wlan>          Name of the monitor-mode interface

Example:
	reaver-er -i mon0 

REQUIRES: 
-input interface to be already in MONITOR MODE (use airmon-ng for that)
-needs to be run as sudo
-airodump-ng (with WPS feature; version 1.2 & up)
-reaver
-pixie-dust

DISCLAIMER: the way the stdouts, stderrs and pipes are handled could posibly be improved and done in fewer lines of code. Not too worried about that for the moment, as long as the script works.
