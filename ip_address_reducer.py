#!/usr/bin/python
"""ip_address_reducer.py"""

from operator import itemgetter
from itertools import groupby
import sys

def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator, 1)

def main(separator='\t'):
    word_counts = []
    data = read_mapper_output(sys.stdin, separator=separator)
    for current_word, group in groupby(data, itemgetter(0)):
        try:
            total_count = sum(int(count) for current_word, count in group)
            word_counts.append((current_word, total_count))
        except ValueError:
            pass

    word_counts.sort(key=itemgetter(1), reverse=True)
    for word, count in word_counts[:5]:
        print(f"{word}{separator}{count}")

if __name__ == "__main__":
    main()