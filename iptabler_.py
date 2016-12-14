#!/usr/bin/env python
import os
import sys

def main():
    if len(sys.argv) != 2:
        print("Script that adds iptables listed on a formated file.\n\nRequired Argument:\n     <file>          Path of file containing rules \n\n Example: \n    pyhton3 iptabler_ iptable_rules.txt")
        sys.exit()
    RULES = sys.argv[1]
    try:
        file = open(RULES, 'r')
        lines = file.readlines()
        for i in lines:
            if i[0] != "#":
                print("exec: " + i)
                os.system(i)
    except OSError as e:
        print("Script that adds iptables listed on a formated file.\n\nRequired Argument:\n     <file>          Path of file containing rules \n\n Example: \n    pyhton3 iptabler_ iptable_rules.txt")
        sys.exit()


if __name__ == '__main__':
    main()
