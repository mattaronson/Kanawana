#!/usr/bin/env python3
"""Find the same prose written into two articles.

WHY. Cutting a long article into spinouts is the wrong move when the block being
cut already exists somewhere else: the cut then creates a third copy, or relocates
the weaker of two versions. That is not hypothetical. On 2026-09-06 a 1,463-word
block of `canadian-camping-movement.md` was about to be carefully spun out when a
check of the destination showed `history/oldest-camp-question.md` already carried
the whole argument -- and carried it BETTER, with a source where the copy had open
speculation. The copy was deleted instead (f_5118). Nothing in the toolchain
caught that; it was caught by hand, by luck, on one block out of dozens.

`duplicate_sources.py` finds documents catalogued twice. This is its equivalent
for prose.

WHAT THIS MEASURES. Shared word-shingles between article bodies. A shingle is a
run of N consecutive normalised words; two articles sharing a long run of shingles
are, at that point, the same text. Reported runs are reconstructed back into
contiguous passages so a human can read what actually overlaps.

WHAT IT DOES NOT MEASURE. It cannot tell duplication from legitimate quotation:
two articles quoting the same sentence of the same annual report SHOULD both carry
it. It cannot tell duplication from a deliberate summary-plus-link, which is the
shape the hub-and-spoke structure is supposed to produce. And it is blind to the
same argument made in different words, which is the more common and worse case.
THE OUTPUT IS A READING LIST, NOT A VERDICT.

Sources, Related Articles and the other apparatus sections are excluded: shared
citations there are the cross-linking working, not a defect.

Usage: python3 scripts/wiki/prose_dupes.py [--shingle 12] [--min-run 25]
"""
import argparse
import collections
import pathlib
import re

SKIP = {"sources", "related articles", "research notes", "open questions",
        "images", "revision history", "see also"}


def body_words(text):
    """Normalised words of the article body, minus apparatus sections.

    Returns a list of (word, char_offset) so a matching run can be quoted back.
    """
    out = []
    skipping = False
    offset = 0
    for line in text.split("\n"):
        start = offset
        offset += len(line) + 1
        if line.startswith("#"):
            skipping = line.lstrip("# ").strip().lower() in SKIP
            continue
        if skipping or not line.strip():
            continue
        if line.lstrip().startswith(("<!--", "*Status:", "*Last Updated:")):
            continue
        for m in re.finditer(r"[a-z0-9]+", line.lower()):
            w = m.group(0)
            out.append((w, start + m.start()))
    return out


def shingles(words, n):
    for i in range(len(words) - n + 1):
        yield " ".join(w for w, _ in words[i:i + n]), i


def runs(hits):
    """Collapse (i, j) shingle-index pairs into maximal diagonal runs."""
    hits = sorted(hits)
    seen = {(i, j) for i, j in hits}
    for i, j in hits:
        if (i - 1, j - 1) in seen:
            continue
        length = 1
        while (i + length, j + length) in seen:
            length += 1
        yield i, j, length


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shingle", type=int, default=12)
    ap.add_argument("--min-run", type=int, default=25,
                    help="minimum overlapping words to report a passage")
    args = ap.parse_args()
    n = args.shingle

    docs = {}
    for f in sorted(pathlib.Path("wiki").rglob("*.md")):
        words = body_words(f.read_text(encoding="utf-8"))
        if len(words) >= n:
            docs[str(f.relative_to("wiki"))] = words

    index = collections.defaultdict(list)
    for name, words in docs.items():
        for sh, i in shingles(words, n):
            index[sh].append((name, i))

    pairs = collections.defaultdict(list)
    for sh, locs in index.items():
        if len(locs) < 2 or len(locs) > 40:
            continue  # a shingle in 40 places is boilerplate, not duplication
        for a in range(len(locs)):
            for b in range(a + 1, len(locs)):
                (na, ia), (nb, ib) = locs[a], locs[b]
                if na == nb:
                    continue
                key = (na, nb) if na < nb else (nb, na)
                pairs[key].append((ia, ib) if na < nb else (ib, ia))

    report = []
    for (na, nb), hits in pairs.items():
        passages = []
        for i, j, length in runs(hits):
            words_shared = length + n - 1
            if words_shared >= args.min_run:
                passages.append((words_shared, i, j))
        if passages:
            passages.sort(reverse=True)
            report.append((sum(p[0] for p in passages), na, nb, passages))

    report.sort(reverse=True)
    print("# Cross-article prose duplication\n")
    print("%d articles compared, shingle=%d words, reporting runs of >=%d words.\n"
          % (len(docs), n, args.min_run))
    print("Quotation of a shared source is not duplication. Read before cutting.\n")
    if not report:
        print("No overlapping passages at this threshold.")
        return
    for total, na, nb, passages in report:
        print("\n## %d words shared\n" % total)
        print("- `%s`" % na)
        print("- `%s`\n" % nb)
        for words_shared, i, j in passages[:6]:
            quote = " ".join(w for w, _ in docs[na][i:i + min(words_shared, 30)])
            print("  - **%d words** (at word %d / word %d): %s ..." % (words_shared, i, j, quote))
        if len(passages) > 6:
            print("  - ... and %d shorter passages" % (len(passages) - 6))


if __name__ == "__main__":
    main()
