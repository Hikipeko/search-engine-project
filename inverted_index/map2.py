#!/usr/bin/env python
"""
Map 2.

Input: doc_id t_k tab tf_ik
Output: t_k tab doc_id tf_ik
"""

import sys

for doc_term_tf in sys.stdin.readlines():
    doc_term = doc_term_tf.partition('\t')[0]
    tf_ik = int(doc_term_tf.partition('\t')[2])
    doc_id = doc_term.split()[0]
    t_k = doc_term.split()[1]
    print(f"{t_k}\t{doc_id} {tf_ik}")
