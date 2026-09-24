# Embargo register

**The record comes first. Embargo is metadata, not deletion.**

Operator decision, 2026-09-03:

> "We're better off having the whole record and selecting from it now than
> deleting material that ought to just be embargoed and potentially creating
> holes in the record for future scholarly work that may come to rely on this
> research."

And on where the decision belongs:

> "We need to make surface publication policy decisions at the wiki UI design
> level, not here. For the purpose of collecting the data and writing the
> articles, the repo and wiki are fine."

So nothing is withheld from `kb/facts.json` or from `wiki/`. Both are working
surfaces and both should be complete. What this directory does is **label**
material whose publication needs a decision, so that the decision can be made
once, later, at the layer that actually publishes — and so that it can be made
by someone looking at a list rather than by someone remembering.

## Why not just leave it out

Because omission is invisible and permanent. A later researcher reading a
Kanawana article cannot tell the difference between "the source says nothing
about this" and "someone decided not to write it down," and neither can a later
pass of this project — which is how the same document gets read three times to
the same dead end. A hole in the record looks exactly like an absence of
evidence, and in scholarship that is a serious thing to manufacture.

An embargo says: this exists, here is where, here is why it needs a decision,
here is when to look again.

## How it works

**In the knowledge base.** An embargoed fact is an ordinary fact carrying a
`publication` block:

```json
"publication": {
  "status": "embargoed",
  "register_id": "r_0001",
  "review_on": "2055-01-01",
  "basis": "later of record date + 75 and estimated birth + 100",
  "why": "..."
}
```

**In an article.** The passage is written where it belongs historically, wrapped
so a machine can find it:

```markdown
<!-- embargo:r_0001 -->
...the passage, with a one-line note saying what it is and when it reviews...
<!-- /embargo:r_0001 -->
```

**In this register.** One record per embargo: which facts, which document and
lines, what kind, why, the basis, the review date, and what would justify
earlier release. The register indexes; it does not restate.

## The embargo term

Default for personal assessments of identifiable private individuals: the
**later** of record date + 75 years (the common archival term for restricted
personnel material) and estimated year of birth + 100. Earlier release on the
subject's consent or on confirmation of death.

`review_on` is a date to look again. It is never a date to publish
automatically.

## An assumption in this that turned out to be false, and what was decided

**Checked 2026-09-07: this repository is public.** GitHub reports
`mattaronson/Kanawana` as `visibility: public`, with no licence and no
distribution notice.

The directive quoted at the top of this file — that "for the purpose of
collecting the data and writing the articles, the repo and wiki are fine" —
defers publication policy to a wiki UI layer that will decide what to surface.
Every embargo written since has been built on it. But an embargo marker is an
HTML comment. On github.com the marker is invisible and the passage inside it
renders as ordinary prose to anyone who opens the file. There is no UI layer
standing between this material and the public. The repository is the surface.

That was put to the operator on 2026-09-07 with the specifics: that
`wiki/people/leo-robitaille.md` sits on the default branch carrying a 1973
director's do-not-re-hire list naming three people and adverse assessments of
two more, and that those five are now in their seventies. The options offered
were a private repository, a public repository with the embargoed passages held
in a private half, leaving it as it stands, or deferring.

**He chose to leave it as it stands.** The repository stays public with the
material in it, and embargoed material continues to be written into it as this
file directs.

Three things follow, recorded here so the question is not re-raised from
scratch by a later pass:

1. **The labelling is unchanged.** Everything still gets extracted, wrapped,
   registered and dated. What was decided is the *surface*, not the labelling.
   Unlabelled is still the failure.
2. **`r_0006` is unblocked.** It had summarised a 27-name honour roll instead of
   transcribing it inside markers, which was the weaker treatment under the
   reasoning above and is now the one to correct.
3. **The decision covers this repository.** It is not permission to reproduce
   this material anywhere else.

## The check

`scripts/verify/restricted_guard.py` verifies that every embargoed fact is
registered, dated and reasoned; that every register entry resolves to real facts
and a readable source; that every embargo marker in `wiki/` is paired and names
a real entry; and that no name occurring only in embargoed facts appears in an
article **outside** a block. Unlabelled is the failure — not present.

It names the fact, the article and the register entry. Never the person.

### Three bugs it has had, all failing open

Worth recording, because a check that passes wrongly is worse than no check:

1. The name extractor matched only title case, so names written in capitals for
   emphasis — the ones it exists to find — went straight past it.
2. A debugging session put two of the protected surnames into the stopword list,
   excusing them from every check.
3. It asked whether a name appeared *inside* an embargo block, rather than
   whether every occurrence was inside one. A name both properly blocked and
   loose in the prose passed.

All three were caught by planting a name and watching, not by reading the code.
Any change to this script should be tested the same way.

## Still to do

Publication policy itself — redact, gate, placeholder, or show — is a **wiki UI
design decision** and is deliberately not made here. Tracked as p_308.
