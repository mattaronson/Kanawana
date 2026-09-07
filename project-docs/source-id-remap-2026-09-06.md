# p_220 — the 42 dangling source_ids, and what was done with each

Written 2026-09-06. Every `source_id` cited by a fact in `kb/facts.json` now resolves to a record in
`sources/sources.json`. Nothing was dropped. Two different things were done, and they are not
interchangeable.

## Remapped to an existing record (20)

The dangling id and the canonical id name the same source. The citation was rewritten in place and the
old id no longer appears anywhere in the KB.

| dangling id | remapped to | why |
|---|---|---|
| `src_cbc_2021_covid` | `src_cbc_2021_kanawana` | same outlet, same year, same subject: CBC on Quebec sleepaway camps and Kanawana in 2021. DECIDED ON SUBJECT AND DATE, NOT A MATCHING URL -- a judgement, not an identity |
| `src_concordia_12A` | `src_concordia_ymca_12A` | same sub-series, P0145/12A Camping and Outdoor Education |
| `src_concordia_kanawana_film` | `src_concordia_kanawana_documentary` | same 1993 film record in Concordia AtoM |
| `src_concordia_ymca_fonds` | `src_concordia_fonds` | same fonds-level record, YMCA of Montreal P145 |
| `src_concordia_ymca_fonds_12b` | `src_concordia_atom_kanawana` | same finding aid: the Kamp Kanawana sub-series P0145/12B |
| `src_dev_peace_2015` | `src_devp_leduc_2015` | same Development and Peace press release of 28 July 2015 naming David Leduc |
| `src_gazette_1933_fossils` | `src_newspapers_gazette_1933` | same article: Montreal Gazette, 24 February 1933, "Music and Comedy in Fossils' Revue" |
| `src_hektoen_childrens_hospital` | `src_mcgill_cushing` | the existing record is titled "McGill Architecture PDF / Hektoen International -- Harold Beveridge Cushing" and is the Hektoen piece the citation means |
| `src_ia_1919_autobiographical_sketch` | `src_ia_autobiographical_sketch_1919` | same document: the August 1919 "Brief Autobiographical Sketch of Association Career", the words of the id transposed |
| `src_mediaterre_kanawana` | `src_mediaterre_kanawana_2009` | same Mediaterre item on Kanawana's revitalisation |
| `src_oral_history_aronson` | `src_oral_aronson` | same ongoing oral history with the operator |
| `src_vss_families` | `src_vss_familles_pionnieres` | same Ville de Saint-Sauveur page, "Les familles pionnieres" |
| `src_web_2022_staffing` | `src_cbc_camp_staffing_2022` | same 2022 CBC report on Quebec summer-camp staffing |
| `src_web_quebec_folklore` | `src_web_quebec_folklore_2026` | same Quebec folklore reference set |
| `src_westmount_magazine_mclean_comments` | `src_westmountmag_mclean` | the comment thread on that same article; not a separate publication |
| `src_westmount_mclean_2017` | `src_westmountmag_mclean` | same article: Westmount Magazine, "A fond farewell to Stuart McLean", 2017 |
| `src_wikipedia_ouareau` | `src_wikipedia_camp_ouareau` | same Wikipedia article, Camp Ouareau |
| `src_ymca_quebec_pip_sharpe_2018` | `src_ymca_pip_sharpe_2018` | same YMCA Quebec release, identical URL |
| `src_ymcaquebec_kanawana_history` | `src_ymca_kanawana_history` | same live YMCA Quebec Kanawana history page |
| `src_youtube_kanawana_silent_1960s` | `src_youtube_kanawana_1960s_silent_film` | same video, YouTube id ZrUuQ1SU7q8 |

## Backfilled as a new record (22)

No existing record is the same source. Each record was written **from the citing fact's own wording**,
not from the source, and carries `read_state: unverified_backfill` saying exactly that. **These are not
verified sources.** Anything that wants to rely on one has to fetch it first.

