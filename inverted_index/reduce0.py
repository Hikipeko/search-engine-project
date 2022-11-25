#!/usr/bin/env python3
"""Reduce 0."""

import sys


def main():
    """Doc count."""
    doc_count = 0
    for line in sys.stdin.readlines():
        count = line.partition("\t")[2]
        doc_count += int(count)
    print(doc_count)


if __name__ == "__main__":
    main()
