#!/usr/bin/env python
import sys, re

def main(argv):
    log_pattern = r'(.*?) - .*? \[.*?\] "(\w{3,4}?) .*?" (\d{3}) .*'

    line = sys.stdin.readline()
    pattern = re.compile(log_pattern)

    try:
        while line:
            for match in pattern.findall(line):
                print("match:"+str(match))
                matches_list = list(match)
                print("matches_list:"+str(matches_list))
                ip_addr = match[0]
                rq_type = match[1]
                er_code = match[2]
                print ('LongValueSum:'+rq_type+'\t'+'1')

            line = sys.stdin.readline()
    except EOFError as error:
        return None


if __name__ == "__main__":
    main(sys.argv)