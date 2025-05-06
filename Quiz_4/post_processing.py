"""post_processing.py"""
import sys

total_words = 0
request_counts = []

# Read in the reducer output
for line in sys.stdin:
    line = line.strip()
    word, count = line.split('\t', 1)
    count = int(count)
    total_words += count

print(f"total wordcount: {total_words}")
