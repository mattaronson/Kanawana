#!/usr/bin/env python3
"""Decode OCR text produced from a page scanned 180 degrees rotated.

The OCR engine read rotated glyphs and substituted visually similar upright
characters. Recovery = reverse each line, then map each character back through
a rotation look-alike table. Several rotations are genuinely ambiguous
(rotated 'b' and rotated 'q' both read as 'b'; rotated 'a' reads as 'e', 'B'
or 'q'), so the output is a degraded but human-readable text, NOT a faithful
transcript. Anything quoted from it must be flagged as such.
"""
import sys

M = {
    '!': 't', '1': 't', 'b': 'h', 'q': 'b', 'd': 'p', 'p': 'd',
    'u': 'n', 'n': 'u', 'a': 'e', 'e': 'a', 'J': 'r', 'j': 'r',
    '|': 'l', 'X': 'y', 'A': 'y', 'V': 'A', 'y': 'v', 'm': 'w',
    'w': 'm', 'M': 'W', 'W': 'M', '^': 'v', '0': 'o', '6': 'g',
    'B': 'a', '3': 'E', 'U': 'n', 'h': 'a', 'O': 'C',
    '9': '6', '$': 's', '\\': '/', '/': '\\',
    '(': ')', ')': '(', '[': ']', ']': '[', '<': '>', '>': '<',
}

def decode(line: str) -> str:
    out = ''.join(M.get(c, c) for c in reversed(line.rstrip('\n')))
    # the engine splits a rotated 'm' into two strokes
    return out.replace('nn', 'm').replace('NN', 'M')

if __name__ == '__main__':
    src = sys.argv[1]
    lo = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    hi = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
    for i, line in enumerate(open(src, errors='replace'), 1):
        if lo <= i <= hi:
            print(decode(line))
