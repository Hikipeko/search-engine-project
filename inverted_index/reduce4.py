#!/usr/bin/env python3
"""
Normalization calculation reducer.

Input: partition tab t_k idf_k d_i tf_ik |di|
Output: t_k idf_k (d_i tf_ik |di|)*
"""
import sys
import itertools


def main():
    """Divide sorted lines into groups that share a key."""
    for _, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(group)


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    # t_k is the key
    return line.partition("\t")[2].split()[0]


def reduce_one_group(group):
    """Reduce one group."""
    idf_k = 0.0
    output = ''
    for line in group:
        info = line.partition("\t")[2].strip('\n')
        term = info.split()[0]
        idf_k = info.split()[1]
        output += ' '
        output += info.partition(' ')[2].partition(' ')[2]
    print(f"{term} {idf_k} {output}")


if __name__ == "__main__":
    main()
