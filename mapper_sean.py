#!/usr/bin/env python
import sys, re

def main(argv):
    row_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(.*?)\] "(.*?)" (\d{3})'

    log_line = sys.stdin.readline()
    log_linecount = 0
    pattern = re.compile(row_pattern)

    try:
        while log_line:

            log_linecount += 1
            for matches_tuple in pattern.findall(log_line):
                if len(matches_tuple) > 3:
                    matches_list = list(matches_tuple)[1:]
                    ip_addr = matches_tuple[0].split()[0].strip()
                    dt_time = matches_tuple[1].split()[0].strip()
                    rq_type = matches_tuple[2].split()[0].strip()
                    er_code = matches_tuple[3][0]
                    print ('LongValueSum:'+str(rq_type)+'\t'+'1')

            log_line = sys.stdin.readline()
    except EOFError as error:
        return None


if __name__ == "__main__":
    main(sys.argv)