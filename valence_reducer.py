#!/usr/bin/env python
"""valence_reducer.py"""

from operator import itemgetter
from itertools import groupby
import sys

def read_mapper_output(file):
    for line in file:
        yield line.rstrip().split('\t', 1)

def main():
    data = read_mapper_output(sys.stdin)
    for president, group in groupby(data, itemgetter(0)):
        group_list = list(group)
        group_size = len(group_list)
        total_valence = sum(int(valence) for _, valence in group_list)
        avg_valence = total_valence / group_size
        print(president + '\t' + str(avg_valence))


if __name__ == "__main__":
    main()