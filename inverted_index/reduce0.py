#!/usr/bin/env python3
"""Reduce 0."""

import sys

doc_count = 0
data = sys.stdin.readlines()
for line in data:
    count = line.partition("\t")[2]
    if not count:
        continue
    doc_count += int(count)
print(doc_count)