| new id | cited by | what the citing fact says it is |
|---|---|---|
| `src_cbc_daybreak_camps_reopen` | f_0759 | CBC Montreal Daybreak segment on camps reopening (cited for Sean Day having left the Kanawana director role) |
| `src_concordia_12B04` | f_1256, f_1257, f_1259 | Concordia University Archives, YMCA of Montreal fonds sub-sub-series P0145/12B04: Kamp Kanawana communications (1994 centennial poster, "The Look Out" alumni newsletter, reunion material) |
| `src_concordia_1B` | f_1262 | Concordia University Archives, YMCA of Montreal fonds sub-series P0145/1B: Centennial/Expo Project Committee, holding a 1966 "Summary Historical Statement / resume historique" |
| `src_concordia_reeves_film` | f_1258 | Concordia University Archives record for the 1993 film "Kamp Kanawana: The Experience that Lasts a Lifetime" giving production credits: Laurentien Productions for the Montreal YMCA, directed by Cathy Reeves |
| `src_gazette_1942_parade` | f_0851, f_0855, f_0862, f_0868 | Montreal Gazette, 5 August 1942, "Y.M.C.A. Boys Stage Parade and Circus" -- names Camp Director R. H. Hanagan and Resident Director E. E. Smee |
| `src_geni_cushing` | f_1164 | Geni public family tree pages for the Cushing family of Montreal |
| `src_imtl_ymca` | f_1020 | Images Montreal (imtl.org) pages on the YMCA of Montreal buildings: Victoria Square 1873, Dominion Square 1891, Drummond Street 1912 |
| `src_indigenous_tourism_quebec` | f_1088 | Indigenous tourism Quebec material on the First Nations territories of the Laurentians |
| `src_qahn_laurentians_history` | f_1088 | Quebec Anglophone Heritage Network material on Laurentian regional history |
| `src_vac_cushing` | f_1163 | Veterans Affairs Canada, Canadian Virtual War Memorial record for Robertson Macaulay Cushing |
| `src_warren_reflections` | f_1440, f_1442, f_1443, f_1444, f_1445, f_1446, f_1448 | A "Warren" reflections or memorial piece on the sociologist Harold H. Potter (1914-2004): his dates, his 1947-49 McGill MA under Oswald Hall, and his thesis "The Occupational Adjustments of Montreal Negroes, 1941-48" |
| `src_web_globe_mail_shatner` | f_0568 | A Globe and Mail item on William Shatner as a counsellor at Camp B'nai Brith, Sainte-Agathe-des-Monts, c. 1948-49 |
| `src_web_search_exhausted` | f_1432, f_1985 | NOT A DOCUMENT: a placeholder id used in this project's early months to cite an exhausted web search as the basis for a NEGATIVE finding. Kept so those facts keep a source, but it names no publication and nothing can be re-read from it |
| `src_wikipedia_childrens_hospital` | f_1162 | Wikipedia, Montreal Children's Hospital (formerly the Children's Memorial Hospital) |
| `src_wikipedia_sgwu` | f_1021 | Wikipedia, Sir George Williams University |
| `src_wikipedia_tuxis` | f_0932, f_0935, f_0936 | Wikipedia, Tuxis / Canadian Standard Efficiency Training and the Trail Rangers |
| `src_wiktionary_kanawa` | f_1085 | Wiktionary entries for "kanawa" and its cognates in Carib, Trio, Wayana and Taino |
| `src_ymca_kanawana_leadership_2026` | f_1106 | YMCA Quebec Camp Kanawana leadership-programme page for the 2026 season (Voyageurs Ultimate dates and ages) |
| `src_ymca_kanawana_town_hall` | f_1109 | A Camp Kanawana families Zoom town hall of 27 January (year not stated in the citing fact, probably 2022) with Sean Day, Kate Taylor and Kevin Slezak |
| `src_ymca_quebec_website` | f_1428 | A YMCA Quebec web page cited for Kanawana's three private lakes. NOT REMAPPED: src_ymca_website and src_ymca_quebec_history are both plausible and neither is demonstrably the one meant |
| `src_ymcaq_kanawana` | f_1509 | A YMCA Quebec Kanawana page giving the French name Bucherons for the Lumbermen team |
| `src_ywca_oolahwan_history` | f_1242 | A YWCA camping history source cited for YWCA Camp Hochelaga in Vermont being "the last residential YWCA summer camp". NOT the Oolahwan page already held as src_ywca_oolahwan_page: the claim is about a different camp |

## Three things this exposed

**The queue said 40; there were 42.** The count was taken on 2026-08-12 and drifted, because a dangling
`source_id` reappears whenever a fact is written by hand. Counting it once does not hold it. Worth a
check in the harness rather than a number in the queue.

**`sources/sources.json` has real duplicates, and remapping had to choose between twins.** Three remap
targets have a near-identical sibling holding the same URL: `src_westmount_mag_mclean` beside
`src_westmountmag_mclean`, `src_ymca_pip_sharpe` beside `src_ymca_pip_sharpe_2018`, and
`src_youtube_kanawana_silent` beside `src_youtube_kanawana_1960s_silent_film`. Cleaning those up is
`p_303`'s job, not this one's, but a remap made today is a vote for one twin and this table records
which way it went.

**One remap is a judgement, not an identity.** `src_cbc_2021_covid` → `src_cbc_2021_kanawana` was
decided on outlet, year and subject with **no matching URL**. If the citing fact turns out to have meant
a different CBC piece from 2021, this is the first place to look.

## And one that is not a source at all

`src_web_search_exhausted` is a placeholder from the project's early months, used to cite an exhausted
web search as the basis for a negative finding. It now has a record so the citation resolves, and the
record says plainly that it names no publication and that nothing can be re-read from it. Two facts use
it. That is a different kind of defect from a missing record and it is not fixed here.
