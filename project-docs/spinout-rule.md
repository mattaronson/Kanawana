# When a topic gets its own article

*Written 2026-09-06, after nine spinouts from `connections/institutional-lineage/canadian-camping-movement.md` under p_452. Operator direction: "I want a very robust wiki, with articles that link to new articles when topics get too complicated to fit in an original article, because there are too many points of contact or there's a deep depth of information about a specific reference point in the original article that needs its own article to explain."*

## The rule

A reference point spins out into its own article when **any** of these holds:

1. **It has its own arc**, rather than a role in the parent's arc. A director's career runs before and after their years at camp; the 1956-61 programme framework does not run before or after the programme article's chronology, it *is* part of it.
2. **Three or more articles would want to link to it** — genuinely link to it as a subject, not mention its name in passing while making some other point.
3. **Its section has passed roughly a thousand words** and is still growing.

The parent keeps a paragraph and a link, and **must still read whole** without the moved material.

## What the rule is not

**The five-fact spawning threshold in CLAUDE.md is a different test.** It asks whether a subject exists in the knowledge base, which is a question about the KB. The spinout rule asks whether a subject needs an article of its own, which is a question about the wiki. **A subject over the five-fact line that is already written into an article that fits it does not need a stub; it needs nothing.** Spawning one duplicates the material.

This was got wrong in writing, in this project's own priority queue. p_452 listed the French-language programme and Values for Living as "two overdue stubs" on the five-fact ground alone. Checking the destination showed both were already written into `traditions/programs-activities.md`, and written well. One of them spun out on the rule above; the other stayed exactly where it was (f_5128).

## Check the destination before you cut

**Always.** Cutting an article into pieces is the wrong move when the piece already exists elsewhere: the cut creates a third copy, or relocates the weaker of two versions.

This is not hypothetical. A 1,463-word block of the movement article was about to be carefully spun out when a check of `history/oldest-camp-question.md` showed it already carried the whole argument, and carried it **better** — with a source where the copy had open speculation. The copy was deleted instead (f_5118).

`scripts/wiki/prose_dupes.py` measures shared passages between articles and, since 2026-09-06, within one article. Run it before a cut and read the result. **It cannot see the same argument made in different words**, which is exactly what the oldest-camp case was, so it does not replace reading the destination.

## Watch for the heading that is not about its contents

Four times in one session a section named after one thing turned out to be mostly about another:

| Heading | Words | Actually about it |
|---|---|---|
| "Hay Finlay: the named individual on both sides" | 4,056 | ~600 |
| "The money stops: why the national record thins after 1985" | 5,566 | ~2,400 |
| "A textbook says Kanawana was first, and it is not enough" | 5,486 | 404 |
| "1968-69: horses, a doubled co-ed intake, and a French section" | 2,401 | three unrelated subjects |

The cause is accretion: when a long article grows by reading a source run issue by issue, the headings end up marking **where the reading stopped**, not what the material is. A heading like that is worse than none, because the audit tool reports it as a candidate for the article it names, and the material actually there goes unnamed and unfindable.

**Nothing in the toolchain detects this.** `spinout_audit.py` measures section length; `prose_dupes.py` measures repetition. Whether a section's contents match its heading is found by reading, and only by reading. When a section is over the threshold, read it before deciding what to cut out of it — the answer is often "re-head this first, then cut".

## Mechanics that have bitten

- **Renumber footnotes with a map built from the moved text**, then copy the source entries out in full. Check which labels the cut orphans in the parent and remove only those.
- **Test citation across the whole file, not the body.** A first pass removed five entries as uncited because it tested only the body; `8ag` is cited inside another source note.
- **Look up source ids. Never derive one from a cache filename.** Three dead ids reached E1-reviewed articles that way (f_5120). The 1921 Year Book's record is `src_ymca_year_book_official_rosters_1921`, which its siblings' naming would not predict.
- **Back-references break on the move.** "The same issue", "again signed", "described elsewhere in this article", "recorded above" — these are silent when the paragraph they pointed at leaves, or when the paragraph arrives somewhere new. Diff the flagged set against `HEAD` so pre-existing ones are not chased.
- **A spinout can manufacture duplication.** Drawing on two distant parts of one parent can land two accounts of the same passage one section apart in the child (f_5124).
- **Register the new file in `wiki/articles.json`.** Until 2026-09-06 an unregistered article passed every check, because every per-article check iterates that file (f_5125). It is blocking now.
- **Articles using lettered bullet sources** (`programs-activities.md`, `coeducation-gender.md`, and now `french-language-camping.md`) write `Sources: 0` in the header with a note, since the harness counts numbered entries.
- **Enter a spinout as `draft`**, even when the parent was E1-reviewed. The prose was reviewed; the new article's structure, overview and open questions were not.
