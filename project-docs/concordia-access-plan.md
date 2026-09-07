# Getting access to Concordia's AtoM catalogue — what's required and from whom

*Researched 2026-08-25. Everything below is from Concordia RMA's own published pages and the AtoM
software documentation, both read in full.*

## Short answer

**Yes, a specific person's permission is needed, and there is a documented, sanctioned mechanism for
granting it.** The blocker is a standard AtoM feature, not a Concordia-specific wall, and the same
software ships the exact configuration switches that would let us through. An administrator has to
throw them.

## The person

| Name | Role | Why them |
|---|---|---|
| **John Richan** | **Interim Director and University Archivist** — *and separately listed as* **Digital Archivist** (ext. 4345) | The only named person holding both the archival authority to say yes and the digital-systems role to implement it. This is the ask. |
| Julie Daoust | Lead, Records Management and Archives | Second signature if Richan routes it |
| Eric Côté | Archivist, ext. 5921 | The contact printed inside the P0145 finding aid itself |
| Olivier Bisaillon-Lemay | Archives Reference Technician, ext. 2991 | The published contact for *document requests* — the right person for the box-level asks, not the API one |
| Candice Tarnowski | Administrative Assistant, ext. 7775 | Listed directly under **"Archives & Special Collections Shared Catalogue"** — i.e. the catalogue's own front desk |

**Route:** `archives@concordia.ca`. RMA states it "aims to respond to written requests within five
working days."

**One caveat to raise in the letter:** it is the *Archives & Special Collections **Shared**
Catalogue* — shared with Library Special Collections. The AtoM sysadmin may therefore sit with the
Library rather than RMA. Ask Richan to redirect if it is not his to grant, rather than assuming.

## What is actually blocking us

The challenge is **AtoM's built-in JavaScript Challenge**
(`accesstomemory.org/en/docs/2.10/admin-manual/security/js-challenge/`), not a bespoke Concordia
control. Its `test_headless` setting is what refuses us: a client detected as headless never receives
the `visited` cookie and stays in a redirect loop. That is exactly the behaviour we observed.

**Why it exists — and this is worth being straight about.** AtoM shipped this feature in response to
administrators on the `ica-atom-users` list reporting **AI bot traffic causing high CPU load** on
small archival servers. Dan Gillean of Artefactual recommended it in that thread alongside nginx IP
blocks. So the motivation is not primarily *malice* — it is *load*, and AI research crawlers are
precisely the traffic it was built to shed. That does not make this project's research illegitimate.
It does mean asking is the substantive step, not a formality, and that the strongest version of the
ask is one that **reduces** load rather than adding to it.

> **Not pursued, deliberately:** the AtoM docs note that if an installation leaves the `salt` setting
> at its default, "cookie contents could be guessed and the JS challenge bypassed." That is a
> vulnerability disclosure, not an access route. This project will not test it.

## The four things an administrator can do

Listed least-intrusive first. **Options 3 and 4 together are the recommended ask.**

| # | Setting / action | Effect | Fit |
|---|---|---|---|
| 1 | `cidr_exceptions` | Allowlists an IP range | Poor — our egress is a shared cloud proxy with no stable address to give them |
| 2 | `network_user_agent_exceptions` / `asn_user_agent_exceptions` | Allowlists a network + User-Agent pair | Workable; we would declare a descriptive, contactable UA |
| 3 | `endpoint_exceptions` | Exempts named endpoints from the challenge. The docs say this is "useful for API endpoints that should not be challenged, **such as AtoM's Rest API**" | **Strong** — the documentation's own intended use |
| 4 | **REST API key** | Admin enables the `arRestApiPlugin`, then generates a key on a user account (Admin → Users → Edit → "REST API access key" → (Re)generate). **"Only an administrator has the proper permissions to generate an API Key."** | **Strong** — structured JSON instead of scraped HTML |

**Why 3 + 4 is the right ask.** It leaves the JS challenge fully in force for ordinary web traffic —
the crawler load it was built to stop is unaffected. It routes us onto an interface that is *cheaper*
for their server than the HTML pages we would otherwise be fetching. And it produces clean structured
data rather than parsed markup. This is AtoM's documented, intended configuration for exactly our
situation, so we are asking them to use their own software as designed.

## Two constraints that change what we should expect

**1. Privacy law limits `12B06 Campers`.** RMA states, on its Reading Room page, that "in compliance
with the *Act Respecting Documents Held by Public Bodies and the Protection of Personal Information*,
documents containing personal information cannot" be released, and that "requests may be refused if
they contravene the Privacy Act." Camper records are personal information about identifiable and
often living individuals. **`p_279` should not expect 12B06 to be handed over.** The realistic asks
there are aggregate or structural: enrolment totals, section structures, staff rosters (12B05), and
the financial series (12B02). This also aligns with CLAUDE.md's own standing privacy rule.

**2. Reproduction costs money.** Scholarly use pays scanning fees only, no licensing surcharge:

