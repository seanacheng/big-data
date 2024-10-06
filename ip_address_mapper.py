#!/usr/bin/python
"""ip_address_mapper.py"""

import sys

def read_input(file):
    for line in file:
        try:
            words = line.split()
            if int(words[8]) >= 400:
                yield words[0]
        except:
            continue

def main(separator='\t'):
    data = read_input(sys.stdin)
    for ipAddress in data:
        print('%s%s%d' % (ipAddress, separator, 1))

if __name__ == "__main__":
    main()