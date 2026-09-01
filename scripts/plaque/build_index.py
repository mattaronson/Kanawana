"""Build a person index from the p_291 plaque audit.

NOTE ON 'WOLF': the 2009 boards credit a "Wolf" beneath Counsellor and
Tripper. An earlier version of this script classed that as a STAFF title.
It is not: the operator identifies WOLF as a leadership PROGRAMME -- the
Rangers programme revived in 2001 and renamed Wolf later that decade -- so
a "Wolf" on a trip board is a programme participant attached to the trip,
exactly as "L.I.T. Daphne Pungartnik" and "Lit Amy D." are on other boards.
It is counted as a leadership-track position, never as staff.

Conservative by design. Two names merge only if their NORMALISED forms are
identical, or if the pair appears in ALIASES -- a hand-curated list, every
entry of which was justified in the audit record. Nothing merges on
similarity alone; near-misses are reported separately for human judgement,
never folded in silently.

Initial-only entries ("Katie A-F.", "Mark C.C.") are indexed but excluded
from cross-year tracing, because an initial is not a name.
"""
import json, re, unicodedata, collections, os

ROLE_KEYS = {
 'director':'Director','directors':'Director','directress':'Directress',
 'section_director':'Section Director','coordinators':'Co-ordinator',
 'masters':'Master','capitaine':'Capitaine','counsellor':'Counsellor',
 'counsellors':'Counsellor','cit':'CIT','cits':'CIT','lit':'LIT','lits':'LIT',
 'jc':'JC','jcs':'JC','jcgs':'JC','tripper':'Tripper','trippers':'Tripper',
 'wolf':'Wolf programme','therapist':'Therapist(joke)','guest':'Guest','crew':'Maintenance',
 'staff':'Staff','swimmers':'Swimmer','recipients':'Award recipient',
 'namers':'Cabin namer','signatories':'Signatory','signed':'Signatory',
 'participants':'Participant','members':'Member','campers':'Camper',
 'rangers':'Ranger','voyageurs':'Voyageur','girls':'Camper','boys':'Camper',
 'section':'Member','led_by':'Section leader','confirmed_subset':'Staff',
 'cit_program_director':'CIT Program Director','cit_director':'CIT Director',
 'jbc':'JBC','roll':'Knight',
}
SKIP_KEYS = {'title','motto','mottos','text','inscription','inscriptions','caption',
 'marginalia','device','devices','carved_devices','epigraph','epitaph','dedication',
 'aside','footer','form','object','structure','quotation','song_list_faded','sessions',
 'session','dates','tags','lakes_mapped','origins_listed','years_down_edge','group_mottos',
 'motto_words','blessing','attached_tag','names_low_confidence','ring_tokens','readable',
 'left','right','col1','col2','col3','col4','upper','lower','house_1','house_2',
 'footer_cluster','closing','acrostic_B_A_S_I_N','others','1st','2nd','3rd','4th',
 'window_1','window_2','window_3','window_4','window_5','lower_row','wheels',
 'group_1','group_2','left_paddle','right_paddle','centre_board','adjacent_cursive_board',
 'shelf_label','special_guests_faded','1st_session','3rd_session','4th_session',
 '1st_session_JCGs','1st_session_leader','3rd_session_lit','3rd_session_tripper',
 '3rd_session_dates','1st_session_jbcs','3rd_cabin','speech_bubbles','trailing',
 'Talahassee_2nd_session','Swazi_4th_session','Talahassee_3rd_session',
 'Basin_Breezers_3rd_session','winning_team','hierarchy','counsellors_note'}
# keys that ARE name lists but whose key gives no role
GENERIC = {'left','right','col1','col2','col3','col4','upper','lower','house_1','house_2',
 'footer_cluster','1st','2nd','3rd','4th','window_1','window_2','window_3','window_4',
 'window_5','lower_row','wheels','group_1','group_2','left_paddle','right_paddle',
 'adjacent_cursive_board','special_guests_faded','1st_session','3rd_session','4th_session',
 '3rd_cabin','Talahassee_2nd_session','Swazi_4th_session','Talahassee_3rd_session',
 'Basin_Breezers_3rd_session','acrostic_B_A_S_I_N','others','readable','ring_tokens'}

