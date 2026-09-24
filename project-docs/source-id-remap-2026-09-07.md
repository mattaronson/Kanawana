# Source-id remap, 2026-09-07 — one document, many ids

Companion to `source-id-remap-2026-09-06.md`. That one dealt with citations pointing at ids that did not
exist. This one deals with the opposite: **one document held under several ids at once**, each with its own
record, each accumulating its own facts, and none referencing the others.

## How they were found

Not by looking for them. The duplicate *source_id* check in `scripts/verify/data_integrity.py` had been
advisory since it shipped, and clearing it (twenty ids held by forty-five records) surfaced the harder
question: how many DOCUMENTS are held under different ids, which no id-level check can see? Grouping every
record by its `origin_url` answered it. **Seventy-two urls were held by more than one record, across 161
records.**

## What was excluded, and why the obvious rule is wrong

**A URL identifies a scan or a page, not necessarily a document.** Two groups were excluded on exactly that
ground, and finding them is the reason this pass was not run automatically:

- `archive.org/details/yearbookyoungme01commgoog` holds `src_ymca_yearbook_1899` and
  `src_ymca_yearbook_1900`.
- `archive.org/details/ymcayearbookand00assogoog` holds `src_ymca_yearbook_1898` and
  `src_ymca_yearbook_1900_second_copy`.

**These are not duplicates.** One Internet Archive scan binds several annual volumes together, and this
project deliberately registered one record per year, because each carries a different Montreal staff roster.
Merging them would have moved rosters onto the wrong years — the D. A. Budge and W. H. Ball series among
them. A title-similarity test passes them happily, which is why a second test on the `date` field was added,
and why the residue was read by hand rather than merged on the strength of two passing heuristics.

Also excluded: any URL whose path is empty. Seven BAnQ records share the bare root `numerique.banq.qc.ca`
and are entirely different documents whose per-item URLs were never recorded. **That is a missing-URL
defect, not a duplication one, and it wants the URLs rather than a merge.**

Three groups whose members are genuinely different things also stayed separate: the Concordia 12A page
against the fonds-level record that had been given 12A's URL by mistake; two distinct Flickr albums whose
recorded URL is the album *index*; and a Camp Waabanaki page against a general Ontario-YMCA enumeration
record that had been given one example page's URL. Those are wrong-URL defects and are noted in `p_303`.

## Rules applied to the fifty-nine merges

- **Canonical** = the id with the most facts, then the most wiki citations, then the shortest id. Two
  canonicals were **forced** rather than computed, because `source-id-remap-2026-09-06.md` had already
  chosen a winner and `p_303` says to fold the loser into it: `src_westmountmag_mclean` and
  `src_youtube_kanawana_1960s_silent_film`.
- **Date**: the longest date string among members sharing the canonical's year, so `2017` yields to
  `2017-02-22` while an access year does not overwrite a publication date. Every distinct date the merged
  records held is written into the surviving record's note.
- **Title** longest; **reliability** highest; **type, origin, cache_path, char_count** taken from the first
  member holding one where the canonical had none.
- **Read state**: the canonical keeps its own, unless a merged record carried a `direct:` or `measured:`
  basis and the canonical did not — a measured read outranks an asserted one.
- **Notes**: every distinct note preserved verbatim behind the merge note.

## Effect

- Source records: **1,705 → 1,636** (sixty-nine folded).
- Fact source references repointed: **124**.
- Wiki files rewritten: **14**, plus five articles whose `sources_cited` list held the same id twice once the
  remap collapsed two entries into one.
- One footnote had to be rewritten by hand: `camp-pine-crest.md` carried a note explaining that a blog post
  was "listed four times under three duplicate source ids" and named all three, which after the remap named
  the same id three times.

## The table

