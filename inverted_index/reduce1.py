#!/usr/bin/env python3
"""
tf_ik coundt reducer.

Input: doc_id,t_k tab 1
Output: doc_id t_k tab tf_ik
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
    word_count = 0
    for line in group:
        count = line.partition("\t")[2]
        word_count += int(count)
    print(f"{key}\t{word_count}")


if __name__ == "__main__":
    main()