ALIASES = {  # justified in the audit record; nothing here is a guess
 'matt hamerman':'matt hamerman','matthew hammerman':'matt hamerman',
 'matt wiviott':'matt wiviott','matthew wiviott':'matt wiviott','matt iviott':'matt wiviott',
 'evan frankel':'evan frankel','evan frenkel':'evan frankel',
 'tiff bollhorn':'tiff bollhorn','tiffany ballhorn':'tiff bollhorn',
 'alex bollhorn':'alex bollhorn','alex ballhorn':'alex bollhorn',
 'sarah a-frankel':'sarah addleman frankel','sarah addleman frankel':'sarah addleman frankel',
 'sarah a[ddleman]-frankel':'sarah addleman frankel',
 'nick zarins':'nick zarins','nikk zarins':'nick zarins',
 'lindsay mcdougall':'lindsay mcdougall','lindsay macdougall':'lindsay mcdougall',
 'helena longpre':'helena longpre','heléna longpré':'helena longpre',
 'scott macleod':'scott macleod','scott mcleod':'scott macleod',
 'sally waff':'sally watt','sally watt':'sally watt',
 'j.m. sotiran':'jm sotiron','j.m. (jeff) sotiron':'jm sotiron',
 'sam trowbridge':'sam trowbridge',"sam 'sassim' trowbridge":'sam trowbridge',
 "sam 'saddam' trowbridge":'sam trowbridge',
 'jonathan nagles':'jonathan nagles','johnny nagles':'jonathan nagles',
 'sydney hassoun':'sydney hassoun','sydney hassan':'sydney hassoun',
 'caroline di tommaso':'caroline di tommaso','caroline di tomasso':'caroline di tommaso',
 'reiko webster':'reiko webster','rieke webster':'reiko webster',
 'razi fraticelli':'razi fraticelli','razz fraficelli':'razi fraticelli',
 'meyland g-labelle':'meyland g-labelle','myland g-l.':'meyland g-labelle',
 'nanette lloyd-hughes':'nanette lloyd-hughes','nam l-hughes':'nanette lloyd-hughes',
 'jess dobrinski':'jess dobrinski','jessica dobrinski':'jess dobrinski',
 'emily lecker':'emily lecker','em lecker':'emily lecker',
 'jonathan mee':'jon mee','jon mee':'jon mee',
 'nicolas muszynski':'nick muszynski','nick muszynski':'nick muszynski',
 'charles shulman':'charlie shulman','charlie shulman':'charlie shulman',
 'julien tasse':'julien tasse','julien tassé':'julien tasse',
 'yves tasse':'yves tasse','yves tassé':'yves tasse',
 'emily feldman':'emily feldman',"emily 'melvin' feldman":'emily feldman',
 'jeff muss':'jeff muss',"jeff 'travolta' muss":'jeff muss',
 'nancy fletcher':'nancy fletcher',"nandy 'fletch' fletcher":'nancy fletcher',
 'andrew eldridge':'andrew eldridge',"andrew 'hippo' eldridge":'andrew eldridge',
 "andrew 'hippo' elridge":'andrew eldridge',
 'louis lessard':'louis lessard','louis less[ard]':'louis lessard',
 'jen kaufman':'jennifer kaufman','jennifer kaufman':'jennifer kaufman',
 'jenny kaufman':'jennifer kaufman','jen kauf[man]':'jennifer kaufman',
 'dylan o brian':'dylan obrien','dylan o brien':'dylan obrien',
 'mike zeltzer':'michael zeitzer','micheal zeitzer':'michael zeitzer',
}

def strip_nick(s):
    s = re.sub(r'"[^"]*"', ' ', s)
    s = re.sub(r"'[^']*'", ' ', s)
    s = re.sub(r'\([^)]*\)', ' ', s)
    s = re.sub(r'\[[^\]]*\]', ' ', s)
    return s

