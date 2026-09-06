#!/usr/bin/env python3
"""Append a numbered source note to a wiki article, correctly, in one step.

WHY THIS EXISTS. Adding a numbered source note by hand is four steps, and on
2026-09-06 three of them were got wrong three separate times, in three different
articles, each time shortly after the same mistake had been fixed somewhere else:

  1. pick the next free number -- by enumerating BOTH entries and markers, since
     either can run higher than the last entry you happen to read;
  2. insert the entry INSIDE the Sources list, after the last numbered entry --
     not at the end of the file, because most articles here carry Research Notes
     and HTML comments after Sources, and a naive append lands outside the list
     where the marker resolves to nothing;
  3. bump the `Sources: N` count in the header, which counts NUMBERED entries
     (a lettered sub-note like 8bt does not move it);
  4. add the source id to articles.json `sources_cited` ONLY IF the article
     actually cites the source id -- if it cites a fact id instead, adding it
     there produces the other direction of verify_harness's A2: present in
     sources_cited, never cited in the article.

This does 1-3. Step 4 stays manual because only the author knows how the article
cites. Run scripts/verify/all.py afterwards either way.

Usage:
    python scripts/wiki/add_source_note.py wiki/site/camp-otoreke.md "Note text."
    python scripts/wiki/add_source_note.py ARTICLE "Note text." --dry-run

It prints the number it assigned; put `^<number>` in the prose yourself, because
where the marker belongs is a judgement about the sentence, not about the file.
"""
import argparse
import re
import sys
from pathlib import Path


def next_free(text: str) -> int:
    """Highest of every numbered entry and every ^N marker, plus one."""
    src = text[text.find("## Sources"):] if "## Sources" in text else ""
    entries = {int(m.group(1)) for m in re.finditer(r"^(\d+)\. ", src, re.M)}
    markers = {int(m.group(1)) for m in re.finditer(r"\^(\d+)\b", text)}
    return max(entries | markers, default=0) + 1


def insert_after_last_entry(text: str, note_line: str) -> str:
    """Place the note directly after the last numbered entry in ## Sources."""
    start = text.find("## Sources")
    if start < 0:
        raise SystemExit("no '## Sources' heading in this article")
    last_end = None
    for m in re.finditer(r"^\d+\. .*$", text[start:], re.M):
        last_end = start + m.end()
    if last_end is None:
        raise SystemExit("'## Sources' has no numbered entries to append after")
    return text[:last_end] + "\n" + note_line + text[last_end:]


def bump_header(text: str, new_count: int) -> str:
    m = re.search(r"^(\*Status: .+? \| Sources: )(\d+)(\*)$", text, re.M)
    if not m:
        print("  warning: no '*Status: ... | Sources: N*' header found; not bumped")
        return text
    return text[:m.start()] + m.group(1) + str(new_count) + m.group(3) + text[m.end():]


def count_entries(text: str) -> int:
    src = text[text.find("## Sources"):] if "## Sources" in text else ""
    return len({int(m.group(1)) for m in re.finditer(r"^(\d+)\. ", src, re.M)})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("article")
    ap.add_argument("note", help="the note text, without its leading number")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    path = Path(args.article)
    text = path.read_text()

    n = next_free(text)
    line = f"{n}. {args.note.lstrip()}"
    out = insert_after_last_entry(text, line)
    out = bump_header(out, count_entries(out))

    if args.dry_run:
        print(f"would assign ^{n} and insert:\n  {line[:120]}")
        return 0

    path.write_text(out)
    print(f"added note {n} to {path}")
    print(f"  now put ^{n} in the prose, then run scripts/verify/all.py")
    print( "  and add the source id to articles.json sources_cited ONLY if the")
    print( "  article cites the source id rather than a fact id.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
