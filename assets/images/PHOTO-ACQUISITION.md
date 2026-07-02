# Photo Acquisition Checklist

This is the to-do for populating the Camp Kanawana visual archive. Full provenance for each
item is in `credits.json`. Images can arrive two ways:

- **You drag-and-drop** the file into the chat → I move it into `assets/images/`, set its
  `credits.json` entry to `acquired`, and wire it into the relevant article.
- **A Chrome-for-Claude session** downloads it → save with the `target_filename` from
  `credits.json` and report the source URL.

**Naming:** use the `target_filename` field in `credits.json` (e.g. `flag-raising-kanawana-c1910.jpg`).

**Copyright shortcut (Canada):** photographs created **before 1949 are public domain in Canada**,
so the early archival images (1898, c.1910, 1915, 1944) are safe to display with a credit line.
Items from 1950 onward are likely still in copyright — get permission before publishing.

---

## Tier 1 — Get these first (public domain, high impact)

- [ ] **1898 Camp Jubilee group photo** ("YMCA Camp - Lac St. Joseph"; Cunningham, Brown, Benedict, Dawson)
      → Concordia AtoM, fonds P0145/12L. `camp-jubilee-group-1898.jpg`
- [ ] **Flag-raising ceremony, c.1910** ("FLAG RAISING KAMP KANAWANA / MONTREAL Y.M.C.A. BOYS CAMP")
      → Concordia RMA Flickr (Ref P145). `flag-raising-kanawana-c1910.jpg`
- [ ] **Camp truck, c.1910** → Concordia RMA Flickr (Ref P145). `camp-truck-kanawana-c1910.jpg`
- [x] **Concordia Archives Flickr album** — DONE 2026-07-02: all 34 images acquired and filed to
      `assets/images/historical/` and `assets/images/maps/` (delivered via `photodownloads/`).

## Tier 2 — Strong historical, mostly PD

- [ ] **Camp Otoreke, 1944** → QAHN image page. `camp-otoreke-1944.jpg`
- [ ] **Ross & Macdonald drawings (1913-1921)** — at least the 3 "lead" sheets (one per project)
      → CCA, Ross & Macdonald fonds AP013. `cca-ross-macdonald-<project>.jpg`

## Tier 3 — In copyright; reference now, permission later

- [ ] **Otoreke landing RPPC postcard** → eBay/auction archive. `otoreke-camp-landing-postcard.jpg`
- [ ] **Centennial poster, 1994** → Concordia P0145/12B04. `centennial-poster-1994.jpg`
- [ ] **McCord item C387** (c.1930 postcard) — may need a museum request; not online. `mccord-c387-kanawana-c1930.jpg`
- [x] **1960 CIT plaque** (Ron McCallum) — DONE 2026-07-02: acquired along with the full 151-photo
      "Plaque" album, filed to `assets/images/plaques/cit-1960.jpg` (delivered via `photodownloads/`).
- [ ] **Harold C. Cross portrait, 1971** → Concordia P0145. `harold-cross-1971.jpg`
- [ ] **Facebook "1987-1994" album** — select a few → camp Facebook page.

## Moving images (link only — do NOT store in repo)

- [ ] Cathy Reeves 1993 film (YouTube, Concordia channel) — already cited in `kanawana-in-media`
- [ ] 1960s silent film (YouTube `ZrUuQ1SU7q8`) — optionally extract one still frame
- [ ] 1941 CFCF radio broadcast (Internet Archive) — audio, link only

---

## When a file arrives

1. Place it in `assets/images/` with the `target_filename`.
2. In `credits.json`: set `status: "acquired"`, add `filename`, confirm `rights`.
3. Embed in the suggested article(s) with a caption + credit, e.g.:
   `![Flag-raising at Kamp Kanawana, c.1910](../../assets/images/flag-raising-kanawana-c1910.jpg)`
   `*Flag-raising ceremony, c.1910. Concordia University Archives (P145). Public domain.*`