def norm(s):
    s = strip_nick(s)
    s = unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode()
    s = s.lower().replace('.', ' ').replace('&',' ')
    s = re.sub(r'[^a-z0-9\- ]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return ALIASES.get(s, s)

def is_initial_only(n):
    toks = n.split()
    if len(toks) < 2: return True
    return all(len(t.strip('-')) <= 2 for t in toks[1:])

YEAR_RE = re.compile(r'(?:19|20)\d{2}')
def year_of(row):
    for src in (row['names'].get('title',''), row['image']):
        if not isinstance(src, str): continue
        m = YEAR_RE.findall(src)
        if m: return int(m[0])
    m = re.search(r"'(\d{2})\b", str(row['names'].get('title','')))
    if m:
        y = int(m.group(1)); return 1900+y if y > 30 else 2000+y
    m = re.search(r'-(\d{2})\.jpg', row['image'])
    if m:
        y = int(m.group(1)); return 1900+y if y > 30 else 2000+y
    return None

def group_of(row):
    t = (row['names'].get('title') or row['image']).lower()
    for key, label in [('cit','CIT'),('lit','LIT'),('staff','Staff'),('ranger','Rangers'),
      ('voyageur','Voyageurs'),('advance guard','Advance Guard'),('knight','Knights'),
      ('swim','Swim'),('basin','Basin'),('swazi','Swazi'),('malibu','Malibu'),
      ('lookout','Lookout'),('chopsy','Chopsy'),('rock tent','Rock Tent'),
      ('roadhouse','Roadhouse'),('road house','Roadhouse'),('senior girl','Senior Girls'),
      ('senior boy','Senior Boys'),('jbc','JBC'),('junior','Junior'),('jc','JC'),
      ('explorer','Explorer'),('adventurer','Adventurer'),('talahassee','Talahassee'),
      ('nature trip','Nature Trip'),('kanawoodstock','Kanawoodstock'),('rounds','Rounds'),
      ('pink flam','Pink Flamingo'),('maintenance','Maintenance'),('kanoing','Canoe Staff'),
      ('sailing','Sailing Staff'),('pig pen','Pig Pen'),('all-kamp','All-Kamp'),
      ('all kamp','All-Kamp')]:
        if key in t: return label
    return None

rows = [json.loads(l) for l in open('kb/plaque-audit/audit.jsonl')]
index = collections.defaultdict(list)
raw_forms = collections.defaultdict(set)

for r in rows:
    yr, grp = year_of(r), group_of(r)
    for key, val in r['names'].items():
        if key in SKIP_KEYS and key not in GENERIC: continue
        role = ROLE_KEYS.get(key, 'Member' if key in GENERIC else None)
        if role is None: continue
        items = val if isinstance(val, list) else [val]
        for it in items:
            if isinstance(it, list) and len(it) == 2 and isinstance(it[1], int):
                nm, y2 = it[0], it[1]           # Knights roll: [name, year]
            elif isinstance(it, str):
                nm, y2 = it, yr
            else:
                continue
            n = norm(nm)
            if not n or len(n) < 3: continue
            raw_forms[n].add(nm.strip())
            index[n].append({'year': y2, 'group': grp, 'role': role,
                             'image': r['image'], 'as_written': nm.strip()})

os.makedirs('kb/plaque-audit', exist_ok=True)
out = {}
for n, apps in index.items():
    yrs = sorted({a['year'] for a in apps if a['year']})
    out[n] = {'forms': sorted(raw_forms[n]), 'appearances': apps,
              'years': yrs, 'span': (yrs[-1]-yrs[0]) if len(yrs) > 1 else 0,
              'initial_only': is_initial_only(n)}
json.dump(out, open('kb/plaque-audit/person-index.json','w'), indent=1, ensure_ascii=False)

multi = {n: d for n, d in out.items() if len(d['years']) > 1 and not d['initial_only']}
print('distinct normalised names :', len(out))
print('name-appearances          :', sum(len(d['appearances']) for d in out.values()))
print('traced across >1 YEAR     :', len(multi))
print('spanning >=5 years        :', sum(1 for d in multi.values() if d['span'] >= 5))
print('spanning >=10 years       :', sum(1 for d in multi.values() if d['span'] >= 10))
