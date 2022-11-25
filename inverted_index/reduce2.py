#!/usr/bin/env python3
"""
idf_k count reducer.

Input: t_k tab doc_id tf_ik
Output: t_k tab idf_k (doc_id tf_ik)*
"""
import sys
import itertools
import math


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def reduce_one_group(key, group):
    """Reduce one group."""
    # Read number of documents in collection C
    with open('./total_document_count.txt', encoding='utf-8') as input_file:
        doc_cnt = int(input_file.read())
    n_k = 0
    output_str = ''
    for line in group:
        output_str += ' '
        output_str += line.partition("\t")[2].strip('\n')
        n_k += 1
    idf_k = math.log10(doc_cnt / n_k)
    print(f"{key}\t{idf_k}{output_str}")


if __name__ == "__main__":
    main()
