# p_218 mechanical VERIFY findings (deterministic half)

Run 2026-08-12 against all 28 draft articles. Scripts in this scratchpad:
`verify_harness.py`, `convention_check.py`, `uncited_claims.py`.

## Clean results (no action)
- **Citation markers**: every `^N` in all 28 articles resolves to a numbered Sources entry. Zero dangling.
- **`[src_]` refs**: every bracket ref in all 28 resolves to a real `sources.json` record. Zero dangling.
  (Note: this is *within these 28*; the wider 40-dangling-source_id problem is p_220's scope, in `kb/facts.json`.)
- **Wiki-links**: zero broken across all 28 (and 0/711 broken wiki-wide).
- **`articles.json sources_cited`**: consistent with the set of `[src_]` ids actually cited, for all 28.
  (An earlier count-based check produced 5 false positives; numbered entries may legitimately
  repeat a source, so sets must be compared, not counts.)

## F1. Header "Sources: N" wrong in 9 articles
Convention confirmed empirically, not assumed: header N == count of numbered Sources entries
(35/46 E1-reviewed, **3/3 R3-verified** — the actual bar being advanced to).

| article | header says | actual entries |
|---|---|---|
| bruce-netherwood | 7 | 9 |
| chris-adam | 6 | 8 |
| green-triangle | 8 | 9 |
| interwar-era | 10 | 11 |
| james-orbinski | 6 | 5 |
| justin-caldwell | 5 | 6 |
| nelson-mcewen | 4 | 10 |
| richard-patten | 4 | 7 |
| sam-lazarus | 5 | 6 |

## F2. Two orphan Sources entries (listed, never cited)
- `between-centennials` #7 (McMorris thesis, `src_mcmorris_thesis`) — "McMorris" appears nowhere
  in the body; genuinely unused.
- `postwar-gap` #8 (`src_concordia_chrcs_fonds`) — exact duplicate of #7, which *is* cited by `^7`.

## F3. Overview paragraphs systematically uncited — the one substantive mechanical finding
Overviews that assert a date, by status:

| status | overviews asserting a year | uncited | % |
|---|---|---|---|
| E1-reviewed | 33 | 5 | 15% |
| R3-verified | 2 | 1 | 50% |
| **draft (these 28)** | **25** | **18** | **72%** |

The mature articles *do* cite their Overviews; the Campaign 65-71 spawns systematically do not.
This bears directly on the R3 bar's "every claim cited". This finding is robust — it checks only
whether the Overview section contains any `^N`/`[src_]` at all, which needs no sentence parsing.

### Discarded approach (recorded so it is not re-attempted)
`overview_propagation.py` tried to auto-propagate body citations into Overviews by matching years
sentence-by-sentence. **Its output is unreliable — do not use it.** House style puts the citation
marker *after* the sentence period (`...for the same span.^1`), so a `(?<=[.!?])\s+` splitter
detaches every marker from the sentence it belongs to and reattaches it to the next one. This
produced false "NO BODY CITATION" verdicts — e.g. it flagged `arleen-boyer`'s 1995/2000 tenure as
entirely uncited when `arleen-boyer.md:12` plainly cites `^1`. Any future mechanical citation
analysis in this wiki must treat a trailing `^N` as belonging to the preceding sentence.
Claim-level grounding is better done by reading, which is what the five VERIFY agents are doing.

## F4. Name-variant scan wiki-wide: CLEAN (no action)
`name_variants.py` harvested capitalised person-name sequences across all 88 wiki files and grouped
near-duplicates. Every variant found — "Arlene Boyle" vs "Arleen Boyer", "Joanna Hode" /
"Johanna A.A. Hoade" / "Joanna A.A. Hoad", "Nicholas" vs "Nicolas Garcia" — occurs **only** inside
explicit correction narratives (Revision History entries, `<!-- R10/R14/R15/R17 -->` research notes,
and Overview sentences that state the correction). The current-use spelling is consistent in every
file. This is the no-silent-overwrite rule working as designed, not corruption. Independently
corroborated by the Two-Tier Era VERIFY agent, which also found no cross-file misspellings.
Residual cosmetic-only variants: "David Leduc" vs "Dave Leduc" (5 files), "R.L." vs "R. L. Charlton".

## Observations logged, deliberately NOT fixed here (scope discipline)
- **Two coexisting citation conventions wiki-wide.** Older E1-reviewed articles use bullet-style
  Sources lists with inline `[src_]` refs and no `^N` markers (e.g. `founding-1894`, `da-budge`);
  all 28 Campaign 65-71 drafts use numbered entries + `^N`. Both are internally coherent. Unifying
  them would touch ~50 E1-reviewed articles — out of scope for p_218, worth its own queue item.
  (`da-budge` is a genuine hybrid: bullets plus one stray `5.` entry — real sediment.)
- **`word_count` computed two different ways.** 22 of 28 were counted body-only; 6
  (chris-adam, james-orbinski, john-cleghorn, nelson-mcewen, rob-braide, ross-bannerman) were
  counted full-file including the Sources section. Mean |drift| is 65–110 words under every
  candidate convention, i.e. the field is approximate under all of them. Not part of the R3 bar;
  normalizing it here would add false precision. Worth a separate documented-convention pass.
