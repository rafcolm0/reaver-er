#!/usr/bin/env python
import os


def main():
    file = open('iptabler_rules.txt', 'r')
    lines = file.readlines()
    for i in lines:
        if i[0] != "#":
            print("exec: " + i)
            os.system(i)


if __name__ == '__main__':
    main()
