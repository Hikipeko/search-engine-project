#!/usr/bin/env python
"""
Map 3.

Input: t_k tab idf_k (doc_id tf_ik)*
Output: doc_id tab t_k tf_ik idf_k
"""

import sys

for line in sys.stdin.readlines():
    term = line.partition('\t')[0]
    idf_docs = line.partition('\t')[2].split()
    idf_k = idf_docs.pop(0)
    for i in range(len(idf_docs) // 2):
        doc_id = int(idf_docs[2 * i])
        tf_ik = int(idf_docs[2 * i + 1])
        print(f"{doc_id}\t{term} {tf_ik} {idf_k}")