| Folded | Into | URL |
|---|---|---|
| `src_ia_ballantyne_ymca` | `src_ballantyne_1944` | https://archive.org/details/1851-1944-a-brief-history-of-the-canadian-ymca |
| `src_banq_montrealmatin_1971` | `src_banq_montreal_matin_1971_08_24` | https://numerique.banq.qc.ca/patrimoine/details/52327/4512657 |
| `src_canadian_history_ehx_pageant` | `src_canada_ehx_pageant` | https://canadaehx.com/2023/09/12/the-voyageur-centennial-canoe-pageant |
| `src_canada_post_mosher_2021` | `src_canadapost_mosher` | https://www.canadapost-postescanada.ca/blogs/personal/perspectives/editorial-cartoonist-terry-mosher |
| `src_cae_mosher` | `src_canadian_encyclopedia_mosher` | https://www.thecanadianencyclopedia.ca/en/article/terry-mosher |
| `src_cbc_sleepaway_greenlight_2021` | `src_cbc_2021_kanawana` | https://www.cbc.ca/news/canada/montreal/quebec-sleepaway-camps-1.6017617 |
| `src_cbc_mclean_fund` | `src_cbc_mclean_fund_2017` | https://www.cbc.ca/news/canada/montreal/stuart-mclean-fund-to-help-kids-in-need-attend-quebec-camp-1.3987146 |
| `src_websearch_taylor_statten_cca` | `src_cca_history` | https://www.ccamping.org/history |
| `src_cca_ross_macdonald_doctors_cottage` | `src_cca_ross_macdonald_kanawana` | https://www.cca.qc.ca/en/archives/45474/fonds-ross-macdonald/387039/projects/50576/doctors-cottage-for-kamp-kanawana |
| `src_cfcf_broadcast_1941` | `src_cfcf_1941` | https://archive.org/details/1941-06-26-ymca-kamp-kanawana-broadcast-station-cfcf |
| `src_ia_cfcf_broadcast_1941` | `src_cfcf_1941` | https://archive.org/details/1941-06-26-ymca-kamp-kanawana-broadcast-station-cfcf |
| `src_ia_cfcf_1941` | `src_cfcf_1941` | https://archive.org/details/1941-06-26-ymca-kamp-kanawana-broadcast-station-cfcf |
| `src_concordia_ymca_fonds_12l` | `src_concordia_12L` | https://www.concordia.ca/offices/archives/ymca-fonds-sub-series-12L.html |
| `src_concordia_fonds_14D` | `src_concordia_14D10` | https://www.concordia.ca/offices/archives/ymca-fonds-sub-sub-series-14D10.html |
| `src_concordia_atom_fonds_p0145` | `src_concordia_atom_fonds` | https://concordia.accesstomemory.org/ymca-of-montreal-fonds-2 |
| `src_cathy_reeves_documentary_1993` | `src_concordia_kanawana_documentary` | https://concordia.accesstomemory.org/index.php/kamp-kanawana-the-experience-that-lasts-a-lifetime |
| `src_concordia_mclean` | `src_concordia_mclean_tribute` | https://www.concordia.ca/cunews/offices/vpaer/aar/2017/02/16/stuart-mclean-canadas-storyteller.html |
| `src_dawson_adam_research` | `src_dawson_chris_adam` | https://www.dawsoncollege.qc.ca/research/researchers/adam-chris |
| `src_dawson_crlt` | `src_dawson_seaman_scholarship` | https://www.dawsoncollege.qc.ca/community-recreation-leadership-training-crlt/scholarships |
| `src_biographi_cushing_lemuel` | `src_dcb_cushing` | https://www.biographi.ca/en/bio/cushing_lemuel_10E.html |
| `src_websearch_emsb_kanawana` | `src_emsb_kanawana_experience` | https://www.emsb.qc.ca/emsb/articles/camping-experience |
| `src_facebook_kanawana` | `src_facebook_ykanawana` | https://www.facebook.com/YKanawana |
| `src_facebook_kanawana_125` | `src_facebook_ykanawana` | https://www.facebook.com/YKanawana |
| `src_fb_kanawana` | `src_facebook_ykanawana` | https://www.facebook.com/YKanawana |
| `src_msn_kanawana_closed_2021` | `src_gazette_covid_2021` | https://www.msn.com/en-ca/news/canada/kanawana-sleepaway-camp-in-the-laurentians-to-remain-closed-this-summer/ar-BB1fRCYt |
| `src_gocamp_pro_kate_taylor` | `src_gocamp_pro_kate` | https://gocamp.pro/beyondcamp/social-media-advocacy |
| `src_gocamp_kate_taylor` | `src_gocamp_pro_kate` | https://gocamp.pro/beyondcamp/social-media-advocacy |
| `src_1951_kamp_kanawana_history` | `src_ia_kanawana_history_1951` | https://archive.org/details/1951-kamp-kanawana-history |
| `src_ymf_1900_12_10_seventh_annual_report_of_the_current_camp_committee` | `src_ia_seventh_annual_report_current_camp_1900` | https://archive.org/details/1900-12-10-seventh-annual-report-of-the-current-camp-committee |
| `src_ia_annual_report_1891` | `src_ia_ymca_annual_1891_92` | https://archive.org/details/sgw-ymca-annual-report-1991-1992 |
| `src_jsm_farrell_1998` | `src_jsm_farrell_1998_full` | https://journals.humankinetics.com/view/journals/jsm/12/4/article-p288.xml |
| `src_lapresse_desjardins_2018` | `src_lapresse_ymca_2018` | https://www.lapresse.ca/affaires/tetes-daffiche/201805/15/01-5181939-un-million-pour-les-ymca.php |
| `src_leigh_evans_lv_blog` | `src_leigh_evans_blog` | https://leighcevans.wordpress.com/about/camp |
| `src_mcmorris_thesis_spectrum` | `src_mcmorris_thesis` | https://spectrum.library.concordia.ca/id/eprint/992763 |
| `src_montrealer_mclean_2008` | `src_montrealer_mclean` | https://themontrealeronline.com/2008/01/stuart-mclean-from-montreal-west-to-the-vinyl-cafe |
| `src_montrealer_mosher_2016` | `src_montrealer_mosher_2016_kerr` | https://themontrealeronline.com/2016/02/terry-mosher-aka-aislin |
| `src_montreal_families_gender_2022` | `src_mtl_families_gender` | https://www.montrealfamilies.ca/kanawana-breaks-down-gender-barriers-with-third-sleeping-option |
| `src_montreal_families_gender` | `src_mtl_families_gender` | https://www.montrealfamilies.ca/kanawana-breaks-down-gender-barriers-with-third-sleeping-option |
| `src_newspapers_gazette_1897` | `src_newspapers_com_gazette` | https://www.newspapers.com/article/the-gazette-ymca-summer-camp-kanawana/35176458 |
| `src_nouvelles_laurentides_kanawana_2024` | `src_nouvelles_laurentides_2024` | https://nouvelleslaurentides.ca/lete-2024-marque-loffre-dun-nouveau-programme-a-saint-sauveur-aventure-a-kanawana |
| `src_wikipedia_camp_ouareau` | `src_ouareau_wikipedia` | https://en.wikipedia.org/wiki/Camp_Ouareau |
| `src_ourkids_mclean_interview` | `src_ourkids_mclean` | https://www.ourkids.net/camp/stuart-mclean-interview.php |
| `src_edgar_university_paper` | `src_ourontario_mary_edgar` | https://images.ourontario.ca/sunstrong/72744/data |
| `src_qahn_ymca_camp` | `src_qahn_howard` | https://qahn.org/article/ymca-camp-saint-adolphe-dhoward |
| `src_qahn_ymca_camp_saint_adolphe` | `src_qahn_howard` | https://qahn.org/article/ymca-camp-saint-adolphe-dhoward |
| `src_readers_digest_buckland` | `src_readers_digest_camp_shapes_lives` | https://www.readersdigest.ca/culture/how-summer-camp-shapes-lives |
| `src_samaritanmag_mclean_2017` | `src_samaritanmag_mclean` | https://www.samaritanmag.com/news/why-family-late-vinyl-cafe-host-stuart-mclean-asks-donations-camp-kanawana |
| `src_samaritanmag_mclean_kanawana` | `src_samaritanmag_mclean` | https://www.samaritanmag.com/news/why-family-late-vinyl-cafe-host-stuart-mclean-asks-donations-camp-kanawana |
| `src_trent_cca_fonds_78_004` | `src_trent_cca_fonds` | https://archives.trentu.ca/index.php/78-004 |
| `src_taylor_statten_camps` | `src_tsc_history` | https://taylorstattencamps.com/tsc-history |
| `src_umn_ymca_canada_records` | `src_umn_kautz_ymca` | https://archives.lib.umn.edu/repositories/7/resources/992 |
| `src_websearch_page_family_vss` | `src_vss_familles_pionnieres` | https://www.vss.ca/loisirs-et-culture/culture-et-communaute/les-familles-pionnieres-de-saint-sauveur |
| `src_westmount_mag_mclean` | `src_westmountmag_mclean` | https://www.westmountmag.ca/stuart-mclean |
| `src_wikipedia_big_cove_sections` | `src_wikipedia_big_cove` | https://en.wikipedia.org/wiki/Big_Cove_YMCA_Camp |
| `src_wikipedia_cushing_jr` | `src_wikipedia_cushing` | https://en.wikipedia.org/wiki/Lemuel_Cushing_Jr. |
| `src_wp_mosher` | `src_wikipedia_mosher` | https://en.wikipedia.org/wiki/Terry_Mosher |
| `src_wikipedia_harold_potter` | `src_wikipedia_potter` | https://en.wikipedia.org/wiki/Harold_H._Potter |
| `src_wikipedia_mclean` | `src_wikipedia_stuart_mclean` | https://en.wikipedia.org/wiki/Stuart_McLean |
| `src_ymcaq_120th_reunion` | `src_ymca_120th` | https://www.ymcaquebec.org/en/About-Us/Newsroom/2014-en/Camp-YMCA-Kanawana-s-120th-anniversary-reunion-en |
| `src_ymca_john_island_newsletter` | `src_ymca_john_island_mclean_speech` | https://www.ymcaneo.ca/wp-content/uploads/2019/03/jic-alumni-newsletter-spring-2012.pdf |
| `src_ymca_pip_adam_2017` | `src_ymca_pip_adam` | https://www.ymcaquebec.org/en/about-us/newsroom/2017/environmentalist-teacher-chris-adam-receives-camp |
| `src_ymca_pip_sharpe_2018` | `src_ymca_pip_sharpe` | https://www.ymcaquebec.org/en/About-Us/Newsroom/2018/Refugee-Advocate-Marina-Sharpe-Receives-Camp-YMCA |
| `src_ymca_pip_orbinski` | `src_ymca_quebec_pip_orbinski_2024` | https://www.ymcaquebec.org/en/about-us/newsroom/2024/dr-james-orbinski-receives-the-camp-ymca-kanawana-pip-award |
| `src_ymca_pip_orbinski_2024` | `src_ymca_quebec_pip_orbinski_2024` | https://www.ymcaquebec.org/en/about-us/newsroom/2024/dr-james-orbinski-receives-the-camp-ymca-kanawana-pip-award |
| `src_ymca_pip_award_skinner` | `src_ymca_quebec_pip_skinner` | https://www.ymcaquebec.org/en/news/als-advocate-carol-skinner-receives-camp-ymca-kanawana |
| `src_ymca_gta_blog_games` | `src_ymcagta_pinecrest_games` | https://www.ymcagta.org/blog/celebrating-tradition-with-the-pine-crest-games |
| `src_ymcagta_pine_crest_games` | `src_ymcagta_pinecrest_games` | https://www.ymcagta.org/blog/celebrating-tradition-with-the-pine-crest-games |
| `src_youtube_kanawana_silent` | `src_youtube_kanawana_1960s_silent_film` | https://www.youtube.com/watch?v=ZrUuQ1SU7q8 |
| `src_sam_lazarus_zeffy` | `src_zeffy_lazarus_fund` | https://www.zeffy.com/fundraising/8bc0b92d-1ae8-4791-8eeb-d890713c2360 |
