#!/usr/bin/env python
"""
Map 4.

Input: doc_id tab |d_i| t_k tf_ik idf_k
Output: partition tab t_k idf_k d_i tf_ik |di|
"""

import sys

for line in sys.stdin.readlines():
    doc_id = int(line.partition('\t')[0])
    info = line.partition('\t')[2].split()
    d_norm = info[0]
    t_k = info[1]
    tf_ik = info[2]
    idf_k = info[3]
    print(f"{doc_id % 3}\t{t_k} {idf_k} {doc_id} {tf_ik} {d_norm}")