| Format | 0–50 images | 51–100 | 101+ |
|---|---|---|---|
| Low resolution (≤300 dpi, .jpg) | $10.00 | $7.50 | $5.00 |
| High resolution (≥600 dpi) | $15.00 | $11.50 | $7.50 |

Audiovisual reproduction is $1.00/minute for scholarly use. Digital photography without flash is
permitted free in the Reading Room — **for a Montreal-based researcher this is by far the cheapest
route to bulk material.** Appointment required; Reading Room is Mon–Thu, 9:00–11:30 and 1:30–4:00,
Faubourg Building FG A112, 1250 Guy.

## Draft letter

> **To:** archives@concordia.ca
> **Subject:** Research access request — YMCA of Montreal fonds (P0145), Kamp Kanawana
>
> Dear Mr. Richan,
>
> I am a Westmount city councillor and lawyer, researching the history of Camp Kanawana — the YMCA of
> Montreal's camp at Saint-Sauveur, founded 1894 — for a non-commercial public history project. I have
> been working from your published finding aid for the YMCA of Montreal fonds (P0145, generated
> 24 November 2023), which has been invaluable.
>
> I have six requests, in descending order of importance.
>
> **1. P0145/12C01 — "Evaluation, recommendations re Camp Otoreke as a mixed [gender] camp, 1936"
> (Box HA2315).** This is the single document I would most like to see. Kanawana did not admit girls
> until 1968, and an internal recommendation to do so was declined in 1965; a 1936 evaluation of mixed
> camping at an affiliated Y camp would materially change how that history is understood. I would be
> glad to consult it in the Reading Room, or to pay reproduction fees for a scan.
>
> **2. Three sub-sub-series with no page on the public website:** P0145/12B02 (Financial
> administration), 12B05 (Staff, counsellors) and 12B06 (Campers). Your static finding-aid pages on
> concordia.ca cover 12B01, 12B03, 12B04 and 12B07 but not these three. I understand that 12B06 in
> particular is likely to contain personal information and may be restricted under the *Act Respecting
> Documents Held by Public Bodies*; I am not seeking information about identifiable individuals, and
> aggregate or structural information — enrolment figures, section organisation, staff rosters — would
> serve the project fully.
>
> **3. An object list for P0145/12B.** The finding aid records that the Kanawana sub-series includes
> "objects (t-shirts, badges, ribbons, pennants)" alongside film reels and audiocassettes. Is an
> item-level list of those objects available? Camp material culture is poorly documented and this may
> be the only surviving record of it.
>
> **4. A technical request, which I hope is straightforward.** I would like to consult the AtoM
> catalogue programmatically rather than by hand, for a few hundred descriptions in this one fonds. I
> understand and support the JavaScript challenge you have enabled — I am aware it was introduced
> because of AI crawler load on archival servers, and I have no wish to add to that. Rather than work
> around it, I would rather use the interface AtoM provides for this: could an administrator issue a
> **REST API key** against a user account, and add the REST API to `endpoint_exceptions`? That is the
> configuration Artefactual's own documentation recommends for API access. It would leave the
> challenge fully in force for ordinary web traffic, and API requests are cheaper for your server than
> the equivalent page loads. If this is a Library Special Collections decision rather than an RMA one,
> given the shared catalogue, I would be grateful if you could point me to the right person.
>
> **5. Audiovisual reproduction.** Your finding aid lists several quarter-inch audio reels for the
> camp. Three are of particular interest, and I would be glad to pay the scholarly reproduction rate:
>
> - **P0145-11-0193**, "Kamp Kanawana — Interview with Woodsman," 24 August 1962
> - **P0145-11-0197**, "What is God? / Interview of Kamp Kanawana campers and staff," 1963
> - **P0145-11-0191**, "Pathfinder evaluation" (undated)
>
> The first two appear to be recordings of campers and staff speaking in 1962 and 1963. Almost
> everything known about the camp in that decade comes from annual reports and printed brochures, so
> contemporaneous voices would be genuinely significant. I note that RMA posted P0145-09-0066 ("Canoe
> Trips") to your YouTube channel in February 2026 — if any of these are already digitized, or are
> candidates for it, I would be glad to know.
>
> **6. P145/12N04 — the Quebec Camping Association / Association des camps du Québec papers (Box
> HA1888).** Your finding aid lists, among the 1978-1980 material in this sub-sub-series, an item called
> "**Annuaire 1979, liste des membres**." The provincial association published one of these each year and
> Kanawana was a member camp; the 1979 volume is the earliest I have been able to locate anywhere, and
> published copies of the series appear not to have reached the digitized collections. If it is a camp
> directory rather than a bare membership list, it would give me Kanawana's own entry — address,
> director, capacity, ages served — for a period the project is otherwise thin on. I would be glad to
> pay for a scan of the Kanawana entry, or of the whole volume if that is simpler. The same box's
> "Constitution et règlements" (1979) and "Publications, public relations" (1978-1979) would be worth
> seeing in the same visit.
>
> I am in Montreal and can come to the Reading Room at your convenience.
>
> With thanks,
> Matt Aronson
