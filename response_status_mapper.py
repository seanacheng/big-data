#!/usr/bin/python
"""response_status_mapper.py"""

import sys

def read_input(file):
    for line in file:
        try:
            words = line.split()
            statusCode = int(words[8])
            if statusCode < 200:
                yield "informational"
            elif statusCode < 300:
                yield "successful"
            elif statusCode < 400:
                yield "redirection"
            elif statusCode < 500:
                yield "client error"
            else:
                yield "server error"
        except:
            continue

def main(separator='\t'):
    data = read_input(sys.stdin)
    for responseStatus in data:
        print('%s%s%d' % (responseStatus, separator, 1))

if __name__ == "__main__":
    main()