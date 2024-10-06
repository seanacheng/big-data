#!/usr/bin/python
"""request_type_mapper.py"""

import sys

def read_input(file):
    for line in file:
        try:
            words = line.split()
            yield words[5].strip('"')
        except:
            continue

def main(separator='\t'):
    data = read_input(sys.stdin)
    for requestType in data:
        print('%s%s%d' % (requestType, separator, 1))

if __name__ == "__main__":
    main()