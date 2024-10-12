#!/usr/bin/env python
"""request_type_mapper.py"""

import sys

def read_input(file):
    for line in file:
        try:
            words = line.split(" ")
            yield words[5].strip('"')
        except:
            continue

def main():
    data = read_input(sys.stdin.readlines())
    for requestType in data:
        print("LongValueSum:" + requestType + "\t" + "1")

if __name__ == "__main__":
    main()