#!/usr/bin/env python
"""Map 0."""

import csv
import sys

csv.field_size_limit(sys.maxsize)
data = sys.stdin.readlines()
print(f"D\t{len(data)}")