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
        print(group_list)
        group_size = len(group_list)
        try:
            total_valence = sum(int(valence) for _, valence in group)
            print(total_valence)
            avg_valence = total_valence / group_size
            print(president + '\t' + avg_valence)
        except ValueError:
            pass


if __name__ == "__main__":
    main()