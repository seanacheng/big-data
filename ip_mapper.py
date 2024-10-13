#!/usr/bin/env python
import sys, re

def main(argv):
    line = sys.stdin.readline()

    log_pattern = r'(.*?) - .*? \[.*?\] "(\w{3,4}?) .*?" (\d{3}) .*'
    pattern = re.compile(log_pattern)

    try:
        while line:
            for match in pattern.findall(line):
                statusCode = int(match[2])
                if statusCode >= 400:
                    ip_addr = str(match[0])
                    print ('LongValueSum:'+ip_addr+'\t'+'1')

            line = sys.stdin.readline()
    except EOFError as error:
        return None


if __name__ == "__main__":
    main(sys.argv)