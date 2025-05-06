#!/usr/bin/env python
"""valence_reducer.py"""

from operator import itemgetter
from itertools import groupby
import sys

def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator, 1)

def main(separator='\t'):
    data = read_mapper_output(sys.stdin, separator=separator)
    for president, group in groupby(data, itemgetter(0)):
        try:
            total_valence = sum(int(valence) for _, valence in group)
            print("%s%s%d" % (president, separator, total_valence / len(data)))
        except ValueError:
            pass


if __name__ == "__main__":
    main()