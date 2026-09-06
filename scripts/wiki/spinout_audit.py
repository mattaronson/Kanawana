#!/usr/bin/env python3
"""Find sections that have outgrown the article they sit in.

WHY. The wiki's median article is under 2,000 words and its largest is over
36,000, of which 71% is one section. That is not a wiki, it is a small number of
books with a wiki around them. The operating principle (operator, 2026-09-06) is
that a reference point spins out into its own article when it has its own arc
rather than a role in the parent's arc, when three or more articles would want to
link to it, or when its section outgrows a paragraph-and-a-link.

WHAT THIS MEASURES AND WHAT IT DOES NOT. It measures section word counts, which
is a proxy and only a proxy. A 1,200-word section that is genuinely one argument
belongs where it is; a 400-word section about a person with a career elsewhere may
still want its own article. THE THRESHOLD FLAGS CANDIDATES FOR A HUMAN TO JUDGE.
It does not decide.

Usage: python3 scripts/wiki/spinout_audit.py [--threshold 900]
"""
import argparse
import pathlib
import re


def sections(text):
    """Split on ## headings, keeping ### subsections attached to their parent."""
    parts = re.split(r"\n(?=## )", text)
    for p in parts:
        head = p.split("\n", 1)[0].lstrip("# ").strip()
        yield head, len(p.split())


def subsections(text):
    parts = re.split(r"\n(?=### )", text)
    for p in parts:
        head = p.split("\n", 1)[0].lstrip("# ").strip()
        yield head, len(p.split())


SKIP = {"sources", "related articles", "research notes", "open questions",
        "images", "revision history"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--threshold", type=int, default=900)
    args = ap.parse_args()

    rows = []
    for f in sorted(pathlib.Path("wiki").rglob("*.md")):
        text = f.read_text(encoding="utf-8")
        total = len(text.split())
        for head, words in sections(text):
            if head.lower() in SKIP or words < args.threshold:
                continue
            share = words / total if total else 0
            rows.append((words, share, str(f.relative_to("wiki")), head))

    rows.sort(reverse=True)
    print("SECTIONS OVER %d WORDS -- candidates for spinout, not decisions\n" % args.threshold)
    print("%6s %6s  %-46s %s" % ("words", "share", "article", "section"))
    print("-" * 110)
    for w, share, art, head in rows:
        print("%6d %5.0f%%  %-46s %s" % (w, share * 100, art[:46], head[:44]))
    print("\n%d section(s) over threshold across %d article(s)."
          % (len(rows), len({r[2] for r in rows})))


if __name__ == "__main__":
    main()
