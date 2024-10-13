#!/usr/bin/env python
import sys, re

def main(argv):
    line = sys.stdin.readline()

    log_pattern = r'(.*?) - .*? \[.*?\] "(\w{3,4}?) .*?" (\d{3}) .*'
    pattern = re.compile(log_pattern)

    try:
        while line:
            for match in pattern.findall(line):
                try:
                    rq_type = match[1]
                    print ('LongValueSum:'+str(rq_type)+'\t'+'1')
                except:
                    continue

            line = sys.stdin.readline()
    except EOFError as error:
        return None


if __name__ == "__main__":
    main(sys.argv)