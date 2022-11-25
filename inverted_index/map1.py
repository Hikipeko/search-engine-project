#!/usr/bin/env python
"""
Map 1.

Input: csv file
Output: doc_id,t_k tab 1
"""

import csv
import sys
import re


# read from input
csv.field_size_limit(sys.maxsize)
docs = csv.reader(sys.stdin.readlines())

# load stopwords
with open('./stopwords.txt', encoding='utf-8') as input_file:
    stopwords = input_file.read().splitlines()

for doc in docs:
    doc_id = int(doc[0])
    # cleaning
    text = doc[1] + ' ' + doc[2]
    text = re.sub(r"[^a-zA-Z0-9 ]+", "", text)
    text = text.casefold()
    words = text.split()
    for word in words:
        if word not in stopwords:
            print(f"{doc_id} {word}\t1")
