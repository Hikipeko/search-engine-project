#!/usr/bin/env python3
"""
Normalization calculation reducer.

Input: doc_id tab t_k tf_ik idf_k
Output: doc_id tab |d_i| t_k tf_ik idf_k
"""
import sys
import itertools


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def reduce_one_group(key, group):
    """Reduce one group."""
    term_infos = []
    d_norm = 0.0
    for line in group:
        term_info = line.partition("\t")[2].strip('\n')
        term_infos.append(term_info)
        tf_ik = float(term_info.split()[1])
        idf_k = float(term_info.split()[2])
        d_norm += (tf_ik * tf_ik * idf_k * idf_k)
    for term_info in term_infos:
        print(f"{key}\t{d_norm} {term_info}")


if __name__ == "__main__":
    main()
