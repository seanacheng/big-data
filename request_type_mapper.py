#!/usr/bin/env python
import sys, re

def main(argv):
    # (ip_addr, rqst_type, resp_status)
    log_pattern = r'(.*?) - .*? \[.*?\] "(\w{3,4}?) .*?" (\d{3}) .*'

    line = sys.stdin.readline()
    pattern = re.compile(log_pattern)

    try:
        while line:
            for match in pattern.findall(line):
                print ('LongValueSum:'+match[1]+'\t'+'1')

            line = sys.stdin.readline()
    except EOFError as error:
        return None


if __name__ == "__main__":
    main(sys.argv)