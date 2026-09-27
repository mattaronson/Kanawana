#!/usr/bin/env python3
"""Find articles whose skeleton is broken, as distinct from their prose.

WHY. traditions/canoe-trips.md was reported by spinout_audit.py as the wiki's
largest section, "Canoe Trips at Kanawana, 8,341 words". That is not a section.
It is everything before the file's FIRST '## ' heading: twenty-one '###'
subsections hanging directly off the h1 title with no '##' parent at all. And one
of them, "What a ten-day canoe trip cost in 1926", was sitting AFTER
'## Related Articles' -- past the apparatus, where a reader following the article
never reaches it.

Neither defect is visible to any other check here. spinout_audit.py measures
section length; prose_dupes.py measures repetition; verify_harness.py checks
citations, links and source numbering. A file can have no structure at all and
pass every one of them.

WHAT THIS CHECKS. Only mechanical, decidable things:

  ORPHAN     '###' subsections before the file's first '## ', i.e. hanging off
             the title. The article template has body sections at '##'.
  STRANDED   any heading after an apparatus section (Sources, Related Articles,
             Research Notes, Open Questions, Images). Content there is unreachable
             in practice. 'Revision History' under Research Notes is expected.
  HEADER     more than one '*Last Updated:*' line, or none; a missing
             '*Status: ... | Sources: N*' line.
  MISSING    no '## Sources' in an article that carries citations.

WHAT IT DOES NOT CHECK, and cannot: whether a section's contents match its
heading. Four sections were found this session named after one thing and mostly
about another, every one of them by reading. See project-docs/spinout-rule.md.

Usage: python3 scripts/wiki/structure_audit.py
"""
import pathlib
import re
import sys

APPARATUS = {"sources", "related articles", "research notes", "open questions",
             "images", "see also", "revision history"}
# Process notes are apparatus too, and this project puts them last by convention:
# "R3 Verification Notes", "E1 Review Notes", "R1 Research Notes",
# "VERIFY Notes (2026-07-09)", "Research Gaps". Matched by pattern because they
# carry dates and priority ids in the heading.
APPARATUS_RE = re.compile(
    r"(verification notes|review notes|research notes|research gaps|verify notes"
    r"|revision history|research questions)", re.I)


def is_apparatus(name):
    return name in APPARATUS or bool(APPARATUS_RE.search(name))


# meta/sources-index.md names source ids throughout, because listing them is what
# it is for. That is not citation and it needs no '## Sources' of its own. Named
# as the single exception rather than loosening the rule for every article.
NO_SOURCES_SECTION = {"meta/sources-index.md"}


def audit(path, rel=None):
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    issues = []

    heads = [(i, l) for i, l in enumerate(lines) if re.match(r"^#{2,6} ", l)]
    first_h2 = next((i for i, l in heads if l.startswith("## ")), None)
    orphans = [l.lstrip("# ").strip() for i, l in heads
               if l.startswith("### ") and (first_h2 is None or i < first_h2)]
    if orphans:
        issues.append("ORPHAN: %d '###' subsection(s) before the first '## ': %s"
                      % (len(orphans), orphans[:3] + (["..."] if len(orphans) > 3 else [])))

    # Only a BODY heading after an apparatus section is stranded. Apparatus
    # sections following one another are the template's own order -- Open
    # Questions, Related Articles, Sources, Research Notes -- and a first version
    # of this check that flagged those reported all 114 articles as broken, which
    # is the same uselessness f_5124 records: a checker that cries wolf about the
    # whole corpus hides the cases that are real.
    seen_apparatus = None
    for i, l in heads:
        name = l.lstrip("# ").strip().lower()
        if seen_apparatus and not is_apparatus(name):
            issues.append("STRANDED: '%s' comes after '%s'" % (l.lstrip("# ").strip(), seen_apparatus))
        if l.startswith("## ") and is_apparatus(name):
            seen_apparatus = l.lstrip("# ").strip()

    n_updated = len(re.findall(r"^\*Last Updated:", text, re.M))
    if n_updated != 1:
        issues.append("HEADER: %d '*Last Updated:*' line(s), expected 1" % n_updated)
    if not re.search(r"^\*Status: .* \| Sources: ", text, re.M):
        issues.append("HEADER: no '*Status: ... | Sources: N*' line")
    # Only an article that actually cites something needs a Sources section.
    # history/timeline-overview.md is a navigation page citing nothing, and
    # meta/sources-index.md IS the source index -- a '## Sources' heading in
    # either would be an empty section added to satisfy a checker, which is worse
    # than the thing it was checking for.
    cites = re.search(r"\^\d", text) or re.search(r"\[src_", text)
    if cites and rel not in NO_SOURCES_SECTION and not re.search(r"^## Sources\s*$", text, re.M):
        issues.append("MISSING: no '## Sources', but the article carries citations")
    return issues


def main():
    rows = []
    for f in sorted(pathlib.Path("wiki").rglob("*.md")):
        if f.name == "README.md":
            continue
        found = audit(f, str(f.relative_to("wiki")))
        if found:
            rows.append((str(f.relative_to("wiki")), found))
    print("STRUCTURE AUDIT -- %d article(s) with a broken skeleton\n" % len(rows))
    for name, found in rows:
        print("  %s" % name)
        for i in found:
            print("      - %s" % i)
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
